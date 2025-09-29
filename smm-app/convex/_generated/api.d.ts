/* eslint-disable */
/**
 * Generated `api` utility.
 *
 * THIS CODE IS AUTOMATICALLY GENERATED.
 *
 * To regenerate, run `npx convex dev`.
 * @module
 */

import type {
  ApiFromModules,
  FilterApi,
  FunctionReference,
} from "convex/server";
import type * as campaigns from "../campaigns.js";
import type * as dripStyles from "../dripStyles.js";
import type * as metrics from "../metrics.js";
import type * as nodeActions from "../nodeActions.js";
import type * as notifications from "../notifications.js";
import type * as packages from "../packages.js";
import type * as scheduler from "../scheduler.js";
import type * as smm from "../smm.js";
import type * as users from "../users.js";

/**
 * A utility for referencing Convex functions in your app's API.
 *
 * Usage:
 * ```js
 * const myFunctionReference = api.myModule.myFunction;
 * ```
 */
declare const fullApi: ApiFromModules<{
  campaigns: typeof campaigns;
  dripStyles: typeof dripStyles;
  metrics: typeof metrics;
  nodeActions: typeof nodeActions;
  notifications: typeof notifications;
  packages: typeof packages;
  scheduler: typeof scheduler;
  smm: typeof smm;
  users: typeof users;
}>;
export declare const api: FilterApi<
  typeof fullApi,
  FunctionReference<any, "public">
>;
export declare const internal: FilterApi<
  typeof fullApi,
  FunctionReference<any, "internal">
>;
