# 12-background-job (skill)

**Pass if:** Recognises a scheduled background job plus an email service plus stored signups (which don't exist yet). Brief explains the scheduled-job idea in plain words, the missing database, options for running it, cost, and waits.

## Turn 1: `/vibe send me an email every morning with how many people signed up the day before`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project root files"}`

`[tool] Bash {"command": "ls -la <workdir> <workdir>", "description": "List .vibe and app dirs"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls -la <workdir> && cat <workdir> <workdir>", "description": "List api dir and read README/package.json"}`

`[tool] Bash {"command": "ls -la <workdir> && find <workdir> -type f", "description": "Inspect signup route"}`

`[tool] Read {"file_path": "<workdir>"}`

Here's the shape of what you're asking for. One quick heads-up before the brief: right now your signup form **doesn't actually save emails anywhere** — the API route logs them to the server console and that's it (`app/api/signup/route.ts:4`). So "count yesterday's signups" has nothing to count yet. The daily email needs us to fix that first.

## Brief: daily signup count by email

**What you'll get**
Every morning at ~9am, an email in your inbox that says something like *"Plantpal waitlist: 7 new signups yesterday (142 total)"*.

**What it actually takes**
Three things, because none of them exist yet:
1. **A place to store emails** (a **database** — a filing cabinet your app can read and write from). Needed so there's something to count.
2. **An email sender** (a service that delivers mail on your behalf, so Gmail doesn't flag it as spam).
3. **A scheduler** (a **cron job** — an alarm clock that pokes your app at a set time every day).

**The stack I'd pick for your tier (public, free, under $20/mo)**

- **Database:** Supabase (free tier is generous, built-in access rules for public apps). Alternatives below.
- **Email sender:** Resend (free: 3k emails/mo, 100/day — plenty for a daily report to one person).
- **Scheduler + hosting:** Vercel. Their free Hobby plan includes one daily **cron job**, which is exactly what we need.

Total monthly cost: **$0** on free tiers for a waitlist your size.

**Alternatives worth knowing about**

| Approach | Pros | Cons |
|---|---|---|
| **Build it (recommended)** — Supabase + Resend + Vercel Cron | Full control, zero cost, your emails stay yours | ~4 moving parts to set up once |
| **Managed waitlist tool** (Loops.so, GetWaitlist, Waitlisted) | Signup form + dashboard + email are all built-in | Monthly fee once past free tier, your emails live on their platform, less flexible when you launch |
| **Just query Vercel logs** | No new services | Logs expire fast, not reliable, and you still don't have the emails saved for launch day |

The build-it path also leaves you with your emails in a database you own, which you'll need anyway when Plantpal launches and you want to notify people.

**Risks and what I'll do about them**
- **Public page storing stranger emails** → I'll turn on Supabase **row-level security** (a lock that says "the browser can insert emails but can't read the list back"). You'll want to double-check it; I'll show you how.
- **API keys for Supabase and Resend** → never in code, only in Vercel's environment variables. I'll walk you through where to paste them.
- **Email could land in spam at first** → Resend uses a shared verified domain for free accounts, which is fine for a daily report to yourself. For launch emails to users later, you'd want to verify your own domain.
- **Deploy to Vercel required for cron to work** → it won't run on your laptop. If you don't have a Vercel account yet, we'll make one (free).
- **Not a replacement for a real backup** → database still needs occasional CSV exports before launch. I'll leave a note.

**What you'll need to do (hands-on bits)**
1. Sign up for Supabase (free), click one button to create a project.
2. Sign up for Resend (free), confirm your email.
3. Sign up for Vercel (free) if you don't have it, link to this folder.
4. Paste 3 keys into Vercel's dashboard. I'll tell you exactly which ones.

Rough time: **30–45 minutes end-to-end**, most of it waiting for signups and clicking through sign-ups.

**One quick question before I start:**

`[tool] AskUserQuestion {"questions": [{"question": "What time of day do you want the email to arrive?", "header": "Email time", "multiSelect": false, "options": [{"label": "9am my time (Recommended)", "description": "A good default \u2014 you'll see yesterday's full count with your morning coffee."}, {"label": "7am", "description": "Earlier \u2014 in your inbox before you start the day."}, {"label": "Noon", "description`

I'll pause here and wait for your call on time and approach before I touch any code.

Quick recap of where this stands: **the signup form isn't saving emails yet**, so the daily email has nothing to count until we fix that. The plan above fixes both at once — adds a database to store signups, and the daily email reads from it.

Pick a time + approach above (or type your own) and I'll go.

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
(no file changes)
```