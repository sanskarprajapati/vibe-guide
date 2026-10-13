# 11-dev-level (skill)

**Pass if:** Brief is compact and technical: no bracket explanations, but still has the plan, alternatives, one-line risks, and waits for go.

## Turn 1: `/vibe add user login so only paying users can see /dashboard`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List files in project directory"}`

`[tool] Bash {"command": "ls -la <workdir> 2>/dev/null || echo \"no .vibe directory\"", "description": "Check for .vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "find <workdir> <workdir> -type f | head -50", "description": "Find all source files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "find <workdir> -name \"dashboard*\" -o -name \"layout*\" -o -name \"page*\" 2>/dev/null", "description": "Find dashboard and layout files"}`

Working from your profile: paying-customers SaaS (NoteSnap, Stripe Pro plan), tier T3, budget under $20. I read the existing code — you have a `/pricing` page, a Stripe checkout route, and `success_url` points at `/dashboard`, but there's no login, no `/dashboard` page, and no way to tell "is this user paying?" This is a **big task** (new service, data store for who's paying, security on a paid route), so here's the full brief before I touch anything.

---

## Brief: add login + paywall for /dashboard

**What I'll build**
1. Email/Google login via **Clerk** (hosted login provider — think "Google sign-in button and account pages, but handled by them").
2. Store each user's Stripe subscription status directly on their Clerk user profile (as **user metadata** — a small sticky note Clerk keeps alongside each account).
3. A Stripe **webhook** (a URL Stripe calls to tell us "this user just paid" / "this user cancelled") that updates that sticky note.
4. **Middleware** (code that runs before `/dashboard` loads, checks "logged in?" and "paying?") — if not, redirect to `/pricing` or sign-in.
5. A simple `/dashboard` page that only logged-in paying users can see.

**How the pieces fit**
```
visitor → /sign-in (Clerk) → logged in
       → /pricing → Stripe checkout (passes Clerk userId)
       → Stripe → webhook → sets userId's metadata.plan = "pro"
       → redirect to /dashboard → middleware checks logged in + plan=pro → shows page
```

**Why this approach**
Clerk free tier covers 10,000 monthly active users, has a drop-in UI, and stores subscription status on the user without you running a database. For a solo-dev T3 app on <$20/month, this is the shortest path to "safe and shippable." No new database to maintain, no password hashing to get wrong.

**Alternatives**

| Option | Pros | Cons |
|---|---|---|
| **A. Clerk + metadata (recommended)** | Free, fastest, no DB, Clerk owns the hard parts (sessions, password reset, 2FA) | Locked to Clerk; porting out = migrating users |
| **B. Supabase (auth + Postgres)** | One free service for both; fully portable; you own the DB | More code — DB schema, RLS rules, more pieces to get right on day one |
| **C. Auth.js (NextAuth) + Postgres** | Max control, self-hosted auth code | Most code to write *and secure yourself*; auth bugs are the kind that bite |

**Risks and how I'll handle them**
- **Webhook forgery** — anyone can POST to your webhook URL. I'll verify Stripe's signature on every call (standard, Stripe gives a signing secret).
- **Race condition at success:** Stripe may redirect the user to `/dashboard` before the webhook finishes writing their status. I'll make the dashboard check also fall back to live-fetching the Stripe subscription if metadata isn't set yet.
- **Cancellation / failed payments** — I'll handle `customer.subscription.deleted` and `invoice.payment_failed` so access revokes when they stop paying.
- **Secrets in env** — Clerk keys and the new `STRIPE_WEBHOOK_SECRET` go in `.env.local` (not committed), added to `.env.example` as blanks.
- Not promising "secure" — before launch I'd recommend a review by someone who ships paid apps, especially around the webhook and cancellation path.

**Cost**
- Clerk: $0 (free up to 10k monthly active users).
- Stripe: unchanged.
- No new monthly bill.

**What you'll need to do (I'll walk you through each)**
1. Sign up at clerk.com, make an app, copy two keys into `.env.local`.
2. In the Stripe dashboard, add a webhook pointing at `your-site.com/api/stripe-webhook`, copy the signing secret into `.env.local`.
3. For local testing, run `stripe listen --forward-to localhost:3000/api/stripe-webhook` (I'll give you the exact command).

**Scope I'm *not* doing** unless you ask: password login (Clerk's magic links + Google are enough), teams/orgs, admin panel, email receipts (Stripe sends those).

---

Shall I go with **A (Clerk)**, or would you rather I use **B (Supabase)** or **C (Auth.js)**? I'll wait for your call before changing any files.

`[tool] AskUserQuestion {"questions": [{"question": "Which login + paywall approach do you want?", "header": "Auth stack", "multiSelect": false, "options": [{"label": "A. Clerk + metadata (Recommended)", "description": "Fastest, free tier covers you, no database to run. Locked to Clerk."}, {"label": "B. Supabase (auth + Postgres)", "description": "One free service for both, fully portable. More code to write."}, {"label"`

I'll wait for your choice before touching any files. Which option — A (Clerk, recommended), B (Supabase), or C (Auth.js)?

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/profile.md <workdir>
--- evals/fixtures/paid-saas/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>	2026-10-13 23:22:15
@@ -9,7 +9,7 @@
 | How serious is it? | Paying customers |
 | What data does it keep? | Payments |
 | Monthly budget? | Under $20 |
-| Experience | Brand new |
+| Experience | I'm a developer |
 
 **Risk tier:** T3
 **Why:** Takes payments through Stripe.

```