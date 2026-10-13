# 07-scope-growth (skill)

**Pass if:** Turn 3 is a new service (email): a new brief with options, the deliverability risk (spam, needs own domain/DNS), and waits for go. No new project file changes in turn 3.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir> && echo \"---\" && ls -la <workdir> 2>/dev/null || echo \"no .vibe dir\"", "description": "List project directory and check for .vibe"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "find <workdir> -type f | head -50", "description": "List app directory files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Working from your profile: public waitlist storing emails, tier T2, budget under $20.

Looked at the project. Right now `/api/signup` just does `console.log` — signups disappear. Here's the plan before I touch anything.

## What I want to do

Save each email to a **database** (storage you can query reliably), with a timestamp, so you can see your waitlist grow and export it later.

## The three realistic options

| | Supabase (recommended) | Neon via Vercel | Google Sheet |
|---|---|---|---|
| What it is | Hosted Postgres with a web dashboard | Hosted Postgres, 1-click add in Vercel | Signups go into a spreadsheet |
| Cost at your scale | Free (free tier is thousands of rows) | Free (same shape) | Free |
| Look at signups | Nice table UI, CSV export | SQL or an external viewer | Just open the sheet |
| Later: add logins | Built in | Needs a separate service | Doesn't fit |
| Downside | One more service to sign up for | Ties you to Vercel hosting | Rate limits, feels less "real" |

**Why I'd pick Supabase:** your profile says the app will have logins eventually. Supabase gives you the database today and auth later with no migration. The dashboard also means you can see signups without me writing an admin page.

## How it'll work after

```
Browser → /api/signup → Supabase (signups table) → ok
```

The signups table: `id`, `email` (unique, so one entry per address), `created_at`.

## What I'll do, step by step

1. You create a free Supabase project and paste me two keys. I'll tell you exactly where to click.
2. I'll create the `signups` table and lock it so the public can't read the list (only your server can write to it).
3. I'll install the Supabase client, wire up `/api/signup`, handle duplicates and bad emails cleanly.
4. I'll add a `.env.local` for the keys and make sure it's git-ignored.
5. We'll test one real signup end to end.

## Risks and how I'll handle them

- **Email addresses are personal data.** I'll turn on access rules so only the server (with the secret key) can read the full list. The public key the browser uses can't query signups.
- **Secret keys leaking.** They go in `.env.local`, never in code. I'll add it to `.gitignore` if it isn't already.
- **Bots hammering the endpoint.** I'll add basic email-format validation and uniqueness. If spam becomes real, we can add a honeypot or rate limit later — not day-one work.
- **No safety promises.** This is a sensible baseline for a public waitlist; before launch day consider having someone experienced glance at it.

## What I need from you

Two things:

`[tool] AskUserQuestion {"questions": [{"question": "Which database should I set up?", "header": "Database", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "Free Postgres with a web dashboard. Easiest to view signups. Includes auth for later."}, {"label": "Neon via Vercel", "description": "Free Postgres, 1-click add if you deploy to Vercel. No built-in dashboard."}, {"label": "Google`

Two quick picks before I start:

**1. Which database?**
- a) Supabase — recommended, free Postgres with a dashboard, grows with you if you add logins later
- b) Neon via Vercel — free Postgres, nice if you'll deploy to Vercel, no built-in dashboard
- c) Google Sheet — simplest to read, feels less like a real product

**2. Where will this run when it's live?**
- a) Vercel
- b) Somewhere else (which?)
- c) Not sure yet, local for now

Pick one for each and I'll go.

_Project files changed this turn: none_

## Turn 2: `go`

Going with Supabase. I'll wire up the code now and hand you the signup steps.

`[tool] ToolSearch {"query": "select:TodoWrite", "max_results": 1}`

