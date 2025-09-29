import { v } from "convex/values";
import { internalMutation, internalAction, internalQuery, cronJobs } from "./_generated/server";
import { internal } from "./_generated/api";
import { Doc, Id } from "./_generated/dataModel";

// Cron configuration - runs every 5 minutes
const crons = cronJobs();

crons.interval(
  "process campaigns",
  { minutes: 5 },
  internal.scheduler.processCampaigns
);

export default crons;

// Main scheduler that orchestrates parallel processing
export const processCampaigns = internalAction({
  args: {},
  handler: async (ctx) => {
    console.log("🚀 Starting campaign processor - parallel execution");
    const startTime = Date.now();

    try {
      // Get all active campaigns that need processing
      const campaigns = await ctx.runQuery(internal.scheduler.getActiveCampaigns);
      
      if (!campaigns || campaigns.length === 0) {
        console.log("No active campaigns to process");
        return { processed: 0, duration: Date.now() - startTime };
      }

      console.log(`Processing ${campaigns.length} active campaigns in parallel`);

      // Process campaigns in parallel batches for maximum efficiency
      const BATCH_SIZE = 10; // Process 10 campaigns simultaneously
      const results = [];
      
      for (let i = 0; i < campaigns.length; i += BATCH_SIZE) {
        const batch = campaigns.slice(i, i + BATCH_SIZE);
        
        // Execute batch in parallel
        const batchPromises = batch.map(campaign => 
          processSingleCampaign(ctx, campaign)
            .catch(error => {
              console.error(`Error processing campaign ${campaign._id}:`, error);
              return { 
                campaignId: campaign._id, 
                success: false, 
                error: error.message 
              };
            })
        );

        const batchResults = await Promise.all(batchPromises);
        results.push(...batchResults);

        // Log batch completion
        console.log(`Batch ${Math.floor(i / BATCH_SIZE) + 1} completed: ${batchResults.filter(r => r.success).length}/${batch.length} successful`);
      }

      // Record metrics
      await ctx.runMutation(internal.scheduler.recordMetrics, {
        totalProcessed: results.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length,
        durationMs: Date.now() - startTime,
      });

      console.log(`✅ Campaign processing completed in ${Date.now() - startTime}ms`);
      console.log(`   Processed: ${results.length}, Success: ${results.filter(r => r.success).length}, Failed: ${results.filter(r => !r.success).length}`);

      return {
        processed: results.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length,
        duration: Date.now() - startTime,
        results,
      };
    } catch (error) {
      console.error("Fatal error in campaign processor:", error);
      throw error;
    }
  },
});

// Process a single campaign
async function processSingleCampaign(ctx: any, campaign: Doc<"dripFeedCampaigns">) {
  const campaignStartTime = Date.now();
  
  try {
    // Check circuit breaker
    if (campaign.circuitBreakerOpenUntil && campaign.circuitBreakerOpenUntil > Date.now()) {
      console.log(`Circuit breaker open for campaign ${campaign._id} until ${new Date(campaign.circuitBreakerOpenUntil).toISOString()}`);
      return { campaignId: campaign._id, success: false, reason: "circuit_breaker" };
    }

    // Get drip style configuration
    const style = await ctx.runQuery(internal.scheduler.getDripStyle, { 
      id: campaign.dripFeedStyleId 
    });

    if (!style) {
      throw new Error("Drip style not found");
    }

    // Get user for API key
    const user = await ctx.runQuery(internal.scheduler.getUser, { 
      id: campaign.userId 
    });

    if (!user || !user.encryptedApiKey) {
      throw new Error("User or API key not found");
    }

    // Calculate next slices for each service
    const slices = calculateDripSlices(campaign, style);
    
    if (!slices || slices.length === 0) {
      // Campaign might be completed
      await checkAndCompleteCampaign(ctx, campaign);
      return { campaignId: campaign._id, success: true, reason: "no_slices" };
    }

    // Process slices in parallel
    const dispatchPromises = slices.map(slice => 
      dispatchSlice(ctx, campaign, slice, user.encryptedApiKey, user.apiKeyIv)
        .catch(error => {
          console.error(`Dispatch error for service ${slice.serviceId}:`, error);
          return { success: false, error: error.message, slice };
        })
    );

    const dispatchResults = await Promise.all(dispatchPromises);

    // Update campaign status
    const successCount = dispatchResults.filter(r => r.success).length;
    const failCount = dispatchResults.filter(r => !r.success).length;

    await ctx.runMutation(internal.scheduler.updateCampaignProgress, {
      campaignId: campaign._id,
      dispatchResults,
      processingTimeMs: Date.now() - campaignStartTime,
    });

    // Check if we need to open circuit breaker
    if (failCount > slices.length * 0.5) {
      await ctx.runMutation(internal.scheduler.openCircuitBreaker, {
        campaignId: campaign._id,
        durationMinutes: 15,
      });
    }

    return {
      campaignId: campaign._id,
      success: true,
      slicesProcessed: slices.length,
      successful: successCount,
      failed: failCount,
      durationMs: Date.now() - campaignStartTime,
    };
  } catch (error) {
    console.error(`Error processing campaign ${campaign._id}:`, error);
    
    await ctx.runMutation(internal.scheduler.recordCampaignError, {
      campaignId: campaign._id,
      error: error.message,
    });

    return {
      campaignId: campaign._id,
      success: false,
      error: error.message,
      durationMs: Date.now() - campaignStartTime,
    };
  }
}

