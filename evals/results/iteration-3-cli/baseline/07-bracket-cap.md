# 07-bracket-cap (baseline)

**Pass if:** At most 3 bracketed explanations in the reply. None inside code blocks, commands or file paths. No 'simply/just/easy'. Plain language.

## Turn 1: `explain the whole plan for putting this waitlist online and storing the emails. don't change any code yet`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List files in working directory"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

`[tool] Bash {"command": "ls -la <workdir>/app && cat <workdir>/package.json", "description": "List app directory and show package.json"}`

`[tool] Read {"file_path": "<workdir>/app/page.tsx"}`

`[tool] Bash {"command": "ls -la <workdir>/app/api && find <workdir>/app/api -type f", "description": "List api directory"}`

`[tool] Read {"file_path": "<workdir>/app/api/signup/route.ts"}`

Here's what I see and the plan for getting this live.

## Current state

- Next.js 15 app with one page (`app/page.tsx`) that POSTs `{ email }` to `/api/signup`.
- `app/api/signup/route.ts` just `console.log`s the email — no storage, no validation, no error handling.
- No database, no hosting config, no env vars.

## Plan

**1. Pick the storage.** The main decision. Three realistic options:

| Option | Setup | Cost at waitlist scale | Portability |
|---|---|---|---|
| **Vercel Postgres / Neon** (recommended) | ~5 min, one `DATABASE_URL` env var, `@neondatabase/serverless` driver | Free tier covers thousands of signups | Standard Postgres, easy to export |
| **Supabase** | Dashboard-driven, gives you a UI to view rows | Free tier | Standard Postgres, you can also use its auth later |
| **Airtable / Google Sheets via API** | Zero schema work, non-technical people can view the list | Free | Harder to migrate off |

I'd recommend Neon on Vercel: it's the shortest path and keeps you in SQL for whatever comes next.

**2. Schema.** One table:
```
waitlist(id uuid pk, email text unique not null citext,
         created_at timestamptz default now(),
         source text, user_agent text, ip inet)
```
`unique` on email so duplicate submissions are idempotent, `citext` so `A@x.com` and `a@x.com` collide.

**3. Harden `app/api/signup/route.ts`.** Currently it trusts whatever comes in. It needs:
- Validate the email (regex or `zod`) and reject empty/malformed before touching the DB.
- `INSERT ... ON CONFLICT (email) DO NOTHING` so retries are safe.
- Return `{ ok: true }` on both insert and duplicate; return 400 on bad input, 500 on DB error.
- Basic rate limit (e.g. Vercel's `@vercel/edge` KV or Upstash Redis — 5 req/min/IP). Optional for v1 but worth noting.
- Capture `request.headers.get('x-forwarded-for')` for the `ip` column.

**4. Fix the client.** `app/page.tsx` currently sets `done = true` even if the fetch fails. Add error state and show it. Also set `Content-Type: application/json` on the request (currently missing, works by luck).

**5. Deploy.** Vercel is the path of least resistance for Next.js:
- Push repo to GitHub, import into Vercel.
- Add `DATABASE_URL` to Vercel env vars (Production + Preview).
- Run the `create table` migration once from your laptop (`psql $DATABASE_URL < schema.sql`) or add a `migrations/` folder and run it as a build step.
- Point your domain at Vercel.

**6. Access the emails.** You'll want to actually read the list:
- Quick path: Neon/Supabase both have a web SQL console.
- Nicer: a password-protected `/admin` route, or a scheduled job that emails you a CSV weekly.

**7. Compliance / hygiene before going public.**
- Add a one-line consent note under the form ("We'll email you when Plantpal launches.").
- Link to a privacy page saying what you store and how to request deletion. Required under GDPR/CCPA if you have EU/CA visitors.
- Decide if you want double opt-in (send a confirmation email). Not required for a waitlist, but it keeps your list clean when you later send launch mail.

## Order I'd do it in

1. Create Neon DB + run schema (10 min).
2. Rewrite the API route with validation + insert (20 min).
3. Fix the client's error handling (5 min).
4. Deploy to Vercel with the env var (10 min).
5. Add consent copy + privacy blurb (10 min).
6. Rate limiting + admin view (later, once you see real traffic).

Want me to proceed with the Neon + Vercel path, or would you rather use Supabase / Airtable / something else?

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:28:43
@@ -9,7 +9,7 @@
 | How serious is it? | Real users, free |
 | What data does it keep? | Names, emails, logins |
 | Monthly budget? | Under $20 |
-| Experience | Built a few things |
+| Experience | Brand new |
 
 **Risk tier:** T2
 **Why:** Public page that stores strangers' email addresses.

```