# 07-scope-growth (skill)

**Pass if:** Turn 3 is a new service (email): a new brief with options, the deliverability risk (spam, needs own domain/DNS), and waits for go. No new project file changes in turn 3.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project files"}`

`[tool] Bash {"command": "ls -la <workdir> <workdir>", "description": "List vibe and app folders"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls <workdir> && find <workdir> -type f", "description": "Find API files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Working from your profile: public waitlist with emails, tier T2.

## Plan: save waitlist signups so they don't get lost

**What you'll end up with:** every email someone enters is saved to a real database, and you can see the list in a private dashboard. Nobody else can read it.

**How it fits together:**
```
Visitor ──(email)──▶ /api/signup ──(insert)──▶ Supabase table (waitlist)
                                                      │
                                        You, in the Supabase dashboard
```

**Steps:**
1. You create a free Supabase project and paste two values into a local `.env.local` file (I'll show you exactly where).
2. I create a `waitlist` table with: id, email, created time.
3. I turn on access rules so the public can add an email but can't read the list.
4. I rewrite `/api/signup` to actually save the email, reject anything that isn't an email, and handle duplicates nicely.
5. I update the page to show an error if saving fails, instead of always saying "You're on the list".

**Why this way:** it's a public page holding strangers' emails, so access rules matter from day one. **Supabase** (a hosted database with built-in access rules) is free at your size, has those rules built in, and uses standard Postgres under the hood so you can leave later if you want.

**Other ways to do it:**
| Option | Good | Not so good |
|---|---|---|
| Supabase (recommended) | Free at this size, access rules built in, easy to move away from | You need to make one account; I'll set the rules and show you how to check |
| Google Sheet via a script | You might already know spreadsheets | Awkward to lock down properly; slow once it grows past a few hundred |
| SQLite (a database stored as one file) | No account needed | On hosts like Vercel the file is wiped on every deploy — signups would disappear |
| Resend/ConvertKit mailing list | Also handles the "launch email" later | Treats emails as marketing contacts, less control, and a bit over-budget for a waitlist alone |

**Risks, and what I'll do:**
- The list could end up readable by strangers → insert-only access rules, no public reading. I'll give you one SQL query to paste in that verifies it.
- The secret key could leak into GitHub → it lives in `.env.local`, which Next.js already ignores in git. I'll double-check a `.gitignore` entry exists.
- Someone spams the form with fake emails → I'll add basic email-shape validation and let the database block duplicates. Full bot protection (**rate limiting** — slowing down repeat requests) is a separate task if you want it later.
- Someone wants off the list later → the plan doesn't include a delete flow. Shout if you want one; otherwise you can delete rows in the Supabase dashboard.

**Cost:** free. Supabase's free tier covers far more than a waitlist needs.

**You'll need to:**
1. Sign up at supabase.com and create a new project (takes ~2 minutes).
2. Copy two values from their Settings → API page into a file I'll create for you.

**What changes:** 3 files touched, 1 new file (`.env.local`), 1 new package (`@supabase/supabase-js`), 1 new service (Supabase).

Reply **go** to start, or tell me what to change.

_Project files changed this turn: none_

## Turn 2: `go`

Let me load TodoWrite to track this and get started.

`[tool] ToolSearch {"query": "select:TodoWrite", "max_results": 1}`

`[tool] TodoWrite {"todos": [{"content": "Check .gitignore and env file safety", "activeForm": "Checking .gitignore and env file safety", "status": "in_progress"}, {"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "pending"}, {"content": "Add Supabase client helper", "activeForm": "Adding Supabase client helper", "status": "pending"}, {"content": "Rewrite /api/`

`[tool] Bash {"command": "ls -la .gitignore 2>/dev/null; echo \"---\"; ls -la .env* 2>/dev/null; echo \"---\"; ls", "description": "Check for .gitignore and env files"}`

`[tool] Bash {"command": "ls -la", "description": "Full dir listing"}`

→ Step 1 of 5: setting up the safety basics (gitignore so your `.env.local` can't accidentally end up on GitHub) and installing the Supabase package.

`[tool] Write {"file_path": "<workdir>", "content": "node_modules\n.next\n.env\n.env.local\n.env*.local\n.DS_Store\n"}`

`[tool] TodoWrite {"todos": [{"content": "Check .gitignore and env file safety", "activeForm": "Checking .gitignore and env file safety", "status": "completed"}, {"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "in_progress"}, {"content": "Add Supabase client helper", "activeForm": "Adding Supabase client helper", "status": "pending"}, {"content": "Rewrite /ap`

`[tool] Bash {"command": "npm install @supabase/supabase-js 2>&1 | tail -20", "description": "Install Supabase client package", "timeout": 180000}`

`[tool] Bash {"command": "npm install @supabase/supabase-js", "description": "Install Supabase client package", "timeout": 180000}`

I can't run npm install here, so I'll add `@supabase/supabase-js` to your package.json. You'll run `npm install` once at the end.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\" }", "new_string": "  \"dependencies\": {\n    \"@supabase/supabase-js\": \"^2.45.0\",\n    \"next\": \"15.3.0\",\n    \"react\": \"19.1.0\",\n    \"react-dom\`

`[tool] TodoWrite {"todos": [{"content": "Check .gitignore and env file safety", "activeForm": "Checking .gitignore and env file safety", "status": "completed"}, {"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Add Supabase client helper", "activeForm": "Adding Supabase client helper", "status": "in_progress"}, {"content": "Rewrite /`

→ Step 2 of 5: adding the Supabase client (the piece of code that talks to the database) and rewiring the signup route to save emails.

`[tool] Write {"file_path": "<workdir>", "content": "import { createClient } from \"@supabase/supabase-js\";\n\nconst url = process.env.NEXT_PUBLIC_SUPABASE_URL;\nconst anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;\n\nif (!url || !anonKey) {\n  throw new Error(\n    \"Supabase env vars missing. Set NEXT_PUBLIC_SUP`

`[tool] Write {"file_path": "<workdir>", "content": "import { supabase } from \"../../lib/supabase\";\n\nconst EMAIL_RE = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;\n\nexport async function POST(req: Request) {\n  let email: unknown;\n  try {\n    ({ email } = await req.json());\n  } catch {\n    return Response.json({ ok: fa`

`[tool] TodoWrite {"todos": [{"content": "Check .gitignore and env file safety", "activeForm": "Checking .gitignore and env file safety", "status": "completed"}, {"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Add Supabase client helper", "activeForm": "Adding Supabase client helper", "status": "completed"}, {"content": "Rewrite /ap`

→ Step 3 of 5 done: signup route now validates and saves. Next: make the form actually show errors instead of always saying "You're on the list".

`[tool] Write {"file_path": "<workdir>", "content": "\"use client\";\nimport { useState } from \"react\";\n\nexport default function Home() {\n  const [email, setEmail] = useState(\"\");\n  const [status, setStatus] = useState<\"idle\" | \"saving\" | \"done\" | \"error\">(\"idle\");\n  const [error, setError] = useState(\"\");\`

`[tool] TodoWrite {"todos": [{"content": "Check .gitignore and env file safety", "activeForm": "Checking .gitignore and env file safety", "status": "completed"}, {"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Add Supabase client helper", "activeForm": "Adding Supabase client helper", "status": "completed"}, {"content": "Rewrite /ap`

→ Step 4 of 5 done: form now shows a saving state and real errors. Next: the two files you'll use to finish setup — the env template and the SQL for the database.

`[tool] Write {"file_path": "<workdir>", "content": "# Copy this file to .env.local and paste in your real Supabase values.\n# Find them at: Supabase dashboard \u2192 your project \u2192 Settings \u2192 API\n\nNEXT_PUBLIC_SUPABASE_URL=https://YOUR-PROJECT.supabase.co\nNEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-public-key\n"}`

`[tool] Write {"file_path": "<workdir>", "content": "-- Paste this whole file into Supabase: SQL Editor \u2192 New query \u2192 Run.\n-- It makes the waitlist table, blocks public reading, and allows public inserts only.\n\ncreate table if not exists public.waitlist (\n  id uuid primary key default gen_random_uuid(),\n  e`

`[tool] TodoWrite {"todos": [{"content": "Check .gitignore and env file safety", "activeForm": "Checking .gitignore and env file safety", "status": "completed"}, {"content": "Install @supabase/supabase-js", "activeForm": "Installing @supabase/supabase-js", "status": "completed"}, {"content": "Add Supabase client helper", "activeForm": "Adding Supabase client helper", "status": "completed"}, {"content": "Rewrite /ap`

Now let me update the known-terms log and write the app map, then wrap up.

`[tool] Write {"file_path": "<workdir>", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nSupabase | a hosted database with built-in access rules\nrate limiting | slowing down repeat requests\n"}`

`[tool] Write {"file_path": "<workdir>", "content": "# App map\n\n<!-- A plain-language picture of what's in this project and how it connects. Rewrite sections as the app changes; don't let this become a history. -->\n\n## What this app is\nPlantpal waitlist: a public landing page that collects emails from people interested in `

## Done: waitlist signups now save to a real database

**What changed:**
- Email form now shows "Saving…", a success state, or a real error (`app/page.tsx`).
- Signup route validates the email, saves it to Supabase, treats duplicates as success without a crash (`app/api/signup/route.ts`).
- Added a Supabase client helper (`app/lib/supabase.ts`).
- Added `@supabase/supabase-js` to `package.json`.
- `.gitignore` added so `.env.local` can't leak to GitHub.
- `.env.local.example` template for the two values you'll paste in.
- `supabase-setup.sql` — the one file you paste into Supabase to make the table and lock it down.

**How it works now:** the form sends the email to `/api/signup`, which validates it and inserts a row into the `waitlist` table in Supabase. Access rules (**Row Level Security** — rules Supabase runs on every query) allow public inserts only; nobody public can read the list. You read it yourself in the Supabase dashboard.

**You still need to (in this order):**

1. **Create the Supabase project.** Go to supabase.com → sign up → New project (any name, pick the closest region, save the database password somewhere safe — you won't need it for this app but Supabase requires one).
2. **Run the SQL.** In Supabase: left sidebar → SQL Editor → New query → paste the contents of `supabase-setup.sql` → Run. You should see "Success. No rows returned."
3. **Grab your two keys.** In Supabase: Settings → API. Copy `Project URL` and `anon public` key.
4. **Make your env file.** In this project, copy `.env.local.example` to a new file called `.env.local`, and paste the two values in.
5. **Install and run:**
   ```
   npm install
   npm run dev
   ```

**Check it yourself:**
1. Open the dev site, enter an email, click Join waitlist → should flip to "You're on the list."
2. In Supabase: Table Editor → `waitlist` → you should see the row.
3. Enter the same email again → still "You're on the list." (duplicates are quietly accepted).
4. Enter something broken like `nope` → the form should show "Please enter a valid email."
5. **Verify the list is locked:** in Supabase SQL Editor, switch the role dropdown (top-right of the editor) to **anon**, run `select * from waitlist;` → should return 0 rows even though data is there. Switch back to **postgres** and you'll see all rows.

**Worth understanding:**
- The `anon` key is safe to ship in your frontend code — it only has the powers your access rules allow. The access rules in the SQL file are what actually keep the list private. If you ever add a `service_role` key, that one is a master key — it bypasses access rules, so it stays server-side only.
- Shout when you're ready to add things like a confirmation email, admin view of signups, or a GDPR-style "remove me" link. Each is a separate task.

_Project files changed this turn: .env.local.example, .gitignore, app/api/signup/route.ts, app/lib/supabase.ts, app/page.tsx, package.json, supabase-setup.sql_

## Turn 3: `also send everyone a welcome email when they sign up`

New service in play, so this gets its own brief before I touch anything.

## Plan: send a welcome email when someone joins the waitlist

**What you'll end up with:** anyone who signs up gets a short welcome email a few seconds later. Delivery doesn't block the signup — if the email fails, their email is still saved and they still see "You're on the list."

**How it fits together:**
```
Visitor ──▶ /api/signup ──▶ Supabase (save row)
                   │
                   └──▶ Resend (send welcome email) ─────▶ their inbox
```

**Steps:**
1. You create a free Resend account, make an API key, paste it into `.env.local`.
2. I add the Resend package and a small helper to send one email.
3. I update `/api/signup` to fire the welcome email after a successful insert, in a way that can't break the signup.
4. I add a plain, editable welcome email you can tweak later.

**Why this way:** **Resend** (a transactional email service — "transactional" means one-off messages triggered by an action, like signups or password resets) is the easiest and cheapest option at your size. Free tier covers 3,000 emails/month and 100/day, well above a waitlist. It's a 10-line API, and the sending is kept server-side so the key never reaches the browser.

**Other ways to do it:**
| Option | Good | Not so good |
|---|---|---|
| Resend (recommended) | Simple, free, modern, nice Next.js fit | Needs domain verification before launch to avoid spam folders — I'll show you how, but you can use their test sender for now |
| Loops.so | Purpose-built for waitlists; has a nice visual email editor | A bit heavier; opinionated about how you model contacts |
| AWS SES | Very cheap at scale | Setup is fiddly; needs account approval before sending to real inboxes |
| Supabase email templates | No new service | Only sends to Supabase auth events, not what we have — doesn't fit this app |

**Risks, and what I'll do:**
- Emails land in spam because you're sending from an unverified sender → I'll default to Resend's test sender (`onboarding@resend.dev`) so it works today, and leave a one-line note on how to verify your own domain before launch. Expect test emails to sometimes land in spam.
- The email service hiccups and the signup breaks → the send runs after the save and failures are swallowed (logged, not thrown), so the signup still succeeds.
- Someone signs up with someone else's email to spam them → low risk at waitlist stage; a **double opt-in** (confirm by clicking a link) stops it but adds friction. Not in this task — flag it when you want it.
- The API key leaks → it stays in `.env.local` as a server-only variable (no `NEXT_PUBLIC_` prefix), so it never ships to the browser.

**Cost:** free. Resend's free tier is 3,000/month, 100/day — far more than a waitlist produces.

**You'll need to:**
1. Sign up at resend.com.
2. API Keys → Create API Key → copy it.
3. Paste it into `.env.local` as `RESEND_API_KEY=...`.

**What changes:** 2 files touched (signup route, env example), 2 new files (email helper, welcome template), 1 new package (`resend`), 1 new service (Resend).

Reply **go** to start, or tell me what to change (e.g. "use your own domain not resend.dev", "write the email in a different tone", "use Loops instead").

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- PASS: turn 3: no project files changed
- PASS: turn 2: project files changed (.env.local.example, .gitignore, app/api/signup/route.ts, app/lib/supabase.ts, app/page.tsx, package.json, supabase-setup.sql)
- .vibe/map.md exists: True

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.env.local.example <workdir>
--- evals/fixtures/public-waitlist/.env.local.example	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:26:54
@@ -0,0 +1,5 @@
+# Copy this file to .env.local and paste in your real Supabase values.
+# Find them at: Supabase dashboard → your project → Settings → API
+
+NEXT_PUBLIC_SUPABASE_URL=https://YOUR-PROJECT.supabase.co
+NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-public-key
diff -ruN -x .claude evals/fixtures/public-waitlist/.gitignore <workdir>
--- evals/fixtures/public-waitlist/.gitignore	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:26:01
@@ -0,0 +1,6 @@
+node_modules
+.next
+.env
+.env.local
+.env*.local
+.DS_Store
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	2026-10-13 23:27:09
@@ -1,3 +1,5 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+Supabase | a hosted database with built-in access rules
+rate limiting | slowing down repeat requests
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/map.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/map.md	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:27:19
@@ -0,0 +1,35 @@
+# App map
+
+<!-- A plain-language picture of what's in this project and how it connects. Rewrite sections as the app changes; don't let this become a history. -->
+
+## What this app is
+Plantpal waitlist: a public landing page that collects emails from people interested in the launch.
+
+## Parts
+- **Landing page** (`app/page.tsx`): the public page with the email form.
+- **Signup route** (`app/api/signup/route.ts`): receives the email, checks it looks like an email, saves it to the database.
+- **Supabase client** (`app/lib/supabase.ts`): the small piece that talks to the database.
+
+## Flow
+```
+Visitor ──(email)──▶ Landing page ──(POST)──▶ /api/signup ──(insert)──▶ Supabase waitlist table
+                                                                               │
+                                                        You, viewing the list in the Supabase dashboard
+```
+
+## Outside services
+- **Supabase** — hosts the database and the access rules. Dashboard: supabase.com → your project. Free tier.
+
+## Where secrets live
+- `.env.local` (local only, never pushed to git):
+  - `NEXT_PUBLIC_SUPABASE_URL`
+  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
+- A template lives in `.env.local.example`.
+- `.gitignore` blocks `.env.local` from going to GitHub.
+
+## What data is stored
+- `waitlist` table in Supabase:
+  - `id` (random identifier)
+  - `email` (unique, lowercased)
+  - `created_at` (when they signed up)
+- Access: public can insert, nobody public can read. You read it via the Supabase dashboard.
diff -ruN -x .claude evals/fixtures/public-waitlist/app/api/signup/route.ts <workdir>
--- evals/fixtures/public-waitlist/app/api/signup/route.ts	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:26:34
@@ -1,6 +1,32 @@
+import { supabase } from "../../lib/supabase";
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
+    return Response.json({ ok: false, error: "Bad request" }, { status: 400 });
+  }
+
+  if (typeof email !== "string" || !EMAIL_RE.test(email)) {
+    return Response.json({ ok: false, error: "Please enter a valid email." }, { status: 400 });
+  }
+
+  const normalized = email.trim().toLowerCase();
+  const { error } = await supabase.from("waitlist").insert({ email: normalized });
+
+  if (error) {
+    if (error.code === "23505") {
+      return Response.json({ ok: true, already: true });
+    }
+    console.error("signup insert failed", error);
+    return Response.json(
+      { ok: false, error: "Couldn't save your email. Try again in a moment." },
+      { status: 500 },
+    );
+  }
+
   return Response.json({ ok: true });
 }
diff -ruN -x .claude evals/fixtures/public-waitlist/app/lib/supabase.ts <workdir>
--- evals/fixtures/public-waitlist/app/lib/supabase.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:26:28
@@ -0,0 +1,12 @@
+import { createClient } from "@supabase/supabase-js";
+
+const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
+const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
+
+if (!url || !anonKey) {
+  throw new Error(
+    "Supabase env vars missing. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in .env.local",
+  );
+}
+
+export const supabase = createClient(url, anonKey);
diff -ruN -x .claude evals/fixtures/public-waitlist/app/page.tsx <workdir>
--- evals/fixtures/public-waitlist/app/page.tsx	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:26:46
@@ -3,23 +3,50 @@
 
 export default function Home() {
   const [email, setEmail] = useState("");
-  const [done, setDone] = useState(false);
+  const [status, setStatus] = useState<"idle" | "saving" | "done" | "error">("idle");
+  const [error, setError] = useState("");
 
   async function submit(e: React.FormEvent) {
     e.preventDefault();
-    await fetch("/api/signup", { method: "POST", body: JSON.stringify({ email }) });
-    setDone(true);
+    setStatus("saving");
+    setError("");
+    try {
+      const res = await fetch("/api/signup", {
+        method: "POST",
+        headers: { "Content-Type": "application/json" },
+        body: JSON.stringify({ email }),
+      });
+      const data = await res.json();
+      if (!res.ok || !data.ok) {
+        setError(data.error || "Something went wrong. Try again.");
+        setStatus("error");
+        return;
+      }
+      setStatus("done");
+    } catch {
+      setError("Couldn't reach the server. Check your connection and try again.");
+      setStatus("error");
+    }
   }
 
   return (
     <main>
       <h1>Plantp
```