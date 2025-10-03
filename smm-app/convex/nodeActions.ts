"use node";

import { v } from "convex/values";
import { action } from "./_generated/server";
import { internal } from "./_generated/api";
import { encryptApiKey } from "./smm";

export const updateApiKey = action({
  args: {
    apiKey: v.string(),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    // Validate API key by testing it
    const testResult = await ctx.runAction(internal.smm.getBalance, {
      encryptedApiKey: args.apiKey,
      apiKeyIv: "",
    });

    if (!testResult.success) {
      throw new Error("Invalid API key: " + testResult.error);
    }

    // Encrypt the API key
    const { encrypted, iv } = encryptApiKey(args.apiKey);

    // Update user
    await ctx.runMutation(internal.users.updateUserApiKey, {
      clerkId: identity.subject,
      encryptedApiKey: encrypted,
      apiKeyIv: iv,
    });

    return { success: true, balance: testResult.balance };
  },
});