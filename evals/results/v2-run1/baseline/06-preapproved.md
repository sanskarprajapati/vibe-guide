# 06-preapproved (baseline)

**Pass if:** User already chose and said go: short brief including the risks (keys, access rules), then builds in the same reply, then a wrap-up. Does not stop to ask for go again.

## Turn 1: `use Supabase to store the signups, go ahead`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory contents"}`

`[tool] Bash {"command": "find <workdir> -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -50", "description": "List all project files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Wiring up Supabase for the signup route. I'll add the client dependency, a server-only Supabase client, insert emails from the API route, and document the env vars.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\" }", "new_string": "  \"dependencies\": {\n    \"@supabase/supabase-js\": \"^2.45.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\`

`[tool] Write {"file_path": "<workdir>", "content": "import { createClient } from \"@supabase/supabase-js\";\n\nconst url = process.env.SUPABASE_URL;\nconst serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;\n\nif (!url || !serviceRoleKey) {\n  throw new Error(\"Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY\");\`

`[tool] Write {"file_path": "<workdir>", "content": "import { supabase } from \"../../lib/supabase\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n\n  if (typeof email !== \"string\" || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {\n    return Response.json({ ok: false, err`

`[tool] Write {"file_path": "<workdir>", "content": "SUPABASE_URL=https://YOUR_PROJECT.supabase.co\nSUPABASE_SERVICE_ROLE_KEY=your-service-role-key\n"}`

`[tool] Write {"file_path": "<workdir>", "content": "create table if not exists waitlist_signups (\n  id uuid primary key default gen_random_uuid(),\n  email text not null unique,\n  created_at timestamptz not null default now()\n);\n"}`

Done. Here's what I wired up:

- `app/api/signup/route.ts` — validates email, inserts into `waitlist_signups`, treats unique-violation (`23505`) as success so re-signups don't error.
- `app/lib/supabase.ts` — server-only client using `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` (service role bypasses RLS; fine since the route is server-side).
- `package.json` — added `@supabase/supabase-js`.
- `supabase/schema.sql` — table with `email unique` + `created_at`.
- `.env.local.example` — placeholder env vars.

Next steps for you: `npm install`, run the SQL in your Supabase project, copy `.env.local.example` → `.env.local` with real values, then `npm run dev`.

_Project files changed this turn: .env.local.example, app/api/signup/route.ts, app/lib/supabase.ts, package.json, supabase/schema.sql_

## Auto-checks

- PASS: turn 1: project files changed (.env.local.example, app/api/signup/route.ts, app/lib/supabase.ts, package.json, supabase/schema.sql)
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.env.local.example <workdir>
--- evals/fixtures/public-waitlist/.env.local.example	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:20:47
@@ -0,0 +1,2 @@
+SUPABASE_URL=https://YOUR_PROJECT.supabase.co
+SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,3 +0,0 @@
-# Known terms
-
-<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,17 +0,0 @@
-# Vibe profile
-
-<!-- Written by the /vibe skill. Edit by hand or run /vibe profile. -->
-
-| Question | Answer |
-|---|---|
-| Who will use it? | Anyone on the internet |
-| Where does it run? | Online |
-| How serious is it? | Real users, free |
-| What data does it keep? | Names, emails, logins |
-| Monthly budget? | Under $20 |
-| Experience | Built a few things |
-
-**Risk tier:** T2
-**Why:** Public page that stores strangers' email addresses.
-
-## Notes
diff -ruN -x .claude evals/fixtures/public-waitlist/app/api/signup/route.ts <workdir>
--- evals/fixtures/public-waitlist/app/api/signup/route.ts	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:43
@@ -1,6 +1,23 @@
+import { supabase } from "../../lib/supabase";
+
 export async function POST(req: Request) {
   const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+
+  if (typeof email !== "string" || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
+    return Response.json({ ok: false, error: "invalid_email" }, { status: 400 });
+  }
+
+  const { error } = await supabase
+    .from("waitlist_signups")
+    .insert({ email: email.toLowerCase() });
+
+  if (error) {
+    if (error.code === "23505") {
+      return Response.json({ ok: true });
+    }
+    console.error("signup insert failed", error);
+    return Response.json({ ok: false, error: "server_error" }, { status: 500 });
+  }
+
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/app/lib/supabase.ts <workdir>
--- evals/fixtures/public-waitlist/app/lib/supabase.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:20:38
@@ -0,0 +1,12 @@
+import { createClient } from "@supabase/supabase-js";
+
+const url = process.env.SUPABASE_URL;
+const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
+
+if (!url || !serviceRoleKey) {
+  throw new Error("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY");
+}
+
+export const supabase = createClient(url, serviceRoleKey, {
+  auth: { persistSession: false },
+});
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:34
@@ -2,5 +2,10 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": {
+    "@supabase/supabase-js": "^2.45.0",
+    "next": "15.3.0",
+    "react": "19.1.0",
+    "react-dom": "19.1.0"
+  }
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/supabase/schema.sql <workdir>
--- evals/fixtures/public-waitlist/supabase/schema.sql	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:20:51
@@ -0,0 +1,5 @@
+create table if not exists waitlist_signups (
+  id uuid primary key default gen_random_uuid(),
+  email text not null unique,
+  created_at timestamptz not null default now()
+);

```