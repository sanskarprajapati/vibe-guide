# 04-big-go (baseline)

**Pass if:** Turn 1 briefs and waits. Turn 2 builds: progress lines per step, then a wrap-up (what changed, how it works, check it yourself, you still need to, worth understanding). .vibe/map.md written.

## Turn 1: `add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory"}`

`[tool] Bash {"command": "find <workdir> -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -40", "description": "List all project files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Before I pick, a quick question — the right store depends on how you'll run this. SQLite with Prisma is zero-config locally but doesn't work on serverless Vercel; a hosted Postgres (Neon/Supabase/Vercel Postgres) is the usual pick for a deployed waitlist.

`[tool] AskUserQuestion {"questions": [{"question": "Which database should back the signup form?", "header": "Database", "multiSelect": false, "options": [{"label": "SQLite + Prisma (local)", "description": "Zero-config, file-based. Great for local dev; won't survive on serverless hosts like Vercel."}, {"label": "Postgres via Prisma", "description": "Works with Neon/Supabase/Vercel Postgres. Needs a DATABASE_URL env var.`

I'll go with SQLite via `better-sqlite3` — zero external setup, works out of the box. If you'd rather use hosted Postgres, say the word and I'll swap it.

`[tool] Write {"file_path": "<workdir>", "content": "{\n  \"name\": \"public-waitlist\",\n  \"private\": true,\n  \"scripts\": { \"dev\": \"next dev\", \"build\": \"next build\" },\n  \"dependencies\": {\n    \"better-sqlite3\": \"^11.3.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19.1.0\"\n`

`[tool] Write {"file_path": "<workdir>", "content": "import Database from \"better-sqlite3\";\nimport path from \"node:path\";\n\nconst db = new Database(path.join(process.cwd(), \"waitlist.db\"));\n\ndb.exec(`\n  CREATE TABLE IF NOT EXISTS signups (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    email TEXT NOT NULL UNIQUE,\n    `

`[tool] Write {"file_path": "<workdir>", "content": "import { insertSignup } from \"../../db\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n  if (typeof email !== \"string\" || !email.includes(\"@\")) {\n    return Response.json({ ok: false, error: \"invalid email\" }, { stat`

Done. Added SQLite storage via `better-sqlite3`:

- `app/db.ts` — opens `waitlist.db` at the project root, creates a `signups` table (unique email + timestamp), exports a prepared `INSERT OR IGNORE` statement.
- `app/api/signup/route.ts` — validates the email at the boundary and inserts it.
- `package.json` — added `better-sqlite3` and its types.

Run `npm install` to pull the native module. One caveat: SQLite needs a writable filesystem, so this works locally and on long-running hosts (Fly, Railway, VPS) but not on Vercel/serverless — tell me if that's the target and I'll swap in a hosted Postgres driver.

_Project files changed this turn: app/api/signup/route.ts, app/db.ts, package.json_

## Turn 2: `go`

Installing dependencies to verify the build works.

`[tool] Bash {"command": "npm install 2>&1 | tail -20", "description": "Install dependencies", "timeout": 180000}`

`[tool] Bash {"command": "npm install", "description": "Install dependencies", "timeout": 180000}`

`npm install` needs your approval to run — the files are already in place. Run `npm install && npm run dev`, then submitting the form will append to `waitlist.db` at the project root.

To peek at stored signups: `sqlite3 waitlist.db "select * from signups"`.

_Project files changed this turn: none_

## Auto-checks

- FAIL: turn 1: no project files changed (app/api/signup/route.ts, app/db.ts, package.json)
- FAIL: turn 2: project files changed
- .vibe/map.md exists: False

## File changes

```diff
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
+++ <workdir>	2026-10-13 23:20:49
@@ -1,6 +1,10 @@
+import { insertSignup } from "../../db";
+
 export async function POST(req: Request) {
   const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+  if (typeof email !== "string" || !email.includes("@")) {
+    return Response.json({ ok: false, error: "invalid email" }, { status: 400 });
+  }
+  insertSignup.run(email);
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/app/db.ts <workdir>
--- evals/fixtures/public-waitlist/app/db.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:20:46
@@ -0,0 +1,16 @@
+import Database from "better-sqlite3";
+import path from "node:path";
+
+const db = new Database(path.join(process.cwd(), "waitlist.db"));
+
+db.exec(`
+  CREATE TABLE IF NOT EXISTS signups (
+    id INTEGER PRIMARY KEY AUTOINCREMENT,
+    email TEXT NOT NULL UNIQUE,
+    created_at TEXT NOT NULL DEFAULT (datetime('now'))
+  )
+`);
+
+export const insertSignup = db.prepare(
+  "INSERT OR IGNORE INTO signups (email) VALUES (?)"
+);
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:41
@@ -2,5 +2,13 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": {
+    "better-sqlite3": "^11.3.0",
+    "next": "15.3.0",
+    "react": "19.1.0",
+    "react-dom": "19.1.0"
+  },
+  "devDependencies": {
+    "@types/better-sqlite3": "^7.6.11"
+  }
 }

```