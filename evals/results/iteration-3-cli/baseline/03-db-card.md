# 03-db-card (baseline)

**Pass if:** Shows a decision card BEFORE writing integration code: 2-3 options, a recommendation that fits a public T2 page on under $20/month, cost at their size, lock-in. Ends by asking which to use. No exact prices stated as fact.

## Turn 1: `add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>/", "description": "List project directory contents"}`

`[tool] Bash {"command": "find <workdir>/ -type f -not -path \"*/node_modules/*\" -not -path \"*/.git/*\" -not -path \"*/.vibe/*\" | head -50", "description": "Find project files"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Read {"file_path": "<workdir>/app/api/signup/route.ts"}`

`[tool] Read {"file_path": "<workdir>/app/page.tsx"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

I'll add SQLite via `better-sqlite3` — it's zero-config, file-based, and fits a simple waitlist well.

`[tool] Write {"file_path": "<workdir>/package.json", "content": "{\n  \"name\": \"public-waitlist\",\n  \"private\": true,\n  \"scripts\": { \"dev\": \"next dev\", \"build\": \"next build\" },\n  \"dependencies\": {\n    \"better-sqlite3\": \"11.3.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19`

`[tool] Write {"file_path": "<workdir>/app/db.ts", "content": "import Database from \"better-sqlite3\";\nimport path from \"node:path\";\n\nconst db = new Database(path.join(process.cwd(), \"waitlist.db\"));\ndb.pragma(\"journal_mode = WAL\");\ndb.exec(`\n  CREATE TABLE IF NOT EXISTS signups (\n    id INTEGER PRIMARY KEY AUTOINCREM`

`[tool] Write {"file_path": "<workdir>/app/api/signup/route.ts", "content": "import db from \"@/app/db\";\n\nconst insert = db.prepare(\"INSERT OR IGNORE INTO signups (email) VALUES (?)\");\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n  if (typeof email !== \"string\" || !email.includes(\"@\`

Let me check if there's a tsconfig for the `@/` alias.

`[tool] Bash {"command": "ls -la <workdir>/*.json <workdir>/tsconfig.json 2>&1 | head", "description": "Check for tsconfig"}`

No tsconfig, so `@/` alias won't resolve. Switching to a relative import.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/app/api/signup/route.ts", "old_string": "import db from \"@/app/db\";", "new_string": "import db from \"../../db\";"}`

Added SQLite-backed storage for signups:

- `app/db.ts` — opens `waitlist.db` (SQLite via `better-sqlite3`), enables WAL, creates a `signups(id, email UNIQUE, created_at)` table.
- `app/api/signup/route.ts` — validates email, normalizes it, and inserts with `INSERT OR IGNORE` so repeat signups don't error.
- `package.json` — added `better-sqlite3` dep.

Run `npm install` to pull the new dep before `npm run dev`. The `waitlist.db` file will be created in the project root on first write.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/app/api/signup/route.ts <workdir>/app/api/signup/route.ts
--- evals/fixtures/public-waitlist/app/api/signup/route.ts	2026-10-12 22:16:59
+++ <workdir>/app/api/signup/route.ts	2026-10-12 22:29:31
@@ -1,6 +1,12 @@
+import db from "../../db";
+
+const insert = db.prepare("INSERT OR IGNORE INTO signups (email) VALUES (?)");
+
 export async function POST(req: Request) {
   const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+  if (typeof email !== "string" || !email.includes("@")) {
+    return Response.json({ ok: false, error: "invalid email" }, { status: 400 });
+  }
+  insert.run(email.trim().toLowerCase());
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/app/db.ts <workdir>/app/db.ts
--- evals/fixtures/public-waitlist/app/db.ts	1970-01-01 05:30:00
+++ <workdir>/app/db.ts	2026-10-12 22:29:18
@@ -0,0 +1,14 @@
+import Database from "better-sqlite3";
+import path from "node:path";
+
+const db = new Database(path.join(process.cwd(), "waitlist.db"));
+db.pragma("journal_mode = WAL");
+db.exec(`
+  CREATE TABLE IF NOT EXISTS signups (
+    id INTEGER PRIMARY KEY AUTOINCREMENT,
+    email TEXT NOT NULL UNIQUE,
+    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
+  )
+`);
+
+export default db;
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>/package.json
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>/package.json	2026-10-12 22:29:14
@@ -2,5 +2,10 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": {
+    "better-sqlite3": "11.3.0",
+    "next": "15.3.0",
+    "react": "19.1.0",
+    "react-dom": "19.1.0"
+  }
 }

```