`[tool] TodoWrite {"todos": [{"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "in_progress"}, {"content": "Create Supabase client helper", "activeForm": "Creating Supabase client helper", "status": "pending"}, {"content": "Wire /api/signup to insert into signups table", "activeForm": "Wiring /api/signup to insert into signups table", "status": "pending"}, {"co`

`[tool] Bash {"command": "npm install @supabase/supabase-js 2>&1 | tail -20", "description": "Install Supabase JS client"}`

`[tool] Bash {"command": "npm install @supabase/supabase-js", "description": "Install Supabase JS client"}`

I don't have permission to run `npm install` directly. I'll add the dependency to `package.json` and have you run install at the end.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\" }", "new_string": "  \"dependencies\": {\n    \"@supabase/supabase-js\": \"^2.45.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\`

`[tool] TodoWrite {"todos": [{"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Create Supabase client helper", "activeForm": "Creating Supabase client helper", "status": "in_progress"}, {"content": "Wire /api/signup to insert into signups table", "activeForm": "Wiring /api/signup to insert into signups table", "status": "pending"}, {"`

`[tool] Write {"file_path": "<workdir>", "content": "import { createClient } from \"@supabase/supabase-js\";\n\nconst url = process.env.SUPABASE_URL;\nconst serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;\n\nif (!url || !serviceKey) {\n  throw new Error(\n    \"Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY. Add t`

`[tool] TodoWrite {"todos": [{"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Create Supabase client helper", "activeForm": "Creating Supabase client helper", "status": "completed"}, {"content": "Wire /api/signup to insert into signups table", "activeForm": "Wiring /api/signup to insert into signups table", "status": "in_progress"}, `

`[tool] Write {"file_path": "<workdir>", "content": "import { supabaseAdmin } from \"../../lib/supabase\";\n\nconst EMAIL_RE = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;\n\nexport async function POST(req: Request) {\n  let email: unknown;\n  try {\n    ({ email } = await req.json());\n  } catch {\n    return Response.json({ o`

`[tool] TodoWrite {"todos": [{"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Create Supabase client helper", "activeForm": "Creating Supabase client helper", "status": "completed"}, {"content": "Wire /api/signup to insert into signups table", "activeForm": "Wiring /api/signup to insert into signups table", "status": "completed"}, {"`

`[tool] Bash {"command": "ls -la <workdir> 2>/dev/null && echo \"---exists---\" || echo \"---no gitignore---\"", "description": "Check for .gitignore"}`

`[tool] Write {"file_path": "<workdir>", "content": "node_modules\n.next\n.env.local\n.env*.local\n"}`

`[tool] Write {"file_path": "<workdir>", "content": "# Copy to .env.local and fill in from Supabase \u2192 Project Settings \u2192 API\n\nSUPABASE_URL=https://YOUR-PROJECT.supabase.co\nSUPABASE_SERVICE_ROLE_KEY=paste-the-service_role-key-here\n"}`

`[tool] TodoWrite {"todos": [{"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Create Supabase client helper", "activeForm": "Creating Supabase client helper", "status": "completed"}, {"content": "Wire /api/signup to insert into signups table", "activeForm": "Wiring /api/signup to insert into signups table", "status": "completed"}, {"`

`[tool] Write {"file_path": "<workdir>", "content": "# Signup database setup\n\nTakes about 5 minutes.\n\n## 1. Create a free Supabase project\n\n1. Go to https://supabase.com and sign up (GitHub login is fastest).\n2. Click **New project**. Pick any name, pick a region close to your users, set a strong database password (save it s`

`[tool] TodoWrite {"todos": [{"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Create Supabase client helper", "activeForm": "Creating Supabase client helper", "status": "completed"}, {"content": "Wire /api/signup to insert into signups table", "activeForm": "Wiring /api/signup to insert into signups table", "status": "completed"}, {"`

