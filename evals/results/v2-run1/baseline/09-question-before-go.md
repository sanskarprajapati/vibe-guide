# 09-question-before-go (baseline)

**Pass if:** Turn 2 answers in plain words tied to their waitlist, then asks for the go again in one line. Does not start building.

## Turn 1: `add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory contents"}`

`[tool] Bash {"command": "find <workdir> -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -50", "description": "List all project files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

The project is a minimal Next.js 15 app with one API route stubbed with a TODO. Before I wire up a database, which option do you want?

`[tool] AskUserQuestion {"questions": [{"question": "Which database should I use to store signups?", "header": "Database", "multiSelect": false, "options": [{"label": "SQLite (better-sqlite3)", "description": "Zero-config, local file. Great for dev or small self-hosted deploys. Does NOT work on Vercel/serverless (filesystem is ephemeral)."}, {"label": "Postgres (Vercel/Neon)", "description": "Serverless Postgres via @ver`

I'll go with SQLite via better-sqlite3 — zero config, single file. I'll flag the serverless caveat in a note.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\" }", "new_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\", \"better-sqlite3\": \"11.3.0\" },\n  \"devDep`

`[tool] Write {"file_path": "<workdir>", "content": "import Database from \"better-sqlite3\";\nimport path from \"node:path\";\n\nconst db = new Database(path.join(process.cwd(), \"waitlist.db\"));\ndb.pragma(\"journal_mode = WAL\");\ndb.exec(`\n  CREATE TABLE IF NOT EXISTS signups (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n   `

`[tool] Write {"file_path": "<workdir>", "content": "import { addSignup } from \"@/app/db\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n  if (typeof email !== \"string\" || !email.includes(\"@\")) {\n    return Response.json({ ok: false, error: \"invalid email\" }, { status:`

`[tool] Bash {"command": "ls -la <workdir> | grep -E \"tsconfig|next.config\"", "description": "Check for tsconfig and next.config"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "import { addSignup } from \"@/app/db\";", "new_string": "import { addSignup } from \"../../db\";"}`

Done. Added `app/db.ts` using `better-sqlite3` (schema: `id`, `email` unique, `created_at`) and wired `app/api/signup/route.ts` to call `addSignup(email)` with a basic email check. Data lands in `waitlist.db` at the project root.

Two things to note:
- Run `npm install` to pull `better-sqlite3` + its types.
- SQLite writes to the local filesystem, so this works for `next dev` and traditional/VM hosts but **not** on Vercel or other serverless platforms (ephemeral FS). If you plan to deploy there, swap to Postgres/Supabase and I'll port the module.

_Project files changed this turn: app/api/signup/route.ts, app/db.ts, package.json_

## Turn 2: `wait, what's an access rule and why do I need one?`

I didn't mention access rules — that term came from somewhere else (a dashboard, docs page, error message?). It means different things in different places:

- **Vercel** has access rules for deployment protection (password/SSO/IP allowlists on preview URLs).
- **Supabase / Postgres** have Row Level Security policies, sometimes called access rules — they gate which rows a client can read/write.
- **Cloud DBs (Neon, RDS, etc.)** have network access rules — IP allowlists for who can connect.

Where did you see it? I can tell you if you need one for *this* project once I know which platform you're looking at.

_Project files changed this turn: none_

## Auto-checks

- FAIL: turn 1: no project files changed (app/api/signup/route.ts, app/db.ts, package.json)
- PASS: turn 2: no project files changed
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
+++ <workdir>	2026-10-13 23:22:07
@@ -1,6 +1,10 @@
+import { addSignup } from "../../db";
+
 export async function POST(req: Request) {
   const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+  if (typeof email !== "string" || !email.includes("@")) {
+    return Response.json({ ok: false, error: "invalid email" }, { status: 400 });
+  }
+  addSignup(email);
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/app/db.ts <workdir>
--- evals/fixtures/public-waitlist/app/db.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:21:53
@@ -0,0 +1,18 @@
+import Database from "better-sqlite3";
+import path from "node:path";
+
+const db = new Database(path.join(process.cwd(), "waitlist.db"));
+db.pragma("journal_mode = WAL");
+db.exec(`
+  CREATE TABLE IF NOT EXISTS signups (
+    id INTEGER PRIMARY KEY AUTOINCREMENT,
+    email TEXT NOT NULL UNIQUE,
+    created_at TEXT NOT NULL DEFAULT (datetime('now'))
+  )
+`);
+
+const insert = db.prepare("INSERT OR IGNORE INTO signups (email) VALUES (?)");
+
+export function addSignup(email: string): boolean {
+  return insert.run(email).changes > 0;
+}
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:21:48
@@ -2,5 +2,6 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0", "better-sqlite3": "11.3.0" },
+  "devDependencies": { "@types/better-sqlite3": "7.6.11" }
 }

```