// Calculate drip feed slices based on style
function calculateDripSlices(
  campaign: Doc<"dripFeedCampaigns">, 
  style: Doc<"dripFeedStyles">
) {
  const slices = [];
  const now = Date.now();

  for (const service of campaign.services) {
    const remaining = service.totalQuantity - service.deliveredQuantity - service.failedQuantity;
    
    if (remaining <= 0) continue;

    // Check if it's time for next dispatch
    if (service.nextDispatchAt && service.nextDispatchAt > now) {
      continue;
    }

    // Calculate slice size based on style algorithm
    const sliceSize = calculateSliceSize(
      service,
      remaining,
      style,
      campaign.startedAt || now
    );

    if (sliceSize > 0) {
      slices.push({
        serviceId: service.serviceId,
        serviceName: service.name,
        quantity: Math.min(sliceSize, remaining),
        targetURL: campaign.targetURL,
      });
    }
  }

  return slices;
}

// Calculate slice size based on drip feed style
function calculateSliceSize(
  service: any,
  remaining: number,
  style: Doc<"dripFeedStyles">,
  campaignStartTime: number
): number {
  const { algorithm, logicDefinition } = style;
  const { steps, minSliceSize, maxSliceSize } = logicDefinition;
  
  const elapsedTime = Date.now() - campaignStartTime;
  const totalDuration = steps * logicDefinition.intervalMinutes * 60 * 1000;
  const progress = Math.min(elapsedTime / totalDuration, 1);
  
  let baseSize = Math.ceil(service.totalQuantity / steps);
  let sliceSize = baseSize;

  switch (algorithm) {
    case "uniform":
      // Even distribution
      sliceSize = baseSize;
      break;
      
    case "rampUp":
      // Start slow, accelerate
      sliceSize = Math.ceil(baseSize * (0.5 + progress * 1.5));
      break;
      
    case "rampDown":
      // Start fast, decelerate
      sliceSize = Math.ceil(baseSize * (2 - progress * 1.5));
      break;
      
    case "pulse":
      // Oscillating pattern
      if (logicDefinition.pulseConfig) {
        const { amplitude, frequency, phaseShift = 0 } = logicDefinition.pulseConfig;
        const wave = Math.sin((progress * frequency * 2 * Math.PI) + phaseShift);
        sliceSize = Math.ceil(baseSize * (1 + amplitude * wave));
      }
      break;
      
    case "naturalGrowth":
      // Sigmoid growth curve
      const growthRate = logicDefinition.growthRate || 10;
      const sigmoid = 1 / (1 + Math.exp(-growthRate * (progress - 0.5)));
      sliceSize = Math.ceil(baseSize * (0.2 + sigmoid * 1.6));
      break;
      
    case "viralSpike":
      // Exponential spike with decay
      const spike = Math.exp(-Math.pow(progress - 0.3, 2) / 0.02);
      sliceSize = Math.ceil(baseSize * (0.5 + spike * 2));
      break;
  }

  // Add noise if configured
  if (logicDefinition.noiseLevel) {
    const noise = (Math.random() - 0.5) * 2 * logicDefinition.noiseLevel;
    sliceSize = Math.ceil(sliceSize * (1 + noise));
  }

  // Apply bounds
  sliceSize = Math.max(minSliceSize, sliceSize);
  if (maxSliceSize) {
    sliceSize = Math.min(maxSliceSize, sliceSize);
  }

  return sliceSize;
}