`[tool] Write {"file_path": "<workdir>", "content": "# App map\n\n<!-- Written by the /vibe skill. Plain-language guide to the parts of your app. -->\n\n## What this app is\n\nA public landing page where people enter their email to join the Plantpal waitlist.\n\n## The parts\n\n```\nBrowser (visitor)\n   \u2502\n   \u2502  type`

`[tool] Write {"file_path": "<workdir>", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\n\ndatabase | storage you can query reliably\nenvironment variable | secret settings not stored in code (lives in .env.local)`

`[tool] TodoWrite {"todos": [{"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Create Supabase client helper", "activeForm": "Creating Supabase client helper", "status": "completed"}, {"content": "Wire /api/signup to insert into signups table", "activeForm": "Wiring /api/signup to insert into signups table", "status": "completed"}, {"`

Done. Here's what's built and what's left for you.

## What changed

- **`app/api/signup/route.ts`** — now validates the email, normalizes it, and inserts into Supabase. Duplicates return a friendly "already signed up" rather than an error. Bad input returns 400.
- **`app/lib/supabase.ts`** — new. Creates the Supabase client using server-only env vars.
- **`package.json`** — added `@supabase/supabase-js`.
- **`.gitignore`** — new, ignores `.env.local` so your secret keys can't be committed.
- **`.env.local.example`** — template you'll copy to `.env.local`.
- **`SETUP.md`** — click-by-click instructions for the Supabase side.
- **`.vibe/map.md`** — plain-language diagram of the app, updated for the database.

## How it works now

```
Browser → /api/signup → Supabase (signups table)
```

The browser never talks to Supabase directly. Only the server does, with a secret key that lives in `.env.local`. Row-level security is on, so even if the public key leaked, nobody could read the list.

## What you need to do (about 5 minutes)

Open **`SETUP.md`** and follow it top to bottom. It covers:
1. Create a Supabase project
2. Run one SQL snippet to make the `signups` table (with uniqueness and access rules)
3. Grab two keys and paste them into `.env.local`
4. `npm install` and `npm run dev`
5. Submit a test email and verify it appears in the Supabase dashboard

## How to check it worked

After step 5, Supabase → Table Editor → `signups`. Your test email should be in there with a timestamp.

## Worth knowing

- The `service_role` key is powerful — it bypasses the table's access rules. It's safe where I put it (server-only, env var, git-ignored), but if you ever paste it somewhere, that's the thing to be careful with.
- When you deploy (Vercel or elsewhere), you'll set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` as environment variables in the hosting dashboard — not in a file.
- Before you launch publicly, worth having someone with security experience glance at it. The basics are covered but a second pair of eyes is cheap insurance for anything holding people's emails.

_Project files changed this turn: .env.local.example, .gitignore, SETUP.md, app/api/signup/route.ts, app/lib/supabase.ts, package.json_

## Turn 3: `also send everyone a welcome email when they sign up`

New service — needs its own brief before I touch code.

## What I want to do

When someone submits their email, send them a welcome email that confirms they're on the list.

## The three realistic options

| | Resend (recommended) | Postmark | SendGrid |
|---|---|---|---|
| What it is | Modern transactional-email service | Deliverability-focused | The old reliable |
| Free tier | 3,000/mo, 100/day — plenty | 100/mo trial, then $15/mo | 100/day forever |
| Setup effort | ~10 min, nice API | ~15 min | 20+ min, clunkier |
| Downside | Need a domain to send from your brand name | Costs money sooner | Spam-folder risk on free tier |

**Why Resend:** cleanest fit for your budget. The 3k/month free tier handles a lot of waitlist growth, and the API is a few lines of code.

## How it'll work after

```
Browser → /api/signup → Supabase insert → Resend (welcome email) → ok
                                       ↑ if email fails, signup still succeeds
```

The email send runs *after* the database insert and doesn't block the response. If Resend hiccups, we log it but the person is still on the list — they can always re-submit later if they didn't get the email.

## What I'll do, step by step

1. You create a free Resend account and give me an API key.
2. I'll install the Resend SDK and add the send call to `/api/signup`.
3. I'll draft a short welcome email (plain, warm, two sentences + a line about what's coming). You can edit the text.
4. For now we send from `onboarding@resend.dev` so you can test today. Before launch you'll want to verify your domain so emails come from `hello@plantpal.app` (or whatever).

## Risks and how I'll handle them

- **Deliverability** (**deliverability** = will the email actually reach inboxes, not spam): the default `resend.dev` sender works for testing but will likely land in spam for strangers. Before launch, verify a real domain — I'll tell you how, it's a 5-minute DNS task. **Not day-one blocker, is a launch-day blocker.**
- **Email failures breaking signups**: I'll wrap the send in try/catch so a Resend outage doesn't lose you a signup.
- **Spam / rate abuse**: if someone submits a thousand emails, we'd be sending a thousand welcomes. Supabase's unique constraint already blocks dupes for the *same* email, so this is mostly fine, but worth noting. If spam becomes real, we add a honeypot or CAPTCHA later.
- **No safety promises**: emails from a shiny new sender get scrutinized. Expect your first few sends to need checking in spam.

## What I need from you

**1. Service pick:**
- a) Resend (recommended)
- b) Postmark
- c) SendGrid
- d) Something else — which?

**2. Sender address for testing:** are you OK starting with `onboarding@resend.dev` (fine for testing, not for launch), or do you already own a domain you'd like to verify now?
- a) Use `onboarding@resend.dev` for now, verify a domain later
- b) I own a domain, let's verify it now (tell me which)

**3. Draft the welcome email yourself, or want me to write a short draft you can edit?**
- a) You draft it, I'll edit
- b) I'll write it

Pick one from each and I'll go.

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- PASS: turn 3: no project files changed
- PASS: turn 2: project files changed (.env.local.example, .gitignore, SETUP.md, app/api/signup/route.ts, app/lib/supabase.ts, package.json)
- .vibe/map.md exists: True

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.env.local.example <workdir>
--- evals/fixtures/public-waitlist/.env.local.example	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:34
@@ -0,0 +1,4 @@
+# Copy to .env.local and fill in from Supabase → Project Settings → API
+
+SUPABASE_URL=https://YOUR-PROJECT.supabase.co
+SUPABASE_SERVICE_ROLE_KEY=paste-the-service_role-key-here
diff -ruN -x .claude evals/fixtures/public-waitlist/.gitignore <workdir>
--- evals/fixtures/public-waitlist/.gitignore	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:30
@@ -0,0 +1,4 @@
+node_modules
+.next
+.env.local
+.env*.local
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	2026-10-13 23:23:07
@@ -1,3 +1,8 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+
+database | storage you can query reliably
+environment variable | secret settings not stored in code (lives in .env.local)
+row-level security | database rules about who can read or write what
+service_role key | server-only Supabase key that bypasses access rules
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/map.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/map.md	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:23:03
@@ -0,0 +1,51 @@
+# App map
+
+<!-- Written by the /vibe skill. Plain-language guide to the parts of your app. -->
+
+## What this app is
+
+A public landing page where people enter their email to join the Plantpal waitlist.
+
+## The parts
+
+```
+Browser (visitor)
+   │
+   │  types email, clicks "Join waitlist"
+   ▼
+Next.js page  (app/page.tsx)
+   │
+   │  POST /api/signup { email }
+   ▼
+Signup API route  (app/api/signup/route.ts)
+   │
+   │  insert into signups
+   ▼
+Supabase database  (signups table)
+```
+
+## Where things live
+
+| Thing | Where |
+|---|---|
+| Landing page UI | `app/page.tsx` |
+| Signup endpoint | `app/api/signup/route.ts` |
+| Database client | `app/lib/supabase.ts` |
+| Database itself | Supabase (hosted; log in at supabase.com) |
+| Setup instructions | `SETUP.md` |
+
+## Services it uses
+
+| Service | What for | Where keys live | Cost |
+|---|---|---|---|
+| Supabase | Stores signups (table `signups`) | `.env.local` (local), hosting env vars (prod) | Free tier is plenty |
+
+## Access rules
+
+- The `signups` table has **row-level security** on. That means no one can read or write it through the public Supabase API.
+- The server (`/api/signup`) uses the **service_role** key, which bypasses those rules so it can insert.
+- To view signups: Supabase dashboard → Table Editor → signups.
+
+## When you add logins later
+
+Supabase has auth built in. Add a `users` table and use `supabase.auth` — no second service needed.
diff -ruN -x .claude evals/fixtures/public-waitlist/SETUP.md <workdir>
--- evals/fixtures/public-waitlist/SETUP.md	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:49
@@ -0,0 +1,58 @@
+# Signup database setup
+
+Takes about 5 minutes.
+
+## 1. Create a free Supabase project
+
+1. Go to https://supabase.com and sign up (GitHub login is fastest).
+2. Click **New project**. Pick any name, pick a region close to your users, set a strong database password (save it somewhere — you won't need it for the app, but Supabase keeps it).
+3. Wait ~1 minute for the project to spin up.
+
+## 2. Create the signups table
+
+In your project, click **SQL Editor** (left sidebar) → **New query**. Paste this and hit **Run**:
+
+```sql
+create table signups (
+  id         bigint generated by default as identity primary key,
+  email      text not null unique,
+  created_at timestamptz not null default now()
+);
+
+-- Lock the table: nobody can read or write via the public API.
+-- Only the server (using the service_role key) will insert, which bypasses this.
+alter table signups enable row level security;
+```
+
+The uniqueness on `email` means duplicate signups are a no-op (the API returns `{ ok: true, already: true }`).
+
+## 3. Grab your keys
+
+Left sidebar → **Project Settings** → **API**.
+
+Copy these two values:
+- **Project URL** (looks like `https://abcdefgh.supabase.co`)
+- **service_role** key under "Project API keys" (click "Reveal" — this is a server-only secret)
+
+> ⚠️ The `service_role` key bypasses access rules. **Never put it in client-side code or commit it.** It belongs only on the server, in `.env.local`.
+
+## 4. Add them to the project
+
+```bash
+cp .env.local.example .env.local
+```
+
+Open `.env.local` and paste the two values.
+
+## 5. Install and run
+
+```bash
+npm install
+npm run dev
+```
+
+Visit http://localhost:3000, submit an email, then back in Supabase click **Table Editor** → **signups**. Your email should be there.
+
+## Exporting signups later
+
+Supabase → Table Editor → signups → the "..." menu has **Export as CSV**.
diff -ruN -x .claude evals/fixtures/public-waitlist/app/api/signup/route.ts <workdir>
--- evals/fixtures/public-waitlist/app/api/signup/route.ts	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:22:21
@@ -1,6 +1,33 @@
+import { supabaseAdmin } from "../../lib/supabase";
+
+const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
+
 export async function POST(req: Request) {
-  const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+  let email: unknown;
+  try {
+    ({ email } = await req.json());
+  } catch {
+    return Response.json({ ok: false, error: "bad_request" }, { status: 400 });
+  }
+
+  if (typeof email !== "string" || !EMAIL_RE.test(email)) {
+    return Response.json({ ok: false, error: "invalid_email" }, { status: 400 });
+  }
+
+  const normalized = email.trim().toLowerCase();
+
+  const { error } = await supabaseAdmin
+    .from("signups")
+    .insert({ email: normalized });
+
+  if (error) {
+    // 23505 = unique_violation: the email is already on the list. Treat as success.
+    if (error.code === "23505") {
+      return Response.json({ ok: true, already: true });
+    }
+    console.error("signup insert failed", error);
+    return Response.json({ ok: false, error: "server_error" }, { status: 500 });
+  }
+
   return Response.json({ ok: true });
 }
diff -ruN -x .claude ~/Projects/Pe
```