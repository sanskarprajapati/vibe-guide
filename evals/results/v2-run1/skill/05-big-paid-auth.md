# 05-big-paid-auth (skill)

**Pass if:** Full brief that explains the missing pieces (accounts, a place to store who paid, a webhook) in plain words, compares options, lists risks (webhook signature, server-side check), recommends a human review before taking real money, and waits. No project files changed.

## Turn 1: `/vibe add user login so only paying users can see /dashboard`

`[tool] Bash {"command": "ls -la <workdir> 2>&1 | head -50", "description": "List project directory contents"}`

`[tool] Bash {"command": "ls -la <workdir> 2>&1", "description": "Check for .vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "find <workdir> -type f -not -path \"*/node_modules/*\" -not -path \"*/.git/*\" -not -path \"*/.claude/*\" 2>&1 | head -40", "description": "List all project files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Right, I've read the project. One-liner: NoteSnap is a Next.js app that sells a $9/month Pro plan through Stripe, and the dashboard page doesn't exist yet. Working from your profile: public paid app, Stripe already wired, budget under $20/month, new to coding — so I'll keep this cheap and gentle.

This one is **big**. It changes the shape of the app (adds accounts, a database, and a way to know who actually paid). Here's the brief — I won't touch anything yet.

---

## What you're asking for

Right now, anyone who finishes checkout gets redirected to `/dashboard`, but that page doesn't exist, and even if it did, there's no way to tell paying customers apart from someone who just typed `/dashboard` into the browser. To fix that properly, three things have to show up in the project:

1. **Logins** — so people have accounts.
2. **A way to remember who paid** — a tiny database table that says "this user has an active Pro subscription".
3. **A webhook** (a URL Stripe calls when something changes — think of it as Stripe ringing a doorbell every time a payment happens or a subscription cancels) that keeps that table in sync.

Then `/dashboard` just checks: are you logged in? Is your row marked "active"? If yes, show it. If no, bounce to pricing or login.

## What I'd use: Supabase

Supabase gives you logins (email + password, or magic-link emails) and a Postgres database on the same free account. For a brand-new project on your budget, it's the gentlest fit — one signup, one dashboard, free up to 50,000 users.

Flow becomes:
```
Visitor → signs up → logs in → clicks Subscribe
       → Stripe checkout (we tell Stripe who they are)
       → Stripe charges them
       → Stripe calls our webhook → we flip their row to "active"
       → /dashboard sees "active" → lets them in
```

## Alternatives

| Option | Good | Not so good |
|---|---|---|
| **Supabase (recommended)** | Free for your scale, one service for both auth and the database, lots of Next.js examples | Two concepts to learn (auth + a database table) |
| **Clerk** | The prettiest login UI, almost no code | Jumps to $25/month past 10k users — over your stated budget — and still needs a tiny DB elsewhere |
| **Auth.js + Vercel Postgres** | Fully in your Vercel account | You wire everything by hand; harder for a first project |

If you have a preference, say so and I'll go with it.

## What I'd actually build (step by step)

1. Add Supabase to the project; set up a `profiles` table (one row per user) with `stripe_customer_id` and `subscription_status` columns.
2. Add `/signup` and `/login` pages (email + password to start — easiest to grasp; we can add Google later).
3. Require login before `/api/checkout` runs, and pass the logged-in user's id to Stripe so the webhook knows who paid.
4. Add `/api/stripe/webhook` — the endpoint Stripe pings. It updates the `profiles` row when checkout completes, when a subscription renews, and when it cancels.
5. Make `/dashboard` a real page that reads the row and either shows the dashboard or sends you to pricing.
6. Add a "Log out" link and a tiny "You're on Pro ✓" indicator so you can see it working.

## What you'd need to do

Three signups, mostly free:

- **Supabase account** (free) — I'll tell you exactly what to copy.
- **Stripe webhook secret** — you add one URL in your Stripe dashboard, copy a value into `.env`.
- **Local Stripe CLI** (optional but handy) so webhooks work on your laptop before you deploy.

## Risks I want to name upfront

- **Secret keys**: Supabase has two keys (public + service role). The service role key can read anyone's data — it only ever goes in `.env`, never in a page or component. I'll set this up carefully.
- **Row-level security** (database rules that stop one user reading another user's row): I'll turn it on from day one so your users can't see each other's data. You won't need to configure it — I will.
- **Webhook truth**: Only the Stripe webhook is allowed to mark someone "paid". A user hitting `/dashboard` right after checkout can't fake it, because the status lives in the database, not in the browser.
- **Signed-up but didn't pay**: Someone can sign up for free and never subscribe — that's fine, they just can't reach `/dashboard`.
- **Not a security review**: I'm doing the sensible defaults, but once this takes real money, having an experienced developer look it over before launch is worth doing.

## Cost

$0/month at your scale. Free tiers for Supabase cover you until ~50k users; Stripe only charges on real transactions.

## Time

About 20–30 minutes of me working, with a few checkpoints along the way (after Supabase is set up, after the webhook is working, before deploy).

---

A couple of things I need you to answer before I start.

`[tool] AskUserQuestion {"questions": [{"question": "Which auth provider should I set this up with?", "header": "Auth provider", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "Free for your scale, bundles logins + the database I need for subscription status. Best fit for your budget and new-to-coding profile."}, {"label": "Clerk", "description": "Prettiest signup UI, least code. But`

Question tool didn't go through — here they are inline instead. Pick one from each and I'll start.

**1. Which auth provider?**
   a. **Supabase** (recommended) — free at your scale, bundles logins + database.
   b. **Clerk** — prettiest UI, least code, but $25/month past 10k users (over your budget).
   c. **Auth.js + Vercel Postgres** — all inside Vercel, more hand-wiring.

**2. How should people log in?**
   a. **Email + password** (recommended) — easiest to understand and demo.
   b. **Magic link email** — click a link in your inbox to log in; no passwords.
   c. **Google sign-in** — one-click Google; a bit more setup on day one.

Reply with something like "1a, 2a" (or just "go with the recommendations") and I'll start on step 1.

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
(no file changes)
```