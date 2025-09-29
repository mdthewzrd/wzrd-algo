import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const getCurrentUser = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return null;

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user) return null;

    // Don't send encrypted API key to client
    const { encryptedApiKey, apiKeyIv, ...safeUser } = user;
    
    return {
      ...safeUser,
      hasApiKey: !!encryptedApiKey,
    };
  },
});

export const createOrUpdateUser = mutation({
  args: {
    clerkId: v.string(),
    name: v.string(),
    email: v.string(),
  },
  handler: async (ctx, args) => {
    const existingUser = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (existingUser) {
      await ctx.db.patch(existingUser._id, {
        name: args.name,
        email: args.email,
        lastActiveAt: Date.now(),
      });
      return existingUser._id;
    }

    const userId = await ctx.db.insert("users", {
      clerkId: args.clerkId,
      name: args.name,
      email: args.email,
      createdAt: Date.now(),
      lastActiveAt: Date.now(),
      settings: {
        notificationEmail: true,
        notificationInApp: true,
        timezone: "UTC",
      },
    });

    // Create default drip styles for new user
    await createDefaultDripStyles(ctx, userId);

    return userId;
  },
});

// Note: updateApiKey action has been moved to nodeActions.ts since it uses Node.js crypto APIs

export const updateUserApiKey = mutation({
  args: {
    clerkId: v.string(),
    encryptedApiKey: v.string(),
    apiKeyIv: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .first();

    if (!user) throw new Error("User not found");

    await ctx.db.patch(user._id, {
      encryptedApiKey: args.encryptedApiKey,
      apiKeyIv: args.apiKeyIv,
    });

    // Log audit
    await ctx.db.insert("auditLogs", {
      userId: user._id,
      action: "user.api_key_updated",
      entityType: "user",
      entityId: user._id,
      timestamp: Date.now(),
    });
  },
});

export const updateSettings = mutation({
  args: {
    notificationEmail: v.optional(v.boolean()),
    notificationInApp: v.optional(v.boolean()),
    defaultDripStyleId: v.optional(v.id("dripFeedStyles")),
    timezone: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user) throw new Error("User not found");

    const currentSettings = user.settings || {};
    const updatedSettings = {
      ...currentSettings,
      ...(args.notificationEmail !== undefined && { notificationEmail: args.notificationEmail }),
      ...(args.notificationInApp !== undefined && { notificationInApp: args.notificationInApp }),
      ...(args.defaultDripStyleId !== undefined && { defaultDripStyleId: args.defaultDripStyleId }),
      ...(args.timezone !== undefined && { timezone: args.timezone }),
    };

    await ctx.db.patch(user._id, {
      settings: updatedSettings,
    });

    return { success: true };
  },
});

export const deleteAccount = mutation({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user) throw new Error("User not found");

    // Check for active campaigns
    const activeCampaigns = await ctx.db
      .query("dripFeedCampaigns")
      .withIndex("by_user_and_status", (q) => 
        q.eq("userId", user._id).eq("status", "active")
      )
      .first();

    if (activeCampaigns) {
      throw new Error("Cannot delete account with active campaigns. Please pause or cancel all campaigns first.");
    }

    // Delete all user data
    const campaigns = await ctx.db
      .query("dripFeedCampaigns")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .collect();

    for (const campaign of campaigns) {
      // Delete dispatch logs
      const logs = await ctx.db
        .query("dispatchLogs")
        .withIndex("by_campaign", (q) => q.eq("campaignId", campaign._id))
        .collect();
      
      for (const log of logs) {
        await ctx.db.delete(log._id);
      }

      await ctx.db.delete(campaign._id);
    }

    // Delete packages
    const packages = await ctx.db
      .query("packages")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .collect();

    for (const pkg of packages) {
      await ctx.db.delete(pkg._id);
    }

    // Delete notifications
    const notifications = await ctx.db
      .query("notifications")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .collect();

    for (const notification of notifications) {
      await ctx.db.delete(notification._id);
    }

    // Delete audit logs
    const auditLogs = await ctx.db
      .query("auditLogs")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .collect();

    for (const log of auditLogs) {
      await ctx.db.delete(log._id);
    }

    // Finally, delete the user
    await ctx.db.delete(user._id);

    return { success: true };
  },
});

// Helper function to create default drip styles
async function createDefaultDripStyles(ctx: any, userId: string) {
  const defaultStyles = [
    {
      name: "Uniform Distribution",
      description: "Evenly distributes orders across the time period",
      algorithm: "uniform" as const,
      logicDefinition: {
        intervalMinutes: 15,
        steps: 40,
        minSliceSize: 10,
        maxSliceSize: 1000,
      },
      isDefault: true,
      createdAt: Date.now(),
    },
    {
      name: "Ramp Up",
      description: "Starts slow and gradually increases delivery speed",
      algorithm: "rampUp" as const,
      logicDefinition: {
        intervalMinutes: 15,
        steps: 40,
        minSliceSize: 5,
        maxSliceSize: 1500,
        growthRate: 1.5,
      },
      isDefault: false,
      createdAt: Date.now(),
    },
    {
      name: "Ramp Down",
      description: "Starts fast and gradually decreases delivery speed",
      algorithm: "rampDown" as const,
      logicDefinition: {
        intervalMinutes: 15,
        steps: 40,
        minSliceSize: 10,
        maxSliceSize: 2000,
        decayRate: 0.8,
      },
      isDefault: false,
      createdAt: Date.now(),
    },
    {
      name: "Pulse Pattern",
      description: "Creates waves of high and low activity",
      algorithm: "pulse" as const,
      logicDefinition: {
        intervalMinutes: 20,
        steps: 36,
        minSliceSize: 5,
        maxSliceSize: 1000,
        pulseConfig: {
          amplitude: 0.4,
          frequency: 3,
          phaseShift: 0,
        },
      },
      isDefault: false,
      createdAt: Date.now(),
    },
    {
      name: "Natural Growth",
      description: "Mimics organic viral growth pattern",
      algorithm: "naturalGrowth" as const,
      logicDefinition: {
        intervalMinutes: 30,
        steps: 24,
        minSliceSize: 10,
        maxSliceSize: 2500,
        growthRate: 8,
        noiseLevel: 0.15,
      },
      isDefault: false,
      createdAt: Date.now(),
    },
    {
      name: "Viral Spike",
      description: "Creates a spike pattern like viral content",
      algorithm: "viralSpike" as const,
      logicDefinition: {
        intervalMinutes: 10,
        steps: 60,
        minSliceSize: 5,
        maxSliceSize: 5000,
        noiseLevel: 0.2,
      },
      isDefault: false,
      createdAt: Date.now(),
    },
  ];

  for (const style of defaultStyles) {
    await ctx.db.insert("dripFeedStyles", style);
  }
}