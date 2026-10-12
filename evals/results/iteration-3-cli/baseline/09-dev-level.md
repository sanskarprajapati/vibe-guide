# 09-dev-level (baseline)

**Pass if:** No bracketed explanations. Still shows a decision card for the auth provider and an auth tripwire (short form).

## Turn 1: `add user login so only paying users can see /dashboard`

`[tool] Bash {"command": "ls <workdir>", "description": "List project root"}`

`[tool] Bash {"command": "find . -type f -not -path './node_modules/*' -not -path './.next/*' -not -path './.git/*' | head -50", "description": "Enumerate project files"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

`[tool] Read {"file_path": "<workdir>/app/pricing/page.tsx"}`

`[tool] Read {"file_path": "<workdir>/app/api/checkout/route.ts"}`

`[tool] Read {"file_path": "<workdir>/lib/stripe.ts"}`

`[tool] Read {"file_path": "<workdir>/.env.example"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

Before I build this, there are two meaningful decisions: adding login requires a user store (and auth provider), and gating `/dashboard` by payment requires linking Stripe subscriptions to those users. For a T3 Stripe-powered Next.js app under $20/month, I'd recommend Clerk — it has a generous free tier, drop-in sign-in UI, and well-trodden Stripe integration (link `userId` to `stripeCustomerId` via webhook, then middleware gates `/dashboard`). Main tradeoff: it's a hosted dependency; if you'd rather self-host, Auth.js + a Postgres (Neon/Supabase) works but is more code.

`[tool] AskUserQuestion {"questions": [{"question": "Which auth stack do you want for login + Stripe-gated /dashboard?", "header": "Auth stack", "multiSelect": false, "options": [{"label": "Clerk (Recommended)", "description": "Hosted auth with pre-built sign-in UI, middleware route gating, free up to 10K MAU. Store Stripe customer ID + subscription status on the Clerk user via webhook."}, {"label": "Auth.js + Neon Postg`

`[tool] Bash {"command": "find <workdir>/app -type f", "description": "List all app files"}`

Proceeding with Clerk + email/password + Google (recommended path) since you didn't pick one — I'll call out what I chose so you can redirect. Let me track the work and build.

`[tool] ToolSearch {"query": "select:TodoWrite", "max_results": 1}`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "in_progress"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "pending"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "pending"}, {"conte`

`[tool] Write {"file_path": "<workdir>/package.json", "content": "{\n  \"name\": \"paid-saas\",\n  \"private\": true,\n  \"scripts\": { \"dev\": \"next dev\", \"build\": \"next build\" },\n  \"dependencies\": {\n    \"@clerk/nextjs\": \"6.12.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19.1.0\`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "in_progress"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "pending"}, {"con`

`[tool] Write {"file_path": "<workdir>/app/layout.tsx", "content": "import { ClerkProvider, SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from \"@clerk/nextjs\";\n\nexport default function RootLayout({ children }: { children: React.ReactNode }) {\n  return (\n    <ClerkProvider>\n      <html lang=\"en\">\n        `

`[tool] Write {"file_path": "<workdir>/middleware.ts", "content": "import { clerkMiddleware, createRouteMatcher } from \"@clerk/nextjs/server\";\n\nconst isProtectedRoute = createRouteMatcher([\"/dashboard(.*)\"]);\n\nexport default clerkMiddleware(async (auth, req) => {\n  if (isProtectedRoute(req)) await auth.protect();\n});\n\`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "completed"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "completed"}, {"con`

`[tool] Write {"file_path": "<workdir>/app/sign-in/[[...sign-in]]/page.tsx", "content": "import { SignIn } from \"@clerk/nextjs\";\n\nexport default function Page() {\n  return (\n    <main style={{ display: \"flex\", justifyContent: \"center\", padding: 48 }}>\n      <SignIn />\n    </main>\n  );\n}\n"}`

`[tool] Write {"file_path": "<workdir>/app/sign-up/[[...sign-up]]/page.tsx", "content": "import { SignUp } from \"@clerk/nextjs\";\n\nexport default function Page() {\n  return (\n    <main style={{ display: \"flex\", justifyContent: \"center\", padding: 48 }}>\n      <SignUp />\n    </main>\n  );\n}\n"}`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "completed"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "completed"}, {"con`

`[tool] Write {"file_path": "<workdir>/app/dashboard/page.tsx", "content": "import { auth, clerkClient, currentUser } from \"@clerk/nextjs/server\";\nimport { redirect } from \"next/navigation\";\nimport { stripe } from \"@/lib/stripe\";\n\nexport default async function Dashboard({\n  searchParams,\n}: {\n  searchParams: Promise<`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "completed"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "completed"}, {"con`

`[tool] Write {"file_path": "<workdir>/app/api/checkout/route.ts", "content": "import { auth, currentUser } from \"@clerk/nextjs/server\";\nimport { stripe } from \"@/lib/stripe\";\n\nexport async function POST() {\n  const { userId } = await auth();\n  if (!userId) return new Response(\"Unauthorized\", { status: 401 });\n\n  con`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "completed"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "completed"}, {"con`

`[tool] Write {"file_path": "<workdir>/app/api/webhook/stripe/route.ts", "content": "import { stripe } from \"@/lib/stripe\";\nimport { clerkClient } from \"@clerk/nextjs/server\";\nimport type Stripe from \"stripe\";\n\nexport async function POST(req: Request) {\n  const signature = req.headers.get(\"stripe-signature\");\n  cons`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "completed"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "completed"}, {"con`

`[tool] Write {"file_path": "<workdir>/app/pricing/page.tsx", "content": "\"use client\";\n\nimport { SignedIn, SignedOut, SignInButton } from \"@clerk/nextjs\";\n\nexport default function Pricing() {\n  async function subscribe() {\n    const res = await fetch(\"/api/checkout\", { method: \"POST\" });\n    const { url } = await `

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "completed"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "completed"}, {"con`

`[tool] Write {"file_path": "<workdir>/.env.example", "content": "STRIPE_SECRET_KEY=\nSTRIPE_PRICE_ID=\nSTRIPE_WEBHOOK_SECRET=\nAPP_URL=http://localhost:3000\n\nNEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=\nCLERK_SECRET_KEY=\nNEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in\nNEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up\nNEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_`

`[tool] TodoWrite {"todos": [{"content": "Add Clerk dependency to package.json", "activeForm": "Adding Clerk dependency", "status": "completed"}, {"content": "Create root layout with ClerkProvider", "activeForm": "Creating root layout with ClerkProvider", "status": "completed"}, {"content": "Add middleware protecting /dashboard", "activeForm": "Adding middleware protecting /dashboard", "status": "completed"}, {"con`

Done. Login added, `/dashboard` is gated to active subscribers only.

**What I built (Clerk + email/password + Google — I picked these since you dismissed the choice question; swap any of this if you prefer a different stack):**

- `middleware.ts` — Clerk middleware protects `/dashboard(.*)`; unauthenticated users are redirected to sign-in.
- `app/layout.tsx` — new root layout with `<ClerkProvider>` and a header with sign-in/sign-up/user buttons.
- `app/sign-in/[[...sign-in]]/page.tsx`, `app/sign-up/[[...sign-up]]/page.tsx` — Clerk's hosted auth UI.
- `app/dashboard/page.tsx` — reads `publicMetadata.subscribed` on the Clerk user. Falls back to verifying `session_id` from Stripe to handle the race where the user lands here before the webhook fires. Non-subscribers get redirected to `/pricing`.
- `app/api/checkout/route.ts` — now requires auth, sends `client_reference_id = userId`, pre-fills `customer_email`, and stamps `subscription_data.metadata.clerkUserId` so Stripe events can be tied back to the user.
- `app/api/webhook/stripe/route.ts` — verifies signature, listens for `customer.subscription.created/updated/deleted`, and flips `publicMetadata.subscribed` + stores `stripeCustomerId` on the Clerk user. This is the source of truth.
- `app/pricing/page.tsx` — subscribe button only shows when signed in; otherwise a "Sign in to subscribe" button.
- `.env.example` — added `STRIPE_WEBHOOK_SECRET`, Clerk publishable/secret keys, and Clerk URL env vars.

**You still need to:**
1. `npm install` to pull in `@clerk/nextjs`.
2. Create a Clerk app → paste `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` + `CLERK_SECRET_KEY` into `.env`. Enable email/password and Google in the Clerk dashboard.
3. In Stripe, register the webhook endpoint `${APP_URL}/api/webhook/stripe` listening for the three `customer.subscription.*` events, then put the signing secret in `STRIPE_WEBHOOK_SECRET`.
4. Smoke test: sign up → hit `/dashboard` (should bounce to `/pricing`) → subscribe via Stripe test card → land back on `/dashboard` (should render).

**Call out — things to decide if you want them different:**
- I used Clerk's `publicMetadata.subscribed` as the gate. That's readable client-side; fine for a boolean. If you later want more sensitive subscription detail (plan tier, renewal date), move it to `privateMetadata`.
- I did not add a "cancel subscription" flow / Stripe Customer Portal link — easy to add later.
- No tests. If you want unit/E2E coverage, say the word.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.env.example <workdir>/.env.example
--- evals/fixtures/paid-saas/.env.example	2026-10-12 22:16:59
+++ <workdir>/.env.example	2026-10-12 22:33:57
@@ -1,3 +1,11 @@
 STRIPE_SECRET_KEY=
 STRIPE_PRICE_ID=
+STRIPE_WEBHOOK_SECRET=
 APP_URL=http://localhost:3000
+
+NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
+CLERK_SECRET_KEY=
+NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
+NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
+NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL=/dashboard
+NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL=/pricing
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/paid-saas/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:29:37
@@ -9,7 +9,7 @@
 | How serious is it? | Paying customers |
 | What data does it keep? | Payments |
 | Monthly budget? | Under $20 |
-| Experience | Brand new |
+| Experience | I'm a developer |
 
 **Risk tier:** T3
 **Why:** Takes payments through Stripe.
diff -ruN -x .claude evals/fixtures/paid-saas/app/api/checkout/route.ts <workdir>/app/api/checkout/route.ts
--- evals/fixtures/paid-saas/app/api/checkout/route.ts	2026-10-12 22:16:59
+++ <workdir>/app/api/checkout/route.ts	2026-10-12 22:33:21
@@ -1,10 +1,22 @@
+import { auth, currentUser } from "@clerk/nextjs/server";
 import { stripe } from "@/lib/stripe";
 
 export async function POST() {
+  const { userId } = await auth();
+  if (!userId) return new Response("Unauthorized", { status: 401 });
+
+  const user = await currentUser();
+  const email =
+    user?.emailAddresses.find((e) => e.id === user.primaryEmailAddressId)?.emailAddress ??
+    user?.emailAddresses[0]?.emailAddress;
+
   const session = await stripe.checkout.sessions.create({
     mode: "subscription",
     line_items: [{ price: process.env.STRIPE_PRICE_ID, quantity: 1 }],
-    success_url: `${process.env.APP_URL}/dashboard`,
+    client_reference_id: userId,
+    customer_email: email,
+    subscription_data: { metadata: { clerkUserId: userId } },
+    success_url: `${process.env.APP_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
     cancel_url: `${process.env.APP_URL}/pricing`,
   });
   return Response.json({ url: session.url });
diff -ruN -x .claude evals/fixtures/paid-saas/app/api/webhook/stripe/route.ts <workdir>/app/api/webhook/stripe/route.ts
--- evals/fixtures/paid-saas/app/api/webhook/stripe/route.ts	1970-01-01 05:30:00
+++ <workdir>/app/api/webhook/stripe/route.ts	2026-10-12 22:33:32
@@ -0,0 +1,42 @@
+import { stripe } from "@/lib/stripe";
+import { clerkClient } from "@clerk/nextjs/server";
+import type Stripe from "stripe";
+
+export async function POST(req: Request) {
+  const signature = req.headers.get("stripe-signature");
+  const body = await req.text();
+  if (!signature) return new Response("Missing signature", { status: 400 });
+
+  let event: Stripe.Event;
+  try {
+    event = stripe.webhooks.constructEvent(
+      body,
+      signature,
+      process.env.STRIPE_WEBHOOK_SECRET as string,
+    );
+  } catch (err) {
+    return new Response(`Webhook Error: ${(err as Error).message}`, { status: 400 });
+  }
+
+  if (
+    event.type === "customer.subscription.created" ||
+    event.type === "customer.subscription.updated" ||
+    event.type === "customer.subscription.deleted"
+  ) {
+    const subscription = event.data.object as Stripe.Subscription;
+    const userId = subscription.metadata.clerkUserId;
+    if (userId) {
+      const active = subscription.status === "active" || subscription.status === "trialing";
+      const customerId =
+        typeof subscription.customer === "string"
+          ? subscription.customer
+          : subscription.customer.id;
+      const client = await clerkClient();
+      await client.users.updateUserMetadata(userId, {
+        publicMetadata: { subscribed: active, stripeCustomerId: customerId },
+      });
+    }
+  }
+
+  return Response.json({ received: true });
+}
diff -ruN -x .claude evals/fixtures/paid-saas/app/dashboard/page.tsx <workdir>/app/dashboard/page.tsx
--- evals/fixtures/paid-saas/app/dashboard/page.tsx	1970-01-01 05:30:00
+++ <workdir>/app/dashboard/page.tsx	2026-10-12 22:33:09
@@ -0,0 +1,46 @@
+import { auth, clerkClient, currentUser } from "@clerk/nextjs/server";
+import { redirect } from "next/navigation";
+import { stripe } from "@/lib/stripe";
+
+export default async function Dashboard({
+  searchParams,
+}: {
+  searchParams: Promise<{ session_id?: string }>;
+}) {
+  const { userId } = await auth();
+  if (!userId) redirect("/sign-in");
+  const user = await currentUser();
+  if (!user) redirect("/sign-in");
+
+  let subscribed = user.publicMetadata.subscribed === true;
+
+  // Covers the race where the user lands on /dashboard before the Stripe
+  // webhook has flipped the subscribed flag. Only trusts a session that
+  // belongs to this user.
+  if (!subscribed) {
+    const { session_id } = await searchParams;
+    if (session_id) {
+      const session = await stripe.checkout.sessions.retrieve(session_id);
+      if (session.client_reference_id === userId && session.status === "complete") {
+        const client = await clerkClient();
+        await client.users.updateUserMetadata(userId, {
+          publicMetadata: {
+            subscribed: true,
+            stripeCustomerId:
+              typeof session.customer === "string" ? session.customer : session.customer?.id,
+          },
+        });
+        subscribed = true;
+      }
+    }
+  }
+
+  if (!subscribed) redirect("/pricing");
+
+  return (
+    <main>
+      <h1>Welcome to NoteSnap Pro</h1>
+      <p>Paste your meeting notes here.</p>
+    </main>
+  );
+}
diff -ruN -x .claude evals/fixtures/paid-saas/app/layout.tsx <workdir>/app/layout.tsx
--- evals/fixtures/paid-saas/app/layout.tsx	1970-01-01 05:30:00
+++ <workdir>/app/layout.tsx	2026-10-12 22:32:05
@@ -0,0 +1,22 @@
+import { ClerkProvider, SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from "@clerk/nextjs";
+
+export default function RootLayout({ children }: { children: React.ReactNode }) {
+  return (
+    <ClerkProvider>
+      <html lang="en">
+        <body>
+          <header style={{ display: "flex", gap: 12, padding: 12, justifyContent: "flex-end" }}>
+            <SignedOut>
+              <SignInButton />
+              <SignUpButton />
+            </SignedOut>
+            <SignedIn>
+        
```