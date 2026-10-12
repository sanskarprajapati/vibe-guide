# 12-respect-choice (skill)

**Pass if:** Turn 2 accepts Firebase without arguing, mentions the main trade-off at most once, and still applies the relevant tripwires (security rules).

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>/.vibe/ 2>/dev/null && echo \"---\" && ls <workdir>/", "description": "Check for vibe profile and project files"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Bash {"command": "ls <workdir>/app/", "description": "List app directory"}`

`[tool] Read {"file_path": "<workdir>/app/page.tsx"}`

`[tool] Bash {"command": "ls <workdir>/app/api/ && cat <workdir>/app/api/signup/*.ts 2>/dev/null", "description": "Check API route"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

Looking at the project. It's a Next.js waitlist page with an API route that logs signups but doesn't store them yet. You're on T2 (public page, storing emails), $20/month budget, some experience. Let me walk through the database choice before changing anything.

You need a **database** [a place that stores data in rows and columns, so you can read it back later; files on your laptop don't work once this is deployed because servers forget everything between requests]. For a public waitlist that keeps strangers' emails on a small budget, here's what fits:

**1. Supabase (recommended)**
Plain explanation: hosted Postgres database with a dashboard and built-in access rules.
Fits you because: T2 projects need **access rules** [server-enforced "who can read/write what" — without them, anyone on the internet with your public key could read your whole email list] from day one, and Supabase builds them in. One service covers signups now and logins later if you add them.
Cost at your size: free tier easily covers a waitlist; paid tier starts around the low tens per month if you grow.
Watch out for: the access rules (**RLS** [Row Level Security — Postgres feature that filters rows per user]) must be configured correctly. I'll set them up and tell you what to double-check in their dashboard.
Lock-in: low — it's standard Postgres underneath, you can export and move it.

**2. Neon**
Plain explanation: hosted Postgres, no dashboard-level auth or access-rule UI — just the database.
Fits you because: simpler if you only need a database and nothing else, ever.
Cost at your size: generous free tier.
Watch out for: no built-in auth or row-level rules UI. If you ever add logins or a public-read use case, you'll wire that up yourself.

**3. Firebase**: not a fit for you. It charges per read and write, so a bug in a loop can run up the bill, and its data format is harder to move away from later. For a simple email list, that trade-off doesn't earn its keep.

`[tool] ToolSearch {"query": "select:AskUserQuestion", "max_results": 1}`

`[tool] AskUserQuestion {"questions": [{"question": "Which database should we use to store waitlist signups?", "header": "Database", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "Hosted Postgres with built-in access rules. Covers your T2 needs and can grow with you."}, {"label": "Neon", "description": "Hosted Postgres, database only. Simpler if you'll never add logins or public rea`

It looks like the question got dismissed. No worries — just tell me which one you want (Supabase, Neon, Firebase, or something else), and I'll wire it up. If you're unsure, I'd go with **Supabase** for a public waitlist on a small budget.

## Turn 2: `I'll go with Firebase instead`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/tripwires.md"}`

`[tool] Bash {"command": "ls -a <workdir>/", "description": "List all files in project root"}`

Going with Firebase. One trade-off worth saying once: Firebase charges per read and write, and its data format is specific to Firebase — if you ever want to leave, exporting is more work than with a plain Postgres database. Fine for a waitlist, just worth knowing.

Here's the plan, with the warnings that apply at your tier (T2) before I touch anything.

⚠️ **Secrets:** Firebase needs a **service account key** [a JSON file with credentials that let your server write to Firebase; must stay on the server, never in the browser or in git].
What could go wrong: if that key ends up in your code bundle or in git, anyone can write to or empty your database.
How you'd notice: you wouldn't, until bots find it (usually within hours of a public commit).
What I'm doing: putting the credentials in `.env.local`, adding `.env*` to `.gitignore`, and only reading them in server code. The client will never talk to Firebase directly — it hits your `/api/signup`, which does the write.

⚠️ **Database access rules:** Firebase has **security rules** [server-enforced rules that decide who can read/write each collection; the default is sometimes permissive].
What could go wrong: with open rules, anyone who finds the project ID could read your whole email list from a browser.
How you'd notice: you wouldn't, until the list appears somewhere it shouldn't.
What I'm doing: since the client doesn't use the Firebase SDK at all, I'll give you deny-by-default rules to paste into the Firebase console. All writes go through your server with the service account key, which ignores rules — safe because only your API route can call it.

Now the code.

`[tool] Read {"file_path": "<workdir>/app/api/signup/route.ts"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/package.json", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\" }", "new_string": "  \"dependencies\": {\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\": \"19.1.0\",\n    \"firebase-a`

`[tool] Write {"file_path": "<workdir>/lib/firebase.ts", "content": "import { cert, getApps, initializeApp } from \"firebase-admin/app\";\nimport { getFirestore } from \"firebase-admin/firestore\";\n\nfunction getApp() {\n  if (getApps().length) return getApps()[0];\n\n  const projectId = process.env.FIREBASE_PROJECT_ID;\n  con`

`[tool] Write {"file_path": "<workdir>/app/api/signup/route.ts", "content": "import { FieldValue } from \"firebase-admin/firestore\";\nimport { db } from \"@/lib/firebase\";\n\nexport async function POST(req: Request) {\n  const { email } = await req.json();\n\n  if (typeof email !== \"string\" || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]`

`[tool] Write {"file_path": "<workdir>/.env.local.example", "content": "# Firebase service account credentials. Paste values from the JSON file you\n# downloaded in Firebase console -> Project settings -> Service accounts ->\n# Generate new private key. KEEP THIS FILE OUT OF GIT.\nFIREBASE_PROJECT_ID=\nFIREBASE_CLIENT_EMAIL=\n#`

`[tool] Write {"file_path": "<workdir>/.gitignore", "content": "# deps\nnode_modules\n\n# next.js\n.next\nout\n\n# env (secrets)\n.env\n.env.local\n.env.*.local\n\n# firebase service account JSON (if you ever save it to disk)\nfirebase-service-account*.json\nserviceAccount*.json\n"}`

`[tool] Write {"file_path": "<workdir>/firestore.rules", "content": "// Deny all client access. Writes happen on the server with the Firebase Admin\n// SDK, which bypasses these rules. If you later add a client that reads or\n// writes Firestore directly, add narrower rules here instead of opening these.\nrules_version = '2';\n`

Now I need to make the `@/lib/firebase` import work in Next.js — that requires a `tsconfig.json` path alias, which doesn't exist yet. Let me check.

`[tool] Bash {"command": "ls <workdir>/tsconfig.json 2>&1", "description": "Check for tsconfig"}`

No tsconfig, so the `@/` alias won't resolve. I'll switch to a relative import.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/app/api/signup/route.ts", "old_string": "import { db } from \"@/lib/firebase\";", "new_string": "import { db } from \"../../../lib/firebase\";"}`

Now update the vibe profile and known terms to record the choice.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/.vibe/profile.md", "old_string": "## Notes", "new_string": "## Notes\n- 2026-10-12: Database = Firebase (Firestore). User picked over Supabase recommendation. Writes go through server API with Admin SDK; client has no Firebase SDK. Firestore rules locked deny-all."}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/.vibe/known-terms.md", "old_string": "<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->", "new_string": "<!-- Terms /vibe has already explained in this project. One per line: term | short expl`

Done. Here's what changed and what you need to do.

**What changed:**
- `/api/signup` now validates the email and writes it to a `signups` collection in Firestore, keyed by the email so duplicates don't pile up.
- `lib/firebase.ts` sets up the Firebase Admin SDK on the server using env vars.
- `firestore.rules` denies all client access (server writes bypass this).
- `.gitignore` keeps `.env*` and any stray service-account JSON out of git.
- `.env.local.example` shows which three values to paste.
- `firebase-admin` added to `package.json`.

**Three things only you can do** (I can't log into your Firebase account):
1. In the [Firebase console](https://console.firebase.google.com/), create a project, then **Build → Firestore Database → Create database** (pick a region close to your users).
2. **Project settings → Service accounts → Generate new private key.** This downloads a JSON file. Copy `project_id`, `client_email`, `private_key` into a new `.env.local` file (use `.env.local.example` as the template). Then delete the downloaded JSON — don't commit it.
3. **Firestore → Rules tab**, paste the contents of `firestore.rules`, click Publish. Also set a **budget alert** in Google Cloud Billing so a bug can't quietly run up a bill overnight.

Then `npm install` and `npm run dev`, submit the form, and the email should appear in Firestore. Tell me if anything looks off.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.env.local.example <workdir>/.env.local.example
--- evals/fixtures/public-waitlist/.env.local.example	1970-01-01 05:30:00
+++ <workdir>/.env.local.example	2026-10-12 22:32:13
@@ -0,0 +1,8 @@
+# Firebase service account credentials. Paste values from the JSON file you
+# downloaded in Firebase console -> Project settings -> Service accounts ->
+# Generate new private key. KEEP THIS FILE OUT OF GIT.
+FIREBASE_PROJECT_ID=
+FIREBASE_CLIENT_EMAIL=
+# Keep the quotes. Paste the private_key value exactly as it appears in the JSON,
+# including the \n escape sequences.
+FIREBASE_PRIVATE_KEY=""
diff -ruN -x .claude evals/fixtures/public-waitlist/.gitignore <workdir>/.gitignore
--- evals/fixtures/public-waitlist/.gitignore	1970-01-01 05:30:00
+++ <workdir>/.gitignore	2026-10-12 22:32:16
@@ -0,0 +1,15 @@
+# deps
+node_modules
+
+# next.js
+.next
+out
+
+# env (secrets)
+.env
+.env.local
+.env.*.local
+
+# firebase service account JSON (if you ever save it to disk)
+firebase-service-account*.json
+serviceAccount*.json
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>/.vibe/known-terms.md
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/known-terms.md	2026-10-12 22:32:38
@@ -1,3 +1,7 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+database | a place that stores data in rows and columns, so you can read it back later
+access rules | server-enforced "who can read/write what" on a database
+service account key | a JSON file with credentials that let your server write to Firebase; must stay on the server
+security rules | Firebase's server-enforced rules that decide who can read/write each collection
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:32:32
@@ -15,3 +15,4 @@
 **Why:** Public page that stores strangers' email addresses.
 
 ## Notes
+- 2026-10-12: Database = Firebase (Firestore). User picked over Supabase recommendation. Writes go through server API with Admin SDK; client has no Firebase SDK. Firestore rules locked deny-all.
diff -ruN -x .claude evals/fixtures/public-waitlist/app/api/signup/route.ts <workdir>/app/api/signup/route.ts
--- evals/fixtures/public-waitlist/app/api/signup/route.ts	2026-10-12 22:16:59
+++ <workdir>/app/api/signup/route.ts	2026-10-12 22:32:28
@@ -1,6 +1,22 @@
+import { FieldValue } from "firebase-admin/firestore";
+import { db } from "../../../lib/firebase";
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
+  const normalized = email.trim().toLowerCase();
+
+  await db()
+    .collection("signups")
+    .doc(normalized)
+    .set(
+      { email: normalized, createdAt: FieldValue.serverTimestamp() },
+      { merge: true },
+    );
+
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/firestore.rules <workdir>/firestore.rules
--- evals/fixtures/public-waitlist/firestore.rules	1970-01-01 05:30:00
+++ <workdir>/firestore.rules	2026-10-12 22:32:21
@@ -0,0 +1,11 @@
+// Deny all client access. Writes happen on the server with the Firebase Admin
+// SDK, which bypasses these rules. If you later add a client that reads or
+// writes Firestore directly, add narrower rules here instead of opening these.
+rules_version = '2';
+service cloud.firestore {
+  match /databases/{database}/documents {
+    match /{document=**} {
+      allow read, write: if false;
+    }
+  }
+}
diff -ruN -x .claude evals/fixtures/public-waitlist/lib/firebase.ts <workdir>/lib/firebase.ts
--- evals/fixtures/public-waitlist/lib/firebase.ts	1970-01-01 05:30:00
+++ <workdir>/lib/firebase.ts	2026-10-12 22:32:03
@@ -0,0 +1,22 @@
+import { cert, getApps, initializeApp } from "firebase-admin/app";
+import { getFirestore } from "firebase-admin/firestore";
+
+function getApp() {
+  if (getApps().length) return getApps()[0];
+
+  const projectId = process.env.FIREBASE_PROJECT_ID;
+  const clientEmail = process.env.FIREBASE_CLIENT_EMAIL;
+  const privateKey = process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, "\n");
+
+  if (!projectId || !clientEmail || !privateKey) {
+    throw new Error(
+      "Missing Firebase credentials. Set FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, FIREBASE_PRIVATE_KEY in .env.local.",
+    );
+  }
+
+  return initializeApp({ credential: cert({ projectId, clientEmail, privateKey }) });
+}
+
+export function db() {
+  return getFirestore(getApp());
+}
diff -ruN -x .claude evals/fixtures/public-waitlist/package.json <workdir>/package.json
--- evals/fixtures/public-waitlist/package.json	2026-10-12 22:16:59
+++ <workdir>/package.json	2026-10-12 22:31:57
@@ -2,5 +2,10 @@
   "name": "public-waitlist",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0" }
+  "dependencies": {
+    "next": "15.3.0",
+    "react": "19.1.0",
+    "react-dom": "19.1.0",
+    "firebase-admin": "^12.7.0"
+  }
 }

```