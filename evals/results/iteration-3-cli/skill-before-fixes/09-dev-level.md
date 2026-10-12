# 09-dev-level (skill)

**Pass if:** No bracketed explanations. Still shows a decision card for the auth provider and an auth tripwire (short form).

## Turn 1: `/vibe add user login so only paying users can see /dashboard`

`[tool] Bash {"command": "ls -la <workdir>/ 2>&1; echo \"---\"; ls -la <workdir>/.vibe/ 2>&1", "description": "Check for existing profile and project files"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Bash {"command": "find <workdir>/app <workdir>/lib -type f 2>&1", "description": "List project source files"}`

`[tool] Read {"file_path": "<workdir>/app/api/checkout/route.ts"}`

`[tool] Read {"file_path": "<workdir>/app/pricing/page.tsx"}`

`[tool] Read {"file_path": "<workdir>/lib/stripe.ts"}`

`[tool] Read {"file_path": "<workdir>/.env.example"}`

`[tool] Bash {"command": "ls <workdir>/.claude/skills/vibe/references/ 2>&1", "description": "List vibe skill references"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/tripwires.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/explain-style.md"}`

Using your profile: public SaaS taking Stripe payments, developer level, T3.

Before I write code: adding login is a service choice, so let me surface the options. The task also needs a way to persist "user X is subscribed" (set by Stripe webhook, read when gating `/dashboard`), so the auth choice bleeds into whether we also pull in a database.

---

You need **user authentication for a Next.js app + a place to track Stripe subscription status per user**. For a T3 Next.js SaaS on Stripe, <$20/mo, dev-level, here's what fits:

**1. Clerk** — hosted auth with first-class Next.js middleware. **Recommended.**
- Fits you because: Next.js App Router SDK + `middleware.ts` protection for `/dashboard` is a few lines. You can store subscription status in `publicMetadata` from a Stripe webhook — no separate DB until you actually need one.
- Cost at your size: free tier covers you well past launch; usage-priced per MAU after that.
- Watch out for: lock-in on user records (export is possible but not instant); their hosted sign-in UI is fastest, custom UI needs more work.

**2. Supabase Auth** — auth + Postgres bundled.
- Fits you because: you'll likely want a real DB soon anyway (user-owned data, usage logs). One service for auth + a `subscriptions` table keyed by `auth.uid()`.
- Cost at your size: free tier fits; paused after inactivity on free, backups on paid.
- Watch out for: RLS has to be correct on every table from day one — easy to leave a policy too open. Plain Postgres underneath, so leaving later is realistic.

**3. NextAuth / Auth.js** — not a fit here: self-hosted library needs its own DB adapter, session table, and email provider wired up. More moving parts than you need for a solo T3 build under $20.

`[tool] ToolSearch {"query": "select:AskUserQuestion", "max_results": 1}`

`[tool] AskUserQuestion {"questions": [{"question": "Which auth provider should I wire into the app?", "header": "Auth provider", "multiSelect": false, "options": [{"label": "Clerk (Recommended)", "description": "Hosted auth with Next.js middleware. Store subscription status in Clerk publicMetadata via Stripe webhook \u2014 no separate database yet."}, {"label": "Supabase Auth", "description": "Auth + Postgres bundled. T`

Pick one and I'll build it out from there. Once you choose, next steps will be: `/dashboard` page + server-side gate (middleware checks auth, server component checks subscription), Stripe webhook that marks the user as subscribed on `checkout.session.completed` and un-marks on `customer.subscription.deleted`, and the env vars/dashboard steps you'll need to do yourself.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/paid-saas/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:29:17
@@ -9,7 +9,7 @@
 | How serious is it? | Paying customers |
 | What data does it keep? | Payments |
 | Monthly budget? | Under $20 |
-| Experience | Brand new |
+| Experience | I'm a developer |
 
 **Risk tier:** T3
 **Why:** Takes payments through Stripe.

```