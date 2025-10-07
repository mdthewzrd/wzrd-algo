import { v } from "convex/values";
import { mutation, query, action } from "./_generated/server";
import { Doc, Id } from "./_generated/dataModel";

// Queries
export const getCampaigns = query({
  args: {
    status: v.optional(v.union(
      v.literal("draft"),
      v.literal("active"),
      v.literal("paused"),
      v.literal("completed"),
      v.literal("failed"),
      v.literal("cancelled")
    )),
    limit: v.optional(v.number()),
    cursor: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
    
    if (!user) throw new Error("User not found");

    let query = ctx.db
      .query("dripFeedCampaigns")
      .withIndex("by_user", (q) => q.eq("userId", user._id));

    if (args.status) {
      query = ctx.db
        .query("dripFeedCampaigns")
        .withIndex("by_user_and_status", (q) => 
          q.eq("userId", user._id).eq("status", args.status)
        );
    }

    const campaigns = await query
      .order("desc")
      .take(args.limit || 50);

    return {
      items: campaigns,
      nextCursor: campaigns.length === (args.limit || 50) ? 
        campaigns[campaigns.length - 1]._id : undefined,
    };
  },
});

export const getCampaignById = query({
  args: { id: v.id("dripFeedCampaigns") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const campaign = await ctx.db.get(args.id);
    if (!campaign) throw new Error("Campaign not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || campaign.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    return campaign;
  },
});

export const getCampaignMetrics = query({
  args: { id: v.id("dripFeedCampaigns") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const campaign = await ctx.db.get(args.id);
    if (!campaign) throw new Error("Campaign not found");

    const dispatches = await ctx.db
      .query("dispatchLogs")
      .withIndex("by_campaign", (q) => q.eq("campaignId", args.id))
      .collect();

    const totalOrdered = campaign.services.reduce((sum, s) => sum + s.totalQuantity, 0);
    const totalDelivered = campaign.services.reduce((sum, s) => sum + s.deliveredQuantity, 0);
    const totalFailed = campaign.services.reduce((sum, s) => sum + s.failedQuantity, 0);
    
    const successRate = dispatches.length > 0 
      ? dispatches.filter(d => d.status === "success").length / dispatches.length 
      : 0;

    const avgLatency = dispatches
      .filter(d => d.latencyMs)
      .reduce((sum, d) => sum + (d.latencyMs || 0), 0) / 
      (dispatches.filter(d => d.latencyMs).length || 1);

    return {
      totalOrdered,
      totalDelivered,
      totalFailed,
      progress: totalOrdered > 0 ? totalDelivered / totalOrdered : 0,
      successRate,
      avgLatencyMs: avgLatency,
      dispatchCount: dispatches.length,
      status: campaign.status,
      estimatedCompletionTime: calculateEstimatedCompletion(campaign),
    };
  },
});

// Mutations
export const createCampaign = mutation({
  args: {
    name: v.string(),
    targetURL: v.string(),
    dripFeedStyleId: v.id("dripFeedStyles"),
    packageId: v.optional(v.id("packages")),
    services: v.array(v.object({
      serviceId: v.string(),
      name: v.string(),
      totalQuantity: v.number(),
      pricePerThousand: v.number(),
    })),
    metadata: v.optional(v.object({
      clientName: v.optional(v.string()),
      projectName: v.optional(v.string()),
      tags: v.optional(v.array(v.string())),
      notes: v.optional(v.string()),
    })),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
    
    if (!user) throw new Error("User not found");
    if (!user.encryptedApiKey) throw new Error("API key not configured");

    // Validate URL
    if (!isValidUrl(args.targetURL)) {
      throw new Error("Invalid target URL");
    }

    // Validate style exists
    const style = await ctx.db.get(args.dripFeedStyleId);
    if (!style) throw new Error("Drip feed style not found");

    // Calculate total cost
    const totalCost = args.services.reduce((sum, service) => {
      return sum + (service.totalQuantity / 1000) * service.pricePerThousand;
    }, 0);

    const campaignId = await ctx.db.insert("dripFeedCampaigns", {
      userId: user._id,
      name: args.name,
      targetURL: args.targetURL,
      status: "draft",
      dripFeedStyleId: args.dripFeedStyleId,
      packageId: args.packageId,
      services: args.services.map(service => ({
        ...service,
        deliveredQuantity: 0,
        failedQuantity: 0,
        minQuantity: 1,
        maxQuantity: service.totalQuantity,
      })),
      totalCost,
      spentCost: 0,
      createdAt: Date.now(),
      retryCount: 0,
      metadata: args.metadata,
    });

    // Log audit
    await ctx.db.insert("auditLogs", {
      userId: user._id,
      action: "campaign.created",
      entityType: "campaign",
      entityId: campaignId,
      changes: JSON.stringify(args),
      timestamp: Date.now(),
    });

    return campaignId;
  },
});

export const startCampaign = mutation({
  args: { id: v.id("dripFeedCampaigns") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const campaign = await ctx.db.get(args.id);
    if (!campaign) throw new Error("Campaign not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || campaign.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    if (campaign.status !== "draft" && campaign.status !== "paused") {
      throw new Error(`Cannot start campaign in ${campaign.status} status`);
    }

    await ctx.db.patch(args.id, {
      status: "active",
      startedAt: campaign.startedAt || Date.now(),
      pausedAt: undefined,
    });

    // Create notification
    await ctx.db.insert("notifications", {
      userId: user._id,
      type: "campaign_started",
      severity: "info",
      title: "Campaign Started",
      message: `Campaign "${campaign.name}" has been started`,
      metadata: { campaignId: args.id },
      isRead: false,
      isEmailSent: false,
      createdAt: Date.now(),
    });

    return { success: true };
  },
});

export const pauseCampaign = mutation({
  args: { id: v.id("dripFeedCampaigns") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const campaign = await ctx.db.get(args.id);
    if (!campaign) throw new Error("Campaign not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || campaign.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    if (campaign.status !== "active") {
      throw new Error(`Cannot pause campaign in ${campaign.status} status`);
    }

    await ctx.db.patch(args.id, {
      status: "paused",
      pausedAt: Date.now(),
    });

    // Log audit
    await ctx.db.insert("auditLogs", {
      userId: user._id,
      action: "campaign.paused",
      entityType: "campaign",
      entityId: args.id,
      timestamp: Date.now(),
    });

    return { success: true };
  },
});

export const resumeCampaign = mutation({
  args: { id: v.id("dripFeedCampaigns") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const campaign = await ctx.db.get(args.id);
    if (!campaign) throw new Error("Campaign not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || campaign.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    if (campaign.status !== "paused") {
      throw new Error(`Cannot resume campaign in ${campaign.status} status`);
    }

    await ctx.db.patch(args.id, {
      status: "active",
      pausedAt: undefined,
      circuitBreakerOpenUntil: undefined,
    });

    return { success: true };
  },
});

export const cancelCampaign = mutation({
  args: { id: v.id("dripFeedCampaigns") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const campaign = await ctx.db.get(args.id);
    if (!campaign) throw new Error("Campaign not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || campaign.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    if (campaign.status === "completed" || campaign.status === "cancelled") {
      throw new Error(`Cannot cancel campaign in ${campaign.status} status`);
    }

    await ctx.db.patch(args.id, {
      status: "cancelled",
      completedAt: Date.now(),
    });

    // Create notification
    await ctx.db.insert("notifications", {
      userId: user._id,
      type: "campaign_completed",
      severity: "warning",
      title: "Campaign Cancelled",
      message: `Campaign "${campaign.name}" has been cancelled`,
      metadata: { campaignId: args.id },
      isRead: false,
      isEmailSent: false,
      createdAt: Date.now(),
    });

    return { success: true };
  },
});

// Helper functions
function isValidUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    return ["http:", "https:"].includes(parsed.protocol);
  } catch {
    return false;
  }
}

function calculateEstimatedCompletion(campaign: Doc<"dripFeedCampaigns">): number | null {
  if (campaign.status !== "active" || !campaign.startedAt) {
    return null;
  }

  const totalOrdered = campaign.services.reduce((sum, s) => sum + s.totalQuantity, 0);
  const totalDelivered = campaign.services.reduce((sum, s) => sum + s.deliveredQuantity, 0);
  const remaining = totalOrdered - totalDelivered;

  if (remaining <= 0) return Date.now();

  const elapsedTime = Date.now() - campaign.startedAt;
  const deliveryRate = totalDelivered / (elapsedTime / 1000 / 60); // per minute

  if (deliveryRate <= 0) return null;

  const remainingMinutes = remaining / deliveryRate;
  return Date.now() + (remainingMinutes * 60 * 1000);
}