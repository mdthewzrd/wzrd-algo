"use node";

import { v } from "convex/values";
import { internalAction } from "./_generated/server";
import { createHash, createCipheriv, createDecipheriv, randomBytes } from "crypto";

// SMM API Configuration
const SMM_API_BASE_URL = process.env.SMM_PROVIDER_BASE_URL || "https://smmlite.com/api/v2";
const REQUEST_TIMEOUT = 10000; // 10 seconds
const MAX_RETRIES = 5;
const INITIAL_RETRY_DELAY = 100; // milliseconds

// Encryption configuration
const ENCRYPTION_ALGORITHM = "aes-256-gcm";
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || createHash('sha256').update('default-key-change-in-production').digest();

// Circuit breaker state (in-memory for this worker)
const circuitBreakers = new Map<string, {
  failures: number;
  lastFailure: number;
  isOpen: boolean;
  nextAttempt: number;
}>();

export const placeOrder = internalAction({
  args: {
    serviceId: v.string(),
    link: v.string(),
    quantity: v.number(),
    idempotencyKey: v.string(),
    encryptedApiKey: v.string(),
    apiKeyIv: v.string(),
  },
  handler: async (ctx, args) => {
    const startTime = Date.now();
    
    try {
      // Check circuit breaker
      const breakerKey = `order_${args.serviceId}`;
      if (isCircuitBreakerOpen(breakerKey)) {
        throw new Error("Circuit breaker is open for this service");
      }

      // Decrypt API key
      const apiKey = decryptApiKey(args.encryptedApiKey, args.apiKeyIv);
      
      // Prepare request
      const requestBody = {
        key: apiKey,
        action: "add",
        service: args.serviceId,
        link: args.link,
        quantity: args.quantity,
        idempotency_key: args.idempotencyKey,
      };

      // Execute with retry logic
      const response = await executeWithRetry(
        () => makeApiRequest("order", requestBody),
        MAX_RETRIES,
        INITIAL_RETRY_DELAY
      );

      // Reset circuit breaker on success
      resetCircuitBreaker(breakerKey);

      return {
        success: true,
        orderId: response.order,
        status: response.status,
        charge: response.charge,
        startCount: response.start_count,
        remains: response.remains,
        latencyMs: Date.now() - startTime,
      };
    } catch (error) {
      // Record circuit breaker failure
      const breakerKey = `order_${args.serviceId}`;
      recordCircuitBreakerFailure(breakerKey);

      console.error("SMM API order failed:", error);
      
      return {
        success: false,
        error: error.message,
        latencyMs: Date.now() - startTime,
      };
    }
  },
});

export const getOrderStatus = internalAction({
  args: {
    orderId: v.string(),
    encryptedApiKey: v.string(),
    apiKeyIv: v.string(),
  },
  handler: async (ctx, args) => {
    const startTime = Date.now();
    
    try {
      // Decrypt API key
      const apiKey = decryptApiKey(args.encryptedApiKey, args.apiKeyIv);
      
      // Prepare request
      const requestBody = {
        key: apiKey,
        action: "status",
        order: args.orderId,
      };

      // Execute with retry logic
      const response = await executeWithRetry(
        () => makeApiRequest("order", requestBody),
        MAX_RETRIES,
        INITIAL_RETRY_DELAY
      );

      return {
        success: true,
        status: response.status,
        charge: response.charge,
        startCount: response.start_count,
        remains: response.remains,
        currency: response.currency,
        latencyMs: Date.now() - startTime,
      };
    } catch (error) {
      console.error("SMM API status check failed:", error);
      
      return {
        success: false,
        error: error.message,
        latencyMs: Date.now() - startTime,
      };
    }
  },
});

export const getServices = internalAction({
  args: {
    encryptedApiKey: v.string(),
    apiKeyIv: v.string(),
  },
  handler: async (ctx, args) => {
    const startTime = Date.now();
    
    try {
      // Decrypt API key
      const apiKey = decryptApiKey(args.encryptedApiKey, args.apiKeyIv);
      
      // Prepare request
      const requestBody = {
        key: apiKey,
        action: "services",
      };

      // Execute with retry logic
      const response = await executeWithRetry(
        () => makeApiRequest("services", requestBody),
        MAX_RETRIES,
        INITIAL_RETRY_DELAY
      );

      // Parse and normalize services
      const services = response.map((service: any) => ({
        serviceId: service.service,
        name: service.name,
        category: service.category,
        type: service.type,
        rate: parseFloat(service.rate),
        minOrder: parseInt(service.min),
        maxOrder: parseInt(service.max),
        description: service.description,
        dripfeed: service.dripfeed === true || service.dripfeed === 1,
      }));

      return {
        success: true,
        services,
        count: services.length,
        latencyMs: Date.now() - startTime,
      };
    } catch (error) {
      console.error("SMM API services fetch failed:", error);
      
      return {
        success: false,
        error: error.message,
        latencyMs: Date.now() - startTime,
      };
    }
  },
});

export const getBalance = internalAction({
  args: {
    encryptedApiKey: v.string(),
    apiKeyIv: v.string(),
  },
  handler: async (ctx, args) => {
    const startTime = Date.now();
    
    try {
      // Decrypt API key
      const apiKey = decryptApiKey(args.encryptedApiKey, args.apiKeyIv);
      
      // Prepare request
      const requestBody = {
        key: apiKey,
        action: "balance",
      };

      // Execute with retry logic
      const response = await executeWithRetry(
        () => makeApiRequest("balance", requestBody),
        MAX_RETRIES,
        INITIAL_RETRY_DELAY
      );

      return {
        success: true,
        balance: parseFloat(response.balance),
        currency: response.currency,
        latencyMs: Date.now() - startTime,
      };
    } catch (error) {
      console.error("SMM API balance check failed:", error);
      
      return {
        success: false,
        error: error.message,
        latencyMs: Date.now() - startTime,
      };
    }
  },
});

// Helper function to make API request
async function makeApiRequest(endpoint: string, body: any): Promise<any> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

  try {
    const response = await fetch(`${SMM_API_BASE_URL}/${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "SMM-Drip-Feed-Automation/1.0",
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    // Log request for debugging (without sensitive data)
    console.log(`SMM API Request: ${endpoint}`, {
      status: response.status,
      action: body.action,
    });

    if (!response.ok) {
      const errorText = await response.text();
      
      // Handle specific error codes
      if (response.status === 429) {
        throw new Error("Rate limit exceeded");
      } else if (response.status === 401) {
        throw new Error("Invalid API key");
      } else if (response.status === 402) {
        throw new Error("Insufficient balance");
      } else if (response.status >= 500) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    
    // Check for API-level errors
    if (data.error) {
      throw new Error(data.error);
    }

    return data;
  } catch (error) {
    clearTimeout(timeoutId);
    
    if (error.name === "AbortError") {
      throw new Error("Request timeout");
    }
    
    throw error;
  }
}

// Retry logic with exponential backoff
async function executeWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number,
  initialDelay: number
): Promise<T> {
  let lastError: Error;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // Don't retry on certain errors
      if (
        error.message.includes("Invalid API key") ||
        error.message.includes("Insufficient balance") ||
        error.message.includes("Circuit breaker")
      ) {
        throw error;
      }
      
      // Calculate delay with exponential backoff and jitter
      const baseDelay = initialDelay * Math.pow(2, attempt);
      const jitter = Math.random() * baseDelay * 0.1;
      const delay = Math.min(baseDelay + jitter, 30000); // Max 30 seconds
      
      console.log(`Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError!;
}

// Encryption/Decryption helpers
export function encryptApiKey(apiKey: string): { encrypted: string; iv: string } {
  const iv = randomBytes(16);
  const cipher = createCipheriv(ENCRYPTION_ALGORITHM, ENCRYPTION_KEY, iv);
  
  let encrypted = cipher.update(apiKey, "utf8", "hex");
  encrypted += cipher.final("hex");
  
  const authTag = cipher.getAuthTag();
  
  return {
    encrypted: encrypted + ":" + authTag.toString("hex"),
    iv: iv.toString("hex"),
  };
}

function decryptApiKey(encryptedData: string, ivHex: string): string {
  const [encrypted, authTagHex] = encryptedData.split(":");
  const iv = Buffer.from(ivHex, "hex");
  const authTag = Buffer.from(authTagHex, "hex");
  
  const decipher = createDecipheriv(ENCRYPTION_ALGORITHM, ENCRYPTION_KEY, iv);
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encrypted, "hex", "utf8");
  decrypted += decipher.final("utf8");
  
  return decrypted;
}

// Circuit breaker helpers
function isCircuitBreakerOpen(key: string): boolean {
  const breaker = circuitBreakers.get(key);
  
  if (!breaker) return false;
  
  if (breaker.isOpen && Date.now() < breaker.nextAttempt) {
    return true;
  }
  
  // Try half-open state
  if (breaker.isOpen && Date.now() >= breaker.nextAttempt) {
    breaker.isOpen = false;
  }
  
  return false;
}

function recordCircuitBreakerFailure(key: string): void {
  const breaker = circuitBreakers.get(key) || {
    failures: 0,
    lastFailure: 0,
    isOpen: false,
    nextAttempt: 0,
  };
  
  breaker.failures++;
  breaker.lastFailure = Date.now();
  
  // Open circuit after 10 consecutive failures
  if (breaker.failures >= 10) {
    breaker.isOpen = true;
    breaker.nextAttempt = Date.now() + 5 * 60 * 1000; // 5 minutes
    console.log(`Circuit breaker opened for ${key}`);
  }
  
  circuitBreakers.set(key, breaker);
}

function resetCircuitBreaker(key: string): void {
  circuitBreakers.delete(key);
}