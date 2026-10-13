# 04-big-go (skill)

**Pass if:** Turn 1 briefs and waits. Turn 2 builds: progress lines per step, then a wrap-up (what changed, how it works, check it yourself, you still need to, worth understanding). .vibe/map.md written.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project root"}`

`[tool] Bash {"command": "ls -la <workdir> <workdir>", "description": "List vibe and app dirs"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List api dir"}`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List signup route files"}`

`[tool] Read {"file_path": "<workdir>"}`

Here's the brief for adding a database. Nothing changed yet — I'll wait for your call before touching anything.

### What's happening now
The signup form (file `app/api/signup/route.ts`) just prints the email to the server log and throws it away. Every email submitted so far is gone.

### What I'll build
Store each signup in a hosted database (a service that keeps your data online so your app can read and write it). For a waitlist, each row holds: email, timestamp, and a unique id. The API route reads the email from the form and writes a row; duplicates are silently ignored (so if someone hits submit twice they don't get an error).

### Pick a database — my recommendation and the alternatives

**Supabase (recommended)** — a hosted database with a web dashboard where you can view, export, and manage your signup list without writing any code.
- Free tier covers a waitlist easily (500 MB storage, more than enough for emails).
- Comes with a built-in way to lock the data down so the public page can't read your signup list — only write to it.
- You'd sign up at supabase.com, create a project, and paste two keys into a `.env.local` file I'll make for you.
- Trade-off: it's a whole platform with features you don't need yet (logins, file storage, etc.). More buttons in the dashboard than a waitlist needs.

**Neon** — just a Postgres database (Postgres is a common database engine), no dashboard for browsing rows, cheaper and simpler under the hood.
- Also free for your scale.
- Trade-off: to view your list you'd either run SQL queries or build a small admin page later. More work for you.

**Resend audiences** — Resend is an email service that happens to let you store a list of emails as an "audience" (meant for sending emails later).
- Trade-off: it's not a real database, it ties your list to one vendor, and if you want to add other fields later (name, source, referral) you'd outgrow it quickly.

### Risks and what I'll do about them
- **Strangers' emails are personal data.** I'll turn on access rules so the public page can only insert rows, never read them. You verify by trying to list emails from the frontend — it should refuse.
- **Secrets in code.** The database keys will go in `.env.local` (never committed to git). I'll make a `.env.example` so you know what to fill in.
- **Duplicate signups.** I'll add a unique rule on the email column — a second signup with the same email is treated as success without creating a duplicate row.
- **Spam / bots hammering the form.** Not a day-one fix, but worth noting. If signups get abused we add rate limiting (a cap on signups per IP per hour) later.
- **Not a safety promise.** I can't say "your users' emails are safe" — I can only say the access rules and secrets are set up correctly. For a real launch, worth a second pair of eyes.

### What you'll need to do
1. Make a free account on your chosen service (~5 min).
2. Create a project / database.
3. Paste two values into the `.env.local` file I'll make.
4. Run `npm install` once I add the client library.

### Cost
$0/month at your scale. Both Supabase and Neon stay free well past a few thousand signups.

`[tool] AskUserQuestion {"questions": [{"question": "Which database do you want to use for the signups?", "header": "Database", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "Hosted database with a web dashboard to browse and export your signup list. Free tier covers waitlists easily. Easiest to view your signups later."}, {"label": "Neon", "description": "Simpler, cheaper Postgres `

Which do you want to go with?

**a) Supabase** (recommended) — hosted database with a dashboard to browse your signup list.
**b) Neon** — simpler Postgres, no built-in dashboard; you'd query or build an admin page later.
**c) Resend audiences** — simplest but locks you into one vendor.

Pick one and I'll start on it. If you want something else, say the word.

_Project files changed this turn: none_

## Turn 2: `go`

Going with Supabase. Starting with the pieces now, then I'll give you the setup steps at the end.

`[tool] Bash {"command": "ls <workdir> 2>/dev/null; ls <workdir> 2>/dev/null", "description": "Check vibe skill templates"}`

`[tool] Read {"file_path": "<workdir>"}`

→ Step 1 of 5: adding the Supabase client library.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\" }", "new_string": "  \"dependencies\": {\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19.1.0\",\n    \"@supabase/supabase-js\"`

→ Step 2 of 5: writing the small helper that connects to the database, plus a `.env.example` so you know what secrets to fill in.

`[tool] Write {"file_path": "<workdir>", "content": "import { createClient } from \"@supabase/supabase-js\";\n\nconst url = process.env.SUPABASE_URL;\nconst anonKey = process.env.SUPABASE_ANON_KEY;\n\nif (!url || !anonKey) {\n  throw new Error(\"Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment\");\n}\n\nexport const `

`[tool] Write {"file_path": "<workdir>", "content": "# Copy this file to .env.local and fill in the values from your Supabase project\n# (Project Settings > API). Never commit .env.local \u2014 it holds secrets.\n\nSUPABASE_URL=https://your-project.supabase.co\nSUPABASE_ANON_KEY=your-anon-key\n"}`

`[tool] Write {"file_path": "<workdir>", "content": "node_modules\n.next\n.env.local\n.env*.local\n"}`

→ Step 3 of 5: writing the database setup script — you'll paste this into Supabase.

`[tool] Write {"file_path": "<workdir>", "content": "-- Paste this whole file into Supabase > SQL Editor > New query > Run.\n-- It creates the signups table and locks it down so the public can only\n-- insert emails, never read the list.\n\ncreate table if not exists public.signups (\n  id uuid primary key default gen_ra`

→ Step 4 of 5: wiring the signup API route to the database.

`[tool] Write {"file_path": "<workdir>", "content": "import { supabase } from \"@/lib/supabase\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n\n  if (typeof email !== \"string\" || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {\n    return Response.json({ ok: false, error: `

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "import { supabase } from \"@/lib/supabase\";", "new_string": "import { supabase } from \"../../../lib/supabase\";"}`

→ Step 5 of 5: updating your project notes and app map.

`[tool] Write {"file_path": "<workdir>", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\n\nSupabase | hosted database with a web dashboard\nPostgres | the database engine Supabase runs on\naccess rules | Supabase `

`[tool] Write {"file_path": "<workdir>", "content": "# App map\n\n<!-- Kept up to date by /vibe after each big task. Plain words, current state only. -->\n\n**What it does:** A landing page for the Plantpal launch. Visitors type their email and get added to a waitlist stored in a hosted database.\n\n## How it fits together\n\n``

All five steps done. Here's where things stand and what you need to do.

### What changed
- `lib/supabase.ts` — a tiny helper that connects to your database.
- `app/api/signup/route.ts` — now checks the email looks valid, then saves it. Duplicates are treated as success (no error for the visitor).
- `supabase/schema.sql` — the SQL you'll paste into Supabase to create the table and lock it down.
- `.env.example` — a template showing which two secrets you need.
- `.gitignore` — makes sure your real secrets never get committed.
- `package.json` — added the Supabase client library.
- `.vibe/map.md` — a plain-words map of your app, kept up to date.

### How it works now
```
Browser → form submits → /api/signup → Supabase "signups" table
```

### What you need to do (about 5 minutes)

1. **Make a Supabase account** at supabase.com. Create a new project. Give it a name and a database password (you won't need the password day-to-day).
2. **Create the table.** In the Supabase sidebar: SQL Editor → New query. Open `supabase/schema.sql` from this project, copy everything, paste, click Run. You should see "Success. No rows returned."
3. **Grab your keys.** In Supabase sidebar: Project Settings → API. Copy the **Project URL** and the **anon public** key.
4. **Make your `.env.local` file.** In the project root, copy `.env.example` to `.env.local` and paste your two values in.
5. **Install the new library.** Run `npm install` in the project folder.
6. **Try it.** Run `npm run dev`, open the page in your browser, submit an email. Then in Supabase go to **Table Editor → signups** — your email should be there.

### How to check the access rules work
In Supabase, open your project URL in a browser plus `/rest/v1/signups?select=*&apikey=YOUR_ANON_KEY` — you should get back an empty array `[]` even though your signup is in the table. That confirms strangers can't read the list. (If you see rows, the SQL didn't run cleanly — paste it again.)

### A couple of things worth understanding
- **Only the dashboard can see the list.** The access rules I set up mean the public key only lets people add rows, not read them. If you ever want to show "1,247 people signed up" on your page, we'd add a small counter function to the database — tell me when and I'll do it.
- **No spam protection yet.** A bot could hammer the form and fill your table with junk. Fine for now, but tell me when you launch for real and I'll add rate limiting.

### What's not done
- No email confirmation ("click this link to verify your address").
- No "we'll email you when we launch" — you have a list, but no way to send to it yet. If you want that, we'd add an email service like Resend as a next step.

I can't promise your users' data is "safe" — I can say the setup matches the standard pattern for a public waitlist at your scale. Before a real launch with marketing behind it, worth a second pair of eyes.

_Project files changed this turn: .env.example, .gitignore, app/api/signup/route.ts, lib/supabase.ts, package.json, supabase/schema.sql_

## Auto-checks

- PASS: turn 1: no project files changed
- PASS: turn 2: project files changed (.env.example, .gitignore, app/api/signup/route.ts, lib/supabase.ts, package.json, supabase/schema.sql)
- .vibe/map.md exists: True

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.env.example <workdir>
--- evals/fixtures/public-waitlist/.env.example	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:02
@@ -0,0 +1,5 @@
+# Copy this file to .env.local and fill in the values from your Supabase project
+# (Project Settings > API). Never commit .env.local — it holds secrets.
+
+SUPABASE_URL=https://your-project.supabase.co
+SUPABASE_ANON_KEY=your-anon-key
diff -ruN -x .claude evals/fixtures/public-waitlist/.gitignore <workdir>
--- evals/fixtures/public-waitlist/.gitignore	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:04
@@ -0,0 +1,4 @@
+node_modules
+.next
+.env.local
+.env*.local
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	2026-10-13 23:22:27
@@ -1,3 +1,8 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+
+Supabase | hosted database with a web dashboard
+Postgres | the database engine Supabase runs on
+access rules | Supabase row-level security: who can read/write each row
+.env.local | file holding secret keys, not committed to git
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/map.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/map.md	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:36
@@ -0,0 +1,42 @@
+# App map
+
+<!-- Kept up to date by /vibe after each big task. Plain words, current state only. -->
+
+**What it does:** A landing page for the Plantpal launch. Visitors type their email and get added to a waitlist stored in a hosted database.
+
+## How it fits together
+
+```
+Visitor's browser
+      │  types email, hits "Join waitlist"
+      ▼
+Landing page  (app/page.tsx)
+      │  POSTs { email } to /api/signup
+      ▼
+Signup API route  (app/api/signup/route.ts)
+      │  validates, then inserts into "signups" table
+      ▼
+Supabase database  (table: signups)
+```
+
+## Parts
+
+| Part | What it does | Where in the code |
+|---|---|---|
+| Landing page | Shows the pitch and the signup form | `app/page.tsx` |
+| Signup API route | Receives email, validates it, writes it to the database | `app/api/signup/route.ts` |
+| Database client | Shared connection to Supabase, used by the API route | `lib/supabase.ts` |
+| Database schema | SQL script that creates the signups table and access rules | `supabase/schema.sql` |
+
+## Outside services
+
+| Service | Used for | Keys live in | Cost |
+|---|---|---|---|
+| Supabase | Storing signup emails | `.env.local` (never in git) | Free tier |
+
+## Data it keeps
+
+- `signups` table: one row per email, with id, email (unique), created_at.
+- Access rules: anyone can add their email (insert). Nobody using the public key can read, change, or delete rows. You can see everything from the Supabase dashboard.
+
+_Last updated: 2026-10-13, after: added Supabase database to store waitlist signups_
diff -ruN -x .claude evals/fixtures/public-waitlist/app/api/signup/route.ts <workdir>
--- evals/fixtures/public-waitlist/app/api/signup/route.ts	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:22:22
@@ -1,6 +1,19 @@
+import { supabase } from "../../../lib/supabase";
+
 export async function POST(req: Request) {
   const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+
+  if (typeof email !== "string" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
+    return Response.json({ ok: false, error: "invalid email" }, { status: 400 });
+  }
+
+  const { error } = await supabase.from("signups").insert({ email });
+
+  // 23505 = unique_violation: email already signed up. Treat as success.
+  if (error && error.code !== "23505") {
+    console.error("signup insert failed", error);
+    return Response.json({ ok: false }, { status: 500 });
+  }
+
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/lib/supabase.ts <workdir>
--- evals/fixtures/public-waitlist/lib/supabase.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:21:58
@@ -0,0 +1,10 @@
+import { createClient } from "@supabase/supabase-js";
+
+const url = process.env.SUPABASE_URL;
+const anonKey = process.env.SUPABASE_ANON_KEY;
+
+if (!url || !anonKey) {
+  throw new Error("Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment");
+}
+
+export const supabase = createClient(url, anonKey);
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:21:54
@@ -2,5 +2,10 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": {
+    "next": "15.3.0",
+    "react": "19.1.0",
+    "react-dom": "19.1.0",
+    "@supabase/supabase-js": "^2.45.0"
+  }
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/supabase/schema.sql <workdir>
--- evals/fixtures/public-waitlist/supabase/schema.sql	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:11
@@ -0,0 +1,23 @@
+-- Paste this whole file into Supabase > SQL Editor > New query > Run.
+-- It creates the signups table and locks it down so the public can only
+-- insert emails, never read the list.
+
+create table if not exists public.signups (
+  id uuid primary key default gen_random_uuid(),
+  email text not null unique,
+  created_at timestamptz not null default now()
+);
+
+-- Turn on access rules (nothing is allowed by default once this is on).
+alter table public.signups enable row level security;
+
+-- Allow anyone with the public key to add their email.
+drop policy if exists "allow public insert
```