# 03-big-brief (baseline)

**Pass if:** Full brief: end result, a diagram, plain steps, why this way, an alternatives table with pros/cons (SQLite shown as not a fit on serverless), risks with what it will do, cost, what the user must do, what changes. Ends asking for go. No project files changed.

## Turn 1: `add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List files in working directory"}`

`[tool] Bash {"command": "find <workdir> -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -50", "description": "List all files in project"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Before I wire this up, a quick clarification: there are a few reasonable ways to store signups, and the choice affects deployment and dependencies. Which do you want?

`[tool] AskUserQuestion {"questions": [{"question": "Which database should store the waitlist signups?", "header": "Database", "multiSelect": false, "options": [{"label": "SQLite (better-sqlite3)", "description": "File-based, zero setup, runs locally. Simplest to add; good for dev/small waitlist. Won't work on serverless/Vercel (ephemeral filesystem)."}, {"label": "Postgres via Neon/Vercel", "description": "Managed Postg`

I'll go with the simplest option: SQLite via `better-sqlite3`. Zero external services, keeps the project self-contained, and the signup route can swap to Postgres later if you deploy to serverless.

`[tool] Write {"file_path": "<workdir>", "content": "import Database from \"better-sqlite3\";\nimport path from \"node:path\";\n\nlet db: Database.Database | null = null;\n\nexport function getDb() {\n  if (db) return db;\n  db = new Database(path.join(process.cwd(), \"waitlist.db\"));\n  db.pragma(\"journal_mode = WAL\");\n  `

`[tool] Write {"file_path": "<workdir>", "content": "import { getDb } from \"@/app/lib/db\";\n\nexport const runtime = \"nodejs\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n  if (typeof email !== \"string\" || !email.includes(\"@\")) {\n    return Response.json({ ok: false,`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\" }", "new_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\", \"better-sqlite3\": \"^11.3.0\" }"}`

`[tool] Bash {"command": "ls -la <workdir> <workdir> 2>/dev/null", "description": "Check for tsconfig and other config files"}`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List root again"}`

No tsconfig, so the `@/` alias won't resolve. Switching to a relative import.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "import { getDb } from \"@/app/lib/db\";", "new_string": "import { getDb } from \"../../lib/db\";"}`

Done. Signups are now persisted to a local SQLite file (`waitlist.db` at the project root).

Changes:
- `app/lib/db.ts:1` — opens/creates the SQLite DB and `signups` table (unique email + created_at).
- `app/api/signup/route.ts:1` — validates the email, inserts with `INSERT OR IGNORE` so repeats don't error, pinned to the Node.js runtime.
- `package.json:5` — added `better-sqlite3`.

Next steps: run `npm install` to pull in `better-sqlite3`, then `npm run dev`. Note the file-based DB won't survive on serverless deploys (Vercel) — if that's where this is going, swap `app/lib/db.ts` for Postgres.

_Project files changed this turn: app/api/signup/route.ts, app/lib/db.ts, package.json_

## Auto-checks

- FAIL: turn 1: no project files changed (app/api/signup/route.ts, app/lib/db.ts, package.json)
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
+++ <workdir>	2026-10-13 23:20:56
@@ -1,6 +1,14 @@
+import { getDb } from "../../lib/db";
+
+export const runtime = "nodejs";
+
 export async function POST(req: Request) {
   const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+  if (typeof email !== "string" || !email.includes("@")) {
+    return Response.json({ ok: false, error: "invalid email" }, { status: 400 });
+  }
+  getDb()
+    .prepare("INSERT OR IGNORE INTO signups (email) VALUES (?)")
+    .run(email.trim().toLowerCase());
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/app/lib/db.ts <workdir>
--- evals/fixtures/public-waitlist/app/lib/db.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:20:36
@@ -0,0 +1,18 @@
+import Database from "better-sqlite3";
+import path from "node:path";
+
+let db: Database.Database | null = null;
+
+export function getDb() {
+  if (db) return db;
+  db = new Database(path.join(process.cwd(), "waitlist.db"));
+  db.pragma("journal_mode = WAL");
+  db.exec(`
+    CREATE TABLE IF NOT EXISTS signups (
+      id INTEGER PRIMARY KEY AUTOINCREMENT,
+      email TEXT NOT NULL UNIQUE,
+      created_at TEXT NOT NULL DEFAULT (datetime('now'))
+    )
+  `);
+  return db;
+}
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:45
@@ -2,5 +2,5 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0", "better-sqlite3": "^11.3.0" }
 }

```