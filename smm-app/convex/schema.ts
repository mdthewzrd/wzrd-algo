import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    clerkId: v.string(),
    name: v.string(),
    email: v.string(),
    encryptedApiKey: v.optional(v.string()),
    apiKeyIv: v.optional(v.string()),
    createdAt: v.number(),
    lastActiveAt: v.number(),
    settings: v.optional(v.object({
      notificationEmail: v.optional(v.boolean()),
      notificationInApp: v.optional(v.boolean()),
      defaultDripStyleId: v.optional(v.id("dripFeedStyles")),
      timezone: v.optional(v.string()),
    })),
  })
    .index("by_clerk_id", ["clerkId"])
    .index("by_email", ["email"]),

  packages: defineTable({
    userId: v.id("users"),
    name: v.string(),
    description: v.optional(v.string()),
    services: v.array(v.object({
      serviceId: v.string(),
      name: v.string(),
      defaultQuantity: v.optional(v.number()),
      minQuantity: v.number(),
      maxQuantity: v.number(),
      pricePerThousand: v.number(),
    })),
    isActive: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number(),
    usageCount: v.number(),
    lastUsedAt: v.optional(v.number()),
  })
    .index("by_user", ["userId"])
    .index("by_user_active", ["userId", "isActive"]),

  dripFeedStyles: defineTable({
    name: v.string(),
    description: v.string(),
    algorithm: v.union(
      v.literal("uniform"),
      v.literal("rampUp"),
      v.literal("rampDown"),
      v.literal("pulse"),
      v.literal("naturalGrowth"),
      v.literal("viralSpike")
    ),
    logicDefinition: v.object({
      intervalMinutes: v.number(),
      steps: v.number(),
      minSliceSize: v.number(),
      maxSliceSize: v.optional(v.number()),
      pulseConfig: v.optional(v.object({
        amplitude: v.number(),
        frequency: v.number(),
        phaseShift: v.optional(v.number()),
      })),
      growthRate: v.optional(v.number()),
      decayRate: v.optional(v.number()),
      noiseLevel: v.optional(v.number()),
    }),
    isDefault: v.boolean(),
    createdAt: v.number(),
  })
    .index("by_default", ["isDefault"]),

  dripFeedCampaigns: defineTable({
    userId: v.id("users"),
    name: v.string(),
    targetURL: v.string(),
    status: v.union(
      v.literal("draft"),
      v.literal("active"),
      v.literal("paused"),
      v.literal("completed"),
      v.literal("failed"),
      v.literal("cancelled")
    ),
    dripFeedStyleId: v.id("dripFeedStyles"),
    packageId: v.optional(v.id("packages")),
    services: v.array(v.object({
      serviceId: v.string(),
      name: v.string(),
      totalQuantity: v.number(),
      deliveredQuantity: v.number(),
      failedQuantity: v.number(),
      pricePerThousand: v.number(),
      lastDispatchAt: v.optional(v.number()),
      nextDispatchAt: v.optional(v.number()),
    })),
    totalCost: v.number(),
    spentCost: v.number(),
    createdAt: v.number(),
    startedAt: v.optional(v.number()),
    lastProcessedAt: v.optional(v.number()),
    completedAt: v.optional(v.number()),
    pausedAt: v.optional(v.number()),
    failedAt: v.optional(v.number()),
    errorMessage: v.optional(v.string()),
    retryCount: v.number(),
    circuitBreakerOpenUntil: v.optional(v.number()),
    metadata: v.optional(v.object({
      clientName: v.optional(v.string()),
      projectName: v.optional(v.string()),
      tags: v.optional(v.array(v.string())),
      notes: v.optional(v.string()),
    })),
  })
    .index("by_user", ["userId"])
    .index("by_status", ["status"])
    .index("by_user_and_status", ["userId", "status"])
    .index("by_next_process", ["status", "lastProcessedAt"]),

  dispatchLogs: defineTable({
    campaignId: v.id("dripFeedCampaigns"),
    serviceId: v.string(),
    quantity: v.number(),
    idempotencyKey: v.string(),
    remoteOrderId: v.optional(v.string()),
    status: v.union(
      v.literal("pending"),
      v.literal("processing"),
      v.literal("success"),
      v.literal("failed"),
      v.literal("retrying")
    ),
    attemptCount: v.number(),
    requestPayload: v.string(),
    responsePayload: v.optional(v.string()),
    errorMessage: v.optional(v.string()),
    latencyMs: v.optional(v.number()),
    createdAt: v.number(),
    processedAt: v.optional(v.number()),
    completedAt: v.optional(v.number()),
  })
    .index("by_campaign", ["campaignId"])
    .index("by_idempotency", ["idempotencyKey"])
    .index("by_remote_order", ["remoteOrderId"])
    .index("by_status", ["status"])
    .index("by_campaign_and_status", ["campaignId", "status"]),

  notifications: defineTable({
    userId: v.id("users"),
    type: v.union(
      v.literal("campaign_started"),
      v.literal("campaign_completed"),
      v.literal("campaign_failed"),
      v.literal("dispatch_failed"),
      v.literal("low_balance"),
      v.literal("api_key_expiring"),
      v.literal("system_maintenance")
    ),
    severity: v.union(
      v.literal("info"),
      v.literal("warning"),
      v.literal("error"),
      v.literal("critical")
    ),
    title: v.string(),
    message: v.string(),
    metadata: v.optional(v.any()),
    isRead: v.boolean(),
    isEmailSent: v.boolean(),
    createdAt: v.number(),
    readAt: v.optional(v.number()),
  })
    .index("by_user", ["userId"])
    .index("by_user_unread", ["userId", "isRead"])
    .index("by_created", ["createdAt"]),

  systemMetrics: defineTable({
    timestamp: v.number(),
    metric: v.string(),
    value: v.number(),
    labels: v.optional(v.object({
      campaignId: v.optional(v.id("dripFeedCampaigns")),
      userId: v.optional(v.id("users")),
      serviceId: v.optional(v.string()),
      status: v.optional(v.string()),
    })),
    aggregationType: v.union(
      v.literal("counter"),
      v.literal("gauge"),
      v.literal("histogram"),
      v.literal("summary")
    ),
  })
    .index("by_metric_time", ["metric", "timestamp"])
    .index("by_campaign", ["labels.campaignId"]),

  auditLogs: defineTable({
    userId: v.id("users"),
    action: v.string(),
    entityType: v.string(),
    entityId: v.optional(v.string()),
    changes: v.optional(v.string()),
    ipAddress: v.optional(v.string()),
    userAgent: v.optional(v.string()),
    timestamp: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_entity", ["entityType", "entityId"])
    .index("by_timestamp", ["timestamp"]),
});