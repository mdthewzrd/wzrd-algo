import { v } from "convex/values";
import { query } from "./_generated/server";

export const getSystemMetrics = query({
  args: {
    metric: v.string(),
    timeRange: v.optional(v.union(
      v.literal("1h"),
      v.literal("6h"),
      v.literal("24h"),
      v.literal("7d"),
      v.literal("30d")
    )),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const timeRange = args.timeRange || "24h";
    const now = Date.now();
    let startTime: number;

    switch (timeRange) {
      case "1h":
        startTime = now - 60 * 60 * 1000;
        break;
      case "6h":
        startTime = now - 6 * 60 * 60 * 1000;
        break;
      case "24h":
        startTime = now - 24 * 60 * 60 * 1000;
        break;
      case "7d":
        startTime = now - 7 * 24 * 60 * 60 * 1000;
        break;
      case "30d":
        startTime = now - 30 * 24 * 60 * 60 * 1000;
        break;
      default:
        startTime = now - 24 * 60 * 60 * 1000;
    }

    const metrics = await ctx.db
      .query("systemMetrics")
      .withIndex("by_metric_time", (q) => 
        q.eq("metric", args.metric).gte("timestamp", startTime)
      )
      .order("asc")
      .take(1000);

    return aggregateMetrics(metrics, timeRange);
  },
});

export const getDashboardStats = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
    
    if (!user) throw new Error("User not found");

    // Get campaign stats
    const campaigns = await ctx.db
      .query("dripFeedCampaigns")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .collect();

    const activeCampaigns = campaigns.filter(c => c.status === "active").length;
    const completedCampaigns = campaigns.filter(c => c.status === "completed").length;
    const failedCampaigns = campaigns.filter(c => c.status === "failed").length;

    // Calculate total delivered
    const totalDelivered = campaigns.reduce((sum, campaign) => {
      return sum + campaign.services.reduce((s, service) => 
        s + service.deliveredQuantity, 0
      );
    }, 0);

    const totalOrdered = campaigns.reduce((sum, campaign) => {
      return sum + campaign.services.reduce((s, service) => 
        s + service.totalQuantity, 0
      );
    }, 0);

    const totalSpent = campaigns.reduce((sum, campaign) => 
      sum + campaign.spentCost, 0
    );

    // Get recent dispatch success rate
    const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;
    const recentDispatches = await ctx.db
      .query("dispatchLogs")
      .withIndex("by_status")
      .filter((q) => q.gte(q.field("createdAt"), oneDayAgo))
      .take(100);

    const successfulDispatches = recentDispatches.filter(d => 
      d.status === "success"
    ).length;
    
    const successRate = recentDispatches.length > 0 
      ? (successfulDispatches / recentDispatches.length) * 100 
      : 0;

    // Get package count
    const packages = await ctx.db
      .query("packages")
      .withIndex("by_user", (q) => q.eq("userId", user._id))
      .collect();

    return {
      campaigns: {
        total: campaigns.length,
        active: activeCampaigns,
        completed: completedCampaigns,
        failed: failedCampaigns,
      },
      delivery: {
        totalOrdered,
        totalDelivered,
        deliveryRate: totalOrdered > 0 
          ? (totalDelivered / totalOrdered) * 100 
          : 0,
      },
      financial: {
        totalSpent,
        avgCampaignCost: campaigns.length > 0 
          ? totalSpent / campaigns.length 
          : 0,
      },
      performance: {
        successRate,
        dispatchesLast24h: recentDispatches.length,
      },
      packages: {
        total: packages.length,
        active: packages.filter(p => p.isActive).length,
      },
    };
  },
});

export const getCampaignAnalytics = query({
  args: {
    campaignId: v.id("dripFeedCampaigns"),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const campaign = await ctx.db.get(args.campaignId);
    if (!campaign) throw new Error("Campaign not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || campaign.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    // Get all dispatch logs for this campaign
    const dispatchLogs = await ctx.db
      .query("dispatchLogs")
      .withIndex("by_campaign", (q) => q.eq("campaignId", args.campaignId))
      .collect();

    // Group by time buckets for timeline
    const timeline = createTimeline(dispatchLogs, campaign.startedAt || campaign.createdAt);

    // Calculate per-service stats
    const serviceStats = campaign.services.map(service => {
      const serviceLogs = dispatchLogs.filter(log => 
        log.serviceId === service.serviceId
      );

      const successful = serviceLogs.filter(log => 
        log.status === "success"
      ).length;

      const avgLatency = serviceLogs
        .filter(log => log.latencyMs)
        .reduce((sum, log) => sum + (log.latencyMs || 0), 0) / 
        (serviceLogs.filter(log => log.latencyMs).length || 1);

      return {
        serviceId: service.serviceId,
        name: service.name,
        totalQuantity: service.totalQuantity,
        deliveredQuantity: service.deliveredQuantity,
        failedQuantity: service.failedQuantity,
        progress: service.totalQuantity > 0 
          ? (service.deliveredQuantity / service.totalQuantity) * 100 
          : 0,
        successRate: serviceLogs.length > 0 
          ? (successful / serviceLogs.length) * 100 
          : 0,
        avgLatencyMs: avgLatency,
        dispatchCount: serviceLogs.length,
      };
    });

    // Calculate velocity (delivery rate over time)
    const velocity = calculateVelocity(dispatchLogs);

    return {
      campaign: {
        id: campaign._id,
        name: campaign.name,
        status: campaign.status,
        startedAt: campaign.startedAt,
        completedAt: campaign.completedAt,
      },
      timeline,
      serviceStats,
      velocity,
      summary: {
        totalDispatches: dispatchLogs.length,
        successfulDispatches: dispatchLogs.filter(d => d.status === "success").length,
        failedDispatches: dispatchLogs.filter(d => d.status === "failed").length,
        avgLatencyMs: dispatchLogs
          .filter(d => d.latencyMs)
          .reduce((sum, d) => sum + (d.latencyMs || 0), 0) / 
          (dispatchLogs.filter(d => d.latencyMs).length || 1),
      },
    };
  },
});

// Helper functions
function aggregateMetrics(metrics: any[], timeRange: string) {
  if (metrics.length === 0) return [];

  // Determine bucket size based on time range
  let bucketSizeMs: number;
  switch (timeRange) {
    case "1h":
      bucketSizeMs = 5 * 60 * 1000; // 5 minutes
      break;
    case "6h":
      bucketSizeMs = 30 * 60 * 1000; // 30 minutes
      break;
    case "24h":
      bucketSizeMs = 60 * 60 * 1000; // 1 hour
      break;
    case "7d":
      bucketSizeMs = 6 * 60 * 60 * 1000; // 6 hours
      break;
    case "30d":
      bucketSizeMs = 24 * 60 * 60 * 1000; // 1 day
      break;
    default:
      bucketSizeMs = 60 * 60 * 1000;
  }

  const buckets = new Map<number, { values: number[]; timestamp: number }>();

  for (const metric of metrics) {
    const bucketTime = Math.floor(metric.timestamp / bucketSizeMs) * bucketSizeMs;
    
    if (!buckets.has(bucketTime)) {
      buckets.set(bucketTime, { values: [], timestamp: bucketTime });
    }
    
    buckets.get(bucketTime)!.values.push(metric.value);
  }

  return Array.from(buckets.values()).map(bucket => ({
    timestamp: bucket.timestamp,
    value: bucket.values.reduce((sum, v) => sum + v, 0) / bucket.values.length,
    count: bucket.values.length,
  }));
}

function createTimeline(dispatchLogs: any[], startTime: number) {
  const bucketSizeMs = 60 * 60 * 1000; // 1 hour buckets
  const buckets = new Map<number, {
    timestamp: number;
    successful: number;
    failed: number;
    quantity: number;
  }>();

  for (const log of dispatchLogs) {
    const bucketTime = Math.floor(log.createdAt / bucketSizeMs) * bucketSizeMs;
    
    if (!buckets.has(bucketTime)) {
      buckets.set(bucketTime, {
        timestamp: bucketTime,
        successful: 0,
        failed: 0,
        quantity: 0,
      });
    }
    
    const bucket = buckets.get(bucketTime)!;
    if (log.status === "success") {
      bucket.successful++;
      bucket.quantity += log.quantity;
    } else if (log.status === "failed") {
      bucket.failed++;
    }
  }

  return Array.from(buckets.values()).sort((a, b) => a.timestamp - b.timestamp);
}

function calculateVelocity(dispatchLogs: any[]) {
  if (dispatchLogs.length < 2) return 0;

  const successfulLogs = dispatchLogs
    .filter(log => log.status === "success")
    .sort((a, b) => a.createdAt - b.createdAt);

  if (successfulLogs.length < 2) return 0;

  const timeSpan = successfulLogs[successfulLogs.length - 1].createdAt - successfulLogs[0].createdAt;
  const totalQuantity = successfulLogs.reduce((sum, log) => sum + log.quantity, 0);

  // Return quantity per hour
  return timeSpan > 0 ? (totalQuantity / timeSpan) * 60 * 60 * 1000 : 0;
}