import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const getDripStyles = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db
      .query("dripFeedStyles")
      .order("asc")
      .collect();
  },
});

export const getDripStyleById = query({
  args: { id: v.id("dripFeedStyles") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.id);
  },
});

export const createDripStyle = mutation({
  args: {
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
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
    
    if (!user) throw new Error("User not found");

    // Validate logic definition
    if (args.logicDefinition.intervalMinutes < 1) {
      throw new Error("Interval must be at least 1 minute");
    }
    if (args.logicDefinition.steps < 1) {
      throw new Error("Steps must be at least 1");
    }
    if (args.logicDefinition.minSliceSize < 1) {
      throw new Error("Minimum slice size must be at least 1");
    }
    if (args.logicDefinition.maxSliceSize && 
        args.logicDefinition.maxSliceSize < args.logicDefinition.minSliceSize) {
      throw new Error("Maximum slice size must be greater than minimum");
    }

    const styleId = await ctx.db.insert("dripFeedStyles", {
      ...args,
      isDefault: false,
      createdAt: Date.now(),
    });

    // Log audit
    await ctx.db.insert("auditLogs", {
      userId: user._id,
      action: "drip_style.created",
      entityType: "dripFeedStyles",
      entityId: styleId,
      changes: JSON.stringify(args),
      timestamp: Date.now(),
    });

    return styleId;
  },
});

export const updateDripStyle = mutation({
  args: {
    id: v.id("dripFeedStyles"),
    name: v.optional(v.string()),
    description: v.optional(v.string()),
    logicDefinition: v.optional(v.object({
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
    })),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const style = await ctx.db.get(args.id);
    if (!style) throw new Error("Drip style not found");

    if (style.isDefault) {
      throw new Error("Cannot modify default drip styles");
    }

    const updates: any = {};
    if (args.name !== undefined) updates.name = args.name;
    if (args.description !== undefined) updates.description = args.description;
    if (args.logicDefinition !== undefined) {
      // Validate logic definition
      if (args.logicDefinition.intervalMinutes < 1) {
        throw new Error("Interval must be at least 1 minute");
      }
      if (args.logicDefinition.steps < 1) {
        throw new Error("Steps must be at least 1");
      }
      if (args.logicDefinition.minSliceSize < 1) {
        throw new Error("Minimum slice size must be at least 1");
      }
      if (args.logicDefinition.maxSliceSize && 
          args.logicDefinition.maxSliceSize < args.logicDefinition.minSliceSize) {
        throw new Error("Maximum slice size must be greater than minimum");
      }
      updates.logicDefinition = args.logicDefinition;
    }

    await ctx.db.patch(args.id, updates);

    return { success: true };
  },
});

export const deleteDripStyle = mutation({
  args: { id: v.id("dripFeedStyles") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const style = await ctx.db.get(args.id);
    if (!style) throw new Error("Drip style not found");

    if (style.isDefault) {
      throw new Error("Cannot delete default drip styles");
    }

    // Check if style is in use by any campaigns
    const campaignsUsingStyle = await ctx.db
      .query("dripFeedCampaigns")
      .filter((q) => q.eq(q.field("dripFeedStyleId"), args.id))
      .first();

    if (campaignsUsingStyle) {
      throw new Error("Cannot delete drip style that is in use by campaigns");
    }

    await ctx.db.delete(args.id);

    return { success: true };
  },
});

export const previewDripPattern = query({
  args: {
    styleId: v.id("dripFeedStyles"),
    totalQuantity: v.number(),
    duration: v.optional(v.number()), // in hours
  },
  handler: async (ctx, args) => {
    const style = await ctx.db.get(args.styleId);
    if (!style) throw new Error("Drip style not found");

    const duration = args.duration || 24; // Default 24 hours
    const durationMs = duration * 60 * 60 * 1000;
    const { intervalMinutes, steps } = style.logicDefinition;
    
    const points = [];
    const intervalMs = intervalMinutes * 60 * 1000;
    const totalSteps = Math.min(steps, Math.floor(durationMs / intervalMs));
    
    for (let i = 0; i < totalSteps; i++) {
      const progress = i / (totalSteps - 1);
      const sliceSize = calculatePreviewSliceSize(
        args.totalQuantity,
        totalSteps,
        progress,
        style
      );
      
      points.push({
        time: i * intervalMs,
        quantity: sliceSize,
        cumulativeQuantity: points.reduce((sum, p) => sum + p.quantity, 0) + sliceSize,
      });
    }

    return {
      pattern: points,
      totalSteps,
      intervalMinutes,
      estimatedDuration: totalSteps * intervalMinutes,
    };
  },
});

function calculatePreviewSliceSize(
  totalQuantity: number,
  totalSteps: number,
  progress: number,
  style: any
): number {
  const { algorithm, logicDefinition } = style;
  const { minSliceSize, maxSliceSize } = logicDefinition;
  
  const baseSize = Math.ceil(totalQuantity / totalSteps);
  let sliceSize = baseSize;

  switch (algorithm) {
    case "uniform":
      sliceSize = baseSize;
      break;
      
    case "rampUp":
      sliceSize = Math.ceil(baseSize * (0.5 + progress * 1.5));
      break;
      
    case "rampDown":
      sliceSize = Math.ceil(baseSize * (2 - progress * 1.5));
      break;
      
    case "pulse":
      if (logicDefinition.pulseConfig) {
        const { amplitude, frequency, phaseShift = 0 } = logicDefinition.pulseConfig;
        const wave = Math.sin((progress * frequency * 2 * Math.PI) + phaseShift);
        sliceSize = Math.ceil(baseSize * (1 + amplitude * wave));
      }
      break;
      
    case "naturalGrowth":
      const growthRate = logicDefinition.growthRate || 10;
      const sigmoid = 1 / (1 + Math.exp(-growthRate * (progress - 0.5)));
      sliceSize = Math.ceil(baseSize * (0.2 + sigmoid * 1.6));
      break;
      
    case "viralSpike":
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