import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { Doc, Id } from "./_generated/dataModel";

export const getPackages = query({
  args: {
    includeInactive: v.optional(v.boolean()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
    
    if (!user) throw new Error("User not found");

    let packages;
    if (args.includeInactive) {
      packages = await ctx.db
        .query("packages")
        .withIndex("by_user", (q) => q.eq("userId", user._id))
        .collect();
    } else {
      packages = await ctx.db
        .query("packages")
        .withIndex("by_user_active", (q) => 
          q.eq("userId", user._id).eq("isActive", true)
        )
        .collect();
    }

    return packages.sort((a, b) => b.updatedAt - a.updatedAt);
  },
});

export const getPackageById = query({
  args: { id: v.id("packages") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const pkg = await ctx.db.get(args.id);
    if (!pkg) throw new Error("Package not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || pkg.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    return pkg;
  },
});

export const createPackage = mutation({
  args: {
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
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
    
    if (!user) throw new Error("User not found");

    // Validate services
    if (args.services.length === 0) {
      throw new Error("Package must contain at least one service");
    }

    for (const service of args.services) {
      if (service.minQuantity < 0) {
        throw new Error("Minimum quantity cannot be negative");
      }
      if (service.maxQuantity < service.minQuantity) {
        throw new Error("Maximum quantity must be greater than minimum");
      }
      if (service.pricePerThousand < 0) {
        throw new Error("Price cannot be negative");
      }
    }

    const packageId = await ctx.db.insert("packages", {
      userId: user._id,
      name: args.name,
      description: args.description,
      services: args.services,
      isActive: true,
      createdAt: Date.now(),
      updatedAt: Date.now(),
      usageCount: 0,
    });

    // Log audit
    await ctx.db.insert("auditLogs", {
      userId: user._id,
      action: "package.created",
      entityType: "package",
      entityId: packageId,
      changes: JSON.stringify(args),
      timestamp: Date.now(),
    });

    return packageId;
  },
});

export const updatePackage = mutation({
  args: {
    id: v.id("packages"),
    name: v.optional(v.string()),
    description: v.optional(v.string()),
    services: v.optional(v.array(v.object({
      serviceId: v.string(),
      name: v.string(),
      defaultQuantity: v.optional(v.number()),
      minQuantity: v.number(),
      maxQuantity: v.number(),
      pricePerThousand: v.number(),
    }))),
    isActive: v.optional(v.boolean()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const pkg = await ctx.db.get(args.id);
    if (!pkg) throw new Error("Package not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || pkg.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    const updates: any = {
      updatedAt: Date.now(),
    };

    if (args.name !== undefined) updates.name = args.name;
    if (args.description !== undefined) updates.description = args.description;
    if (args.services !== undefined) {
      // Validate services
      for (const service of args.services) {
        if (service.minQuantity < 0) {
          throw new Error("Minimum quantity cannot be negative");
        }
        if (service.maxQuantity < service.minQuantity) {
          throw new Error("Maximum quantity must be greater than minimum");
        }
        if (service.pricePerThousand < 0) {
          throw new Error("Price cannot be negative");
        }
      }
      updates.services = args.services;
    }
    if (args.isActive !== undefined) updates.isActive = args.isActive;

    await ctx.db.patch(args.id, updates);

    // Log audit
    await ctx.db.insert("auditLogs", {
      userId: user._id,
      action: "package.updated",
      entityType: "package",
      entityId: args.id,
      changes: JSON.stringify(updates),
      timestamp: Date.now(),
    });

    return { success: true };
  },
});

export const deletePackage = mutation({
  args: { id: v.id("packages") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const pkg = await ctx.db.get(args.id);
    if (!pkg) throw new Error("Package not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || pkg.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    // Check if package is in use by any active campaigns
    const activeCampaigns = await ctx.db
      .query("dripFeedCampaigns")
      .withIndex("by_user_and_status", (q) => 
        q.eq("userId", user._id).eq("status", "active")
      )
      .filter((q) => q.eq(q.field("packageId"), args.id))
      .first();

    if (activeCampaigns) {
      throw new Error("Cannot delete package that is in use by active campaigns");
    }

    await ctx.db.delete(args.id);

    // Log audit
    await ctx.db.insert("auditLogs", {
      userId: user._id,
      action: "package.deleted",
      entityType: "package",
      entityId: args.id,
      timestamp: Date.now(),
    });

    return { success: true };
  },
});

export const duplicatePackage = mutation({
  args: { id: v.id("packages") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const pkg = await ctx.db.get(args.id);
    if (!pkg) throw new Error("Package not found");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user || pkg.userId !== user._id) {
      throw new Error("Unauthorized");
    }

    const newPackageId = await ctx.db.insert("packages", {
      userId: user._id,
      name: `${pkg.name} (Copy)`,
      description: pkg.description,
      services: pkg.services,
      isActive: true,
      createdAt: Date.now(),
      updatedAt: Date.now(),
      usageCount: 0,
    });

    return newPackageId;
  },
});

export const recordPackageUsage = mutation({
  args: { 
    id: v.id("packages"),
    campaignId: v.id("dripFeedCampaigns"),
  },
  handler: async (ctx, args) => {
    const pkg = await ctx.db.get(args.id);
    if (!pkg) return;

    await ctx.db.patch(args.id, {
      usageCount: pkg.usageCount + 1,
      lastUsedAt: Date.now(),
      updatedAt: Date.now(),
    });
  },
});