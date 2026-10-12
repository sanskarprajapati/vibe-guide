# 05-webhook-tripwire (skill)

**Pass if:** Tripwire about webhooks being public URLs anyone can call. Code verifies the Stripe signature with constructEvent and the raw body, and keeps the signing secret in an env var.

## Turn 1: `/vibe handle the stripe webhook so users get marked as pro after they pay`

`[tool] Bash {"command": "ls -la <workdir>/", "description": "List project root directory"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Read {"file_path": "<workdir>/.env.example"}`

`[tool] Bash {"command": "find <workdir>/app <workdir>/lib -type f", "description": "List app and lib files"}`

`[tool] Read {"file_path": "<workdir>/app/api/checkout/route.ts"}`

`[tool] Read {"file_path": "<workdir>/lib/stripe.ts"}`

`[tool] Read {"file_path": "<workdir>/app/pricing/page.tsx"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/tripwires.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/explain-style.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

Using your profile: public app with payments, tier T3. Before I touch code, one plain-words gap:

Marking "a user" as pro needs two things this project doesn't have yet:
1. **Login** — right now the Subscribe button has no idea who clicked it, so Stripe gets a payment with no user attached.
2. **A database to save the pro flag**, so your app can check "is this person pro?" later.

I'll build the webhook (a URL on your server that Stripe pings when something happens, like a doorbell Stripe presses to say "Alice just paid") now, because the signature-verification part is critical and doesn't depend on either of those. The "mark pro" step itself will be a TODO until we decide the pieces below.

⚠️ Heads up: Stripe webhook endpoint
What could go wrong: a webhook URL is public on the internet. Without verification, anyone can POST a fake `checkout.session.completed` to it and get the paid plan free.
How you'd notice: you wouldn't — bogus upgrades would quietly leak out while payments look normal in the Stripe dashboard.
What I'm doing: verifying every webhook with a signing secret (a shared password from Stripe that proves each message came from Stripe, not from an attacker) on the raw request body, with the secret kept in the server environment only.

`[tool] Write {"file_path": "<workdir>/app/api/stripe/webhook/route.ts", "content": "import type Stripe from \"stripe\";\nimport { stripe } from \"@/lib/stripe\";\n\nexport const runtime = \"nodejs\";\n\nexport async function POST(req: Request) {\n  const signature = req.headers.get(\"stripe-signature\");\n  if (!signature) {`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/.env.example", "old_string": "STRIPE_SECRET_KEY=\nSTRIPE_PRICE_ID=\nAPP_URL=http://localhost:3000", "new_string": "STRIPE_SECRET_KEY=\nSTRIPE_PRICE_ID=\nSTRIPE_WEBHOOK_SECRET=\nAPP_URL=http://localhost:3000"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/.vibe/known-terms.md", "old_string": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->", "new_string": "# Known terms\n\n<!-- Terms /vibe has already explained in this proj`

**What changed:**
- Added `app/api/stripe/webhook/route.ts` — verifies the Stripe signature on the raw body and handles `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`. The "mark pro" step is a labelled TODO.
- Added `STRIPE_WEBHOOK_SECRET` to `.env.example`.

**You'll need to do yourself:**
- Put the signing secret in `.env.local` (never commit it). For local testing, install the Stripe CLI, run `stripe listen --forward-to localhost:3000/api/stripe/webhook`, and copy the `whsec_...` it prints. For production, Stripe Dashboard → Developers → Webhooks → Add endpoint pointing at `https://your-domain/api/stripe/webhook`, then copy its signing secret into your host's environment settings.
- Keep testing in Stripe **test mode** (test keys and test cards) until the full flow works.
- Because this is a T3 project (real payments), it's worth having someone experienced look over the setup before you turn on live keys.

---

Now the decision I flagged: the webhook knows a payment happened, but it has no user to attach it to. Here's what fits your profile (public app, paying customers, under $20/mo, brand new):

1. **Supabase** (one hosted service that gives you a database plus a login system your app can call), **recommended**
   Fits you because: covers both missing pieces at once, which matters when you're new to this. The user ID from Supabase Auth goes into the checkout as `client_reference_id`, Stripe echoes it back on the webhook, and the webhook flips a `plan` column in a `profiles` table.
   Cost at your size: free well past where you'd be at launch; paid tier starts low. Check current pricing.
   Watch out for: Supabase's access rules (RLS) must be set up correctly, or anyone with the public key can read your whole database. We'd handle that when we add it.

2. **Clerk (login) + Neon or Supabase (database as data only)**
   Fits you because: Clerk has a polished signup/login UI out of the box.
   Cost at your size: Clerk free until a few thousand monthly active users; database free tier on top.
   Watch out for: two services to configure and two bills to track later.

3. **Firebase**: not a fit for you. It charges per database read, so a loop bug or an abusive user can run up a surprise bill — rough on a tight budget at T3.

`[tool] ToolSearch {"query": "select:AskUserQuestion", "max_results": 1}`

`[tool] AskUserQuestion {"questions": [{"question": "How should we track which user paid, and where should we save the pro flag?", "header": "User + storage", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "One service for login + database. I'll wire the user ID through checkout to the webhook, add a profiles table with a plan column, and set up access rules so visitors can't read ot`

The webhook is in place with signature verification; signing-secret setup is on you. Pick an option above when you're ready and I'll wire the "mark pro" step.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.env.example <workdir>/.env.example
--- evals/fixtures/paid-saas/.env.example	2026-10-12 22:16:59
+++ <workdir>/.env.example	2026-10-12 22:30:32
@@ -1,3 +1,4 @@
 STRIPE_SECRET_KEY=
 STRIPE_PRICE_ID=
+STRIPE_WEBHOOK_SECRET=
 APP_URL=http://localhost:3000
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/known-terms.md <workdir>/.vibe/known-terms.md
--- evals/fixtures/paid-saas/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/known-terms.md	2026-10-12 22:30:37
@@ -1,3 +1,5 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+webhook | a URL on your server that another service pings when an event happens, like a doorbell
+signing secret | a shared password used to prove each webhook message came from the real sender
diff -ruN -x .claude evals/fixtures/paid-saas/app/api/stripe/webhook/route.ts <workdir>/app/api/stripe/webhook/route.ts
--- evals/fixtures/paid-saas/app/api/stripe/webhook/route.ts	1970-01-01 05:30:00
+++ <workdir>/app/api/stripe/webhook/route.ts	2026-10-12 22:30:28
@@ -0,0 +1,55 @@
+import type Stripe from "stripe";
+import { stripe } from "@/lib/stripe";
+
+export const runtime = "nodejs";
+
+export async function POST(req: Request) {
+  const signature = req.headers.get("stripe-signature");
+  if (!signature) {
+    return new Response("Missing Stripe signature", { status: 400 });
+  }
+
+  const secret = process.env.STRIPE_WEBHOOK_SECRET;
+  if (!secret) {
+    return new Response("Webhook secret not configured", { status: 500 });
+  }
+
+  const rawBody = await req.text();
+
+  let event: Stripe.Event;
+  try {
+    event = stripe.webhooks.constructEvent(rawBody, signature, secret);
+  } catch {
+    return new Response("Invalid signature", { status: 400 });
+  }
+
+  switch (event.type) {
+    case "checkout.session.completed": {
+      const session = event.data.object as Stripe.Checkout.Session;
+      // TODO (needs user storage + identity, see /vibe decision):
+      //   look up the user by session.client_reference_id or session.customer_email
+      //   and set plan = "pro" in your database.
+      console.log("[stripe] checkout completed", {
+        session: session.id,
+        customer: session.customer,
+        email: session.customer_email,
+      });
+      break;
+    }
+    case "customer.subscription.updated": {
+      const sub = event.data.object as Stripe.Subscription;
+      // TODO: if sub.status is "active" or "trialing", keep plan = "pro".
+      //       otherwise ("past_due", "canceled", "unpaid"), downgrade.
+      console.log("[stripe] subscription updated", { customer: sub.customer, status: sub.status });
+      break;
+    }
+    case "customer.subscription.deleted": {
+      const sub = event.data.object as Stripe.Subscription;
+      // TODO: downgrade the user tied to sub.customer back to free.
+      console.log("[stripe] subscription deleted", { customer: sub.customer });
+      break;
+    }
+  }
+
+  return Response.json({ received: true });
+}

```