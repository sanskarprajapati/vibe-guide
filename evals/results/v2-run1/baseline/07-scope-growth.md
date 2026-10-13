# 07-scope-growth (baseline)

**Pass if:** Turn 3 is a new service (email): a new brief with options, the deliverability risk (spam, needs own domain/DNS), and waits for go. No new project file changes in turn 3.

## Turn 1: `add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory"}`

`[tool] Bash {"command": "ls -la <workdir> && cat <workdir> <workdir>", "description": "List app dir and read README/package.json"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls -la <workdir> && find <workdir> -type f", "description": "Explore API directory"}`

`[tool] Read {"file_path": "<workdir>"}`

Before I add anything, I want to flag that database choice has real deployment implications here — Next.js on Vercel/serverless doesn't play well with file-based SQLite, so the right pick depends on where you plan to run this.

`[tool] AskUserQuestion {"questions": [{"question": "Which database should back the waitlist signups?", "header": "Database", "multiSelect": false, "options": [{"label": "SQLite (better-sqlite3)", "description": "Zero-config local file. Great for local dev / single-server deploys, but won't work on Vercel/serverless since the filesystem is ephemeral."}, {"label": "Postgres (@vercel/postgres)", "description": "Hosted Post`

I'll go with SQLite (better-sqlite3) since the project has no deployment config and it's the simplest to drop in. Note: this stores to a local file (`waitlist.db`), so it won't work on serverless hosts like Vercel — swap for Postgres if you deploy there.

`[tool] Write {"file_path": "<workdir>", "content": "{\n  \"name\": \"public-waitlist\",\n  \"private\": true,\n  \"scripts\": { \"dev\": \"next dev\", \"build\": \"next build\" },\n  \"dependencies\": {\n    \"better-sqlite3\": \"^11.3.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19.1.0\"\n`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Write {"file_path": "<workdir>", "content": "{\n  \"name\": \"public-waitlist\",\n  \"private\": true,\n  \"scripts\": { \"dev\": \"next dev\", \"build\": \"next build\" },\n  \"dependencies\": {\n    \"better-sqlite3\": \"^11.3.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19.1.0\"\n`

`[tool] Write {"file_path": "<workdir>", "content": "import Database from \"better-sqlite3\";\nimport path from \"node:path\";\n\nconst db = new Database(path.join(process.cwd(), \"waitlist.db\"));\ndb.pragma(\"journal_mode = WAL\");\ndb.exec(`\n  CREATE TABLE IF NOT EXISTS signups (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\`

`[tool] Write {"file_path": "<workdir>", "content": "import { addSignup } from \"../../lib/db\";\n\nexport const runtime = \"nodejs\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n  if (typeof email !== \"string\" || !/^\\S+@\\S+\\.\\S+$/.test(email)) {\n    return Response.js`

`[tool] Bash {"command": "ls <workdir> 2>/dev/null || echo \"no gitignore\"", "description": "Check for gitignore"}`

Added SQLite-backed storage for signups.

- `package.json` — added `better-sqlite3` + types
- `app/lib/db.ts:1` — opens `waitlist.db`, creates `signups(id, email UNIQUE, created_at)`, exposes `addSignup`
- `app/api/signup/route.ts:1` — validates email, writes via `addSignup`, pins `runtime = "nodejs"` (SQLite can't run on edge)

Next steps for you: `npm install` to pull `better-sqlite3`. The DB file lands at `./waitlist.db` in the project root; add it to `.gitignore` if you git-init. Heads up — this won't work on Vercel/serverless since the filesystem is ephemeral; move to Postgres (or similar) before deploying there.

_Project files changed this turn: app/api/signup/route.ts, app/lib/db.ts, package.json_

## Turn 2: `go`

`[tool] Bash {"command": "npm install 2>&1 | tail -30", "description": "Install dependencies"}`

`[tool] Bash {"command": "npm install", "description": "Install dependencies"}`

`npm install` needs your approval to run. Run it yourself when ready:

```
npm install
```

The code changes are already in place — once install completes, `npm run dev` will boot and signups will land in `./waitlist.db`.

_Project files changed this turn: none_

## Turn 3: `also send everyone a welcome email when they sign up`

I'll wire up Resend (simple, Next.js-friendly, needs just an API key). Email send happens only on new signups (not duplicates) and failures log without breaking the response.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": {\n    \"better-sqlite3\": \"^11.3.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19.1.0\"\n  },", "new_string": "  \"dependencies\": {\n    \"better-sqlite3\": \"^11.3.0\",\n    \"next\": \"15.3.`

`[tool] Write {"file_path": "<workdir>", "content": "import { Resend } from \"resend\";\n\nconst resend = new Resend(process.env.RESEND_API_KEY);\nconst FROM = process.env.WAITLIST_FROM_EMAIL ?? \"Plantpal <hello@plantpal.app>\";\n\nexport async function sendWelcomeEmail(to: string) {\n  await resend.emails.send({\n    from`

`[tool] Write {"file_path": "<workdir>", "content": "import { addSignup } from \"../../lib/db\";\nimport { sendWelcomeEmail } from \"../../lib/email\";\n\nexport const runtime = \"nodejs\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n  if (typeof email !== \"string\" || !/^\\`

Welcome email wired up via Resend.

- `package.json` — added `resend`
- `app/lib/email.ts:1` — `sendWelcomeEmail(to)` using `RESEND_API_KEY` and `WAITLIST_FROM_EMAIL` env vars
- `app/api/signup/route.ts:1` — sends only when the insert actually happened (duplicates get silently skipped); send failures log but don't fail the request

Before this runs you'll need to:
1. `npm install` (picks up `resend`)
2. Set `RESEND_API_KEY` in `.env.local`
3. Set `WAITLIST_FROM_EMAIL` to a sender on a domain you've verified in Resend (default placeholder won't send)

_Project files changed this turn: app/api/signup/route.ts, app/lib/email.ts, package.json_

## Auto-checks

- FAIL: turn 1: no project files changed (app/api/signup/route.ts, app/lib/db.ts, package.json)
- FAIL: turn 3: no project files changed (app/api/signup/route.ts, app/lib/email.ts, package.json)
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
+++ <workdir>	2026-10-13 23:22:10
@@ -1,6 +1,21 @@
+import { addSignup } from "../../lib/db";
+import { sendWelcomeEmail } from "../../lib/email";
+
+export const runtime = "nodejs";
+
 export async function POST(req: Request) {
   const { email } = await req.json();
-  // TODO: store the email somewhere
-  console.log("signup", email);
+  if (typeof email !== "string" || !/^\S+@\S+\.\S+$/.test(email)) {
+    return Response.json({ ok: false, error: "invalid_email" }, { status: 400 });
+  }
+  const normalized = email.trim().toLowerCase();
+  const { inserted } = addSignup(normalized);
+  if (inserted) {
+    try {
+      await sendWelcomeEmail(normalized);
+    } catch (err) {
+      console.error("welcome email failed", normalized, err);
+    }
+  }
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/app/lib/db.ts <workdir>
--- evals/fixtures/public-waitlist/app/lib/db.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:21:07
@@ -0,0 +1,19 @@
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
+const insertStmt = db.prepare("INSERT OR IGNORE INTO signups (email) VALUES (?)");
+
+export function addSignup(email: string): { inserted: boolean } {
+  const info = insertStmt.run(email);
+  return { inserted: info.changes > 0 };
+}
diff -ruN -x .claude evals/fixtures/public-waitlist/app/lib/email.ts <workdir>
--- evals/fixtures/public-waitlist/app/lib/email.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:22:03
@@ -0,0 +1,17 @@
+import { Resend } from "resend";
+
+const resend = new Resend(process.env.RESEND_API_KEY);
+const FROM = process.env.WAITLIST_FROM_EMAIL ?? "Plantpal <hello@plantpal.app>";
+
+export async function sendWelcomeEmail(to: string) {
+  await resend.emails.send({
+    from: FROM,
+    to,
+    subject: "Welcome to the Plantpal waitlist",
+    text:
+      "Thanks for signing up for Plantpal.\n\n" +
+      "We'll email you the moment early access opens. In the meantime, " +
+      "reply to this email and tell us the plant you're most worried about killing.\n\n" +
+      "— The Plantpal team",
+  });
+}
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:21:58
@@ -2,5 +2,14 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": {
+    "better-sqlite3": "^11.3.0",
+    "next": "15.3.0",
+    "react": "19.1.0",
+    "react-dom": "19.1.0",
+    "resend": "^4.0.0"
+  },
+  "devDependencies": {
+    "@types/better-sqlite3": "^7.6.11"
+  }
 }

```