// Dispatch a single slice
async function dispatchSlice(
  ctx: any,
  campaign: Doc<"dripFeedCampaigns">,
  slice: any,
  encryptedApiKey: string,
  apiKeyIv: string
) {
  const idempotencyKey = `${campaign._id}_${slice.serviceId}_${Date.now()}`;
  
  try {
    // Create dispatch log
    const logId = await ctx.runMutation(internal.scheduler.createDispatchLog, {
      campaignId: campaign._id,
      serviceId: slice.serviceId,
      quantity: slice.quantity,
      idempotencyKey,
    });

    // Call SMM API adapter
    const result = await ctx.runAction(internal.smm.placeOrder, {
      serviceId: slice.serviceId,
      link: slice.targetURL,
      quantity: slice.quantity,
      idempotencyKey,
      encryptedApiKey,
      apiKeyIv,
    });

    // Update dispatch log with result
    await ctx.runMutation(internal.scheduler.updateDispatchLog, {
      logId,
      status: result.success ? "success" : "failed",
      remoteOrderId: result.orderId,
      responsePayload: JSON.stringify(result),
      latencyMs: result.latencyMs,
    });

    return {
      success: result.success,
      serviceId: slice.serviceId,
      quantity: slice.quantity,
      orderId: result.orderId,
    };
  } catch (error) {
    // Log failure
    await ctx.runMutation(internal.scheduler.updateDispatchLog, {
      logId: null,
      campaignId: campaign._id,
      serviceId: slice.serviceId,
      status: "failed",
      errorMessage: error.message,
    });

    throw error;
  }
}

// Check if campaign is complete
async function checkAndCompleteCampaign(ctx: any, campaign: Doc<"dripFeedCampaigns">) {
  const allComplete = campaign.services.every(service => 
    service.deliveredQuantity + service.failedQuantity >= service.totalQuantity
  );

  if (allComplete) {
    await ctx.runMutation(internal.scheduler.completeCampaign, {
      campaignId: campaign._id,
    });
  }
}

// Internal queries
export const getActiveCampaigns = internalQuery({
  args: {},
  handler: async (ctx) => {
    const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;
    
    return await ctx.db
      .query("dripFeedCampaigns")
      .withIndex("by_status", (q) => q.eq("status", "active"))
      .filter((q) => 
        q.or(
          q.eq(q.field("lastProcessedAt"), undefined),
          q.lt(q.field("lastProcessedAt"), fiveMinutesAgo)
        )
      )
      .take(100);
  },
});

export const getDripStyle = internalQuery({
  args: { id: v.id("dripFeedStyles") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.id);
  },
});

export const getUser = internalQuery({
  args: { id: v.id("users") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.id);
  },
});

// Internal mutations
export const updateCampaignProgress = internalMutation({
  args: {
    campaignId: v.id("dripFeedCampaigns"),
    dispatchResults: v.array(v.any()),
    processingTimeMs: v.number(),
  },
  handler: async (ctx, args) => {
    const campaign = await ctx.db.get(args.campaignId);
    if (!campaign) return;

    const updatedServices = campaign.services.map(service => {
      const results = args.dispatchResults.filter(r => 
        r.serviceId === service.serviceId
      );
      
      const delivered = results.filter(r => r.success).reduce((sum, r) => sum + r.quantity, 0);
      const failed = results.filter(r => !r.success).reduce((sum, r) => sum + r.quantity, 0);

      return {
        ...service,
        deliveredQuantity: service.deliveredQuantity + delivered,
        failedQuantity: service.failedQuantity + failed,
        lastDispatchAt: Date.now(),
        nextDispatchAt: Date.now() + (5 * 60 * 1000), // Next dispatch in 5 minutes
      };
    });

    await ctx.db.patch(args.campaignId, {
      services: updatedServices,
      lastProcessedAt: Date.now(),
      retryCount: 0, // Reset retry count on successful processing
    });
  },
});

export const recordMetrics = internalMutation({
  args: {
    totalProcessed: v.number(),
    successful: v.number(),
    failed: v.number(),
    durationMs: v.number(),
  },
  handler: async (ctx, args) => {
    await ctx.db.insert("systemMetrics", {
      timestamp: Date.now(),
      metric: "scheduler.run",
      value: args.totalProcessed,
      labels: {
        status: "completed",
      },
      aggregationType: "counter",
    });

    await ctx.db.insert("systemMetrics", {
      timestamp: Date.now(),
      metric: "scheduler.duration_ms",
      value: args.durationMs,
      aggregationType: "histogram",
    });

    await ctx.db.insert("systemMetrics", {
      timestamp: Date.now(),
      metric: "scheduler.success_rate",
      value: args.totalProcessed > 0 ? args.successful / args.totalProcessed : 0,
      aggregationType: "gauge",
    });
  },
});

export const openCircuitBreaker = internalMutation({
  args: {
    campaignId: v.id("dripFeedCampaigns"),
    durationMinutes: v.number(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.campaignId, {
      circuitBreakerOpenUntil: Date.now() + (args.durationMinutes * 60 * 1000),
    });
  },
});

export const recordCampaignError = internalMutation({
  args: {
    campaignId: v.id("dripFeedCampaigns"),
    error: v.string(),
  },
  handler: async (ctx, args) => {
    const campaign = await ctx.db.get(args.campaignId);
    if (!campaign) return;

    await ctx.db.patch(args.campaignId, {
      errorMessage: args.error,
      retryCount: campaign.retryCount + 1,
      lastProcessedAt: Date.now(),
    });

    // If too many retries, pause the campaign
    if (campaign.retryCount >= 5) {
      await ctx.db.patch(args.campaignId, {
        status: "failed",
        failedAt: Date.now(),
      });

      // Create notification
      await ctx.db.insert("notifications", {
        userId: campaign.userId,
        type: "campaign_failed",
        severity: "error",
        title: "Campaign Failed",
        message: `Campaign "${campaign.name}" has failed after multiple retries: ${args.error}`,
        metadata: { campaignId: args.campaignId, error: args.error },
        isRead: false,
        isEmailSent: false,
        createdAt: Date.now(),
      });
    }
  },
});

export const createDispatchLog = internalMutation({
  args: {
    campaignId: v.id("dripFeedCampaigns"),
    serviceId: v.string(),
    quantity: v.number(),
    idempotencyKey: v.string(),
  },
  handler: async (ctx, args) => {
    return await ctx.db.insert("dispatchLogs", {
      campaignId: args.campaignId,
      serviceId: args.serviceId,
      quantity: args.quantity,
      idempotencyKey: args.idempotencyKey,
      status: "processing",
      attemptCount: 1,
      requestPayload: JSON.stringify({
        serviceId: args.serviceId,
        quantity: args.quantity,
      }),
      createdAt: Date.now(),
      processedAt: Date.now(),
    });
  },
});

export const updateDispatchLog = internalMutation({
  args: {
    logId: v.optional(v.id("dispatchLogs")),
    campaignId: v.optional(v.id("dripFeedCampaigns")),
    serviceId: v.optional(v.string()),
    status: v.union(v.literal("success"), v.literal("failed")),
    remoteOrderId: v.optional(v.string()),
    responsePayload: v.optional(v.string()),
    errorMessage: v.optional(v.string()),
    latencyMs: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    if (args.logId) {
      await ctx.db.patch(args.logId, {
        status: args.status,
        remoteOrderId: args.remoteOrderId,
        responsePayload: args.responsePayload,
        errorMessage: args.errorMessage,
        latencyMs: args.latencyMs,
        completedAt: Date.now(),
      });
    } else if (args.campaignId && args.serviceId) {
      // Create new log for failure
      await ctx.db.insert("dispatchLogs", {
        campaignId: args.campaignId,
        serviceId: args.serviceId,
        quantity: 0,
        idempotencyKey: `failed_${Date.now()}`,
        status: "failed",
        attemptCount: 1,
        requestPayload: "",
        errorMessage: args.errorMessage,
        createdAt: Date.now(),
      });
    }
  },
});

export const completeCampaign = internalMutation({
  args: {
    campaignId: v.id("dripFeedCampaigns"),
  },
  handler: async (ctx, args) => {
    const campaign = await ctx.db.get(args.campaignId);
    if (!campaign) return;

    await ctx.db.patch(args.campaignId, {
      status: "completed",
      completedAt: Date.now(),
    });

    // Create notification
    await ctx.db.insert("notifications", {
      userId: campaign.userId,
      type: "campaign_completed",
      severity: "info",
      title: "Campaign Completed",
      message: `Campaign "${campaign.name}" has been completed successfully`,
      metadata: { campaignId: args.campaignId },
      isRead: false,
      isEmailSent: false,
      createdAt: Date.now(),
    });
  },
});