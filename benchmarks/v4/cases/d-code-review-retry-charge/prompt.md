---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

small PR to stop the charge failures we saw during PayRail's incident last week (lots of timeouts + 503s from them). adds retries. lgtm? `chargeOrder` is called from our POST /checkout handler; the load balancer times requests out at 15s.

```diff
--- a/src/payments/charge.ts
+++ b/src/payments/charge.ts
@@ -1,18 +1,22 @@
 import { paymentsClient } from "./client";   // axios instance, baseURL https://api.payrail.com
+import { withRetry } from "../utils/retry";
 import { Order, ChargeResult, toChargeResult } from "./types";
 
 export async function chargeOrder(order: Order): Promise<ChargeResult> {
-  const res = await paymentsClient.post(
-    "/v1/charges",
-    {
-      amount: order.totalCents,
-      currency: order.currency,
-      customer: order.customerId,
-      payment_method: order.paymentMethodId,
-      description: `Order ${order.id}`,
-    },
-    { timeout: 5000 },
-  );
-  return toChargeResult(res.data);
+  return withRetry(async () => {
+    const res = await paymentsClient.post(
+      "/v1/charges",
+      {
+        amount: order.totalCents,
+        currency: order.currency,
+        customer: order.customerId,
+        payment_method: order.paymentMethodId,
+        description: `Order ${order.id}`,
+      },
+      { timeout: 5000 },
+    );
+    return toChargeResult(res.data);
+  }, { attempts: 4, delayMs: 500 });
 }
--- /dev/null
+++ b/src/utils/retry.ts
@@ -0,0 +1,16 @@
+const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
+
+export async function withRetry<T>(
+  fn: () => Promise<T>,
+  opts: { attempts: number; delayMs: number },
+): Promise<T> {
+  let lastErr: unknown;
+  for (let i = 0; i < opts.attempts; i++) {
+    try {
+      return await fn();
+    } catch (err) {
+      lastErr = err;
+      await sleep(opts.delayMs);
+    }
+  }
+  throw lastErr;
+}
```
