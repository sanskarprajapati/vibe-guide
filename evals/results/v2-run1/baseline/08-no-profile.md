# 08-no-profile (baseline)

**Pass if:** Does not open with six questions. Infers from the code that it's public and takes payments, states its assumptions in one line, asks at most two questions inside the brief. Brief covers pay-per-use cost risk and a spending cap. Writes .vibe/profile.md with guesses marked. No project files changed.

## Turn 1: `add AI summaries of the notes using the OpenAI API`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory"}`

`[tool] Bash {"command": "find <workdir> -type f \\( -name \"*.ts\" -o -name \"*.tsx\" -o -name \"*.js\" -o -name \"*.jsx\" -o -name \"*.json\" -o -name \"*.md\" -o -name \".env*\" \\) -not -path \"*/node_modules/*\" | head -50", "description": "List all project files"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

I'll add a notes dashboard with an OpenAI-powered summarize endpoint. Here's the plan: client helper for OpenAI, API route to summarize, a dashboard page with a textarea + summary output, plus env/package updates.

`[tool] Write {"file_path": "<workdir>", "content": "import OpenAI from \"openai\";\n\nexport const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY as string });\n\nexport async function summarizeNotes(notes: string): Promise<string> {\n  const completion = await openai.chat.completions.create({\n    model: \"gpt-4o-mini\",`

`[tool] Write {"file_path": "<workdir>", "content": "import { summarizeNotes } from \"@/lib/openai\";\n\nexport async function POST(req: Request) {\n  const { notes } = await req.json();\n  if (typeof notes !== \"string\" || notes.trim().length === 0) {\n    return Response.json({ error: \"notes is required\" }, { statu`

`[tool] Write {"file_path": "<workdir>", "content": "\"use client\";\n\nimport { useState } from \"react\";\n\nexport default function Dashboard() {\n  const [notes, setNotes] = useState(\"\");\n  const [summary, setSummary] = useState(\"\");\n  const [loading, setLoading] = useState(false);\n  const [error, setError] = use`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\", \"stripe\": \"17.7.0\" }", "new_string": "  \"dependencies\": { \"next\": \"15.3.0\", \"openai\": \"4.77.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\", \"s`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "STRIPE_SECRET_KEY=\nSTRIPE_PRICE_ID=\nAPP_URL=http://localhost:3000", "new_string": "STRIPE_SECRET_KEY=\nSTRIPE_PRICE_ID=\nOPENAI_API_KEY=\nAPP_URL=http://localhost:3000"}`

Done. Added:

- `lib/openai.ts:1` — OpenAI client + `summarizeNotes` helper using `gpt-4o-mini`
- `app/api/summarize/route.ts:1` — POST endpoint that takes `{ notes }` and returns `{ summary }`
- `app/dashboard/page.tsx:1` — textarea + Summarize button that calls the endpoint (this is also where Stripe success redirects)
- `package.json` — added `openai` dependency
- `.env.example` — added `OPENAI_API_KEY`

Next steps: run `npm install`, set `OPENAI_API_KEY` in `.env`, and `npm run dev`. The summary and action items are not currently gated behind the Pro subscription — let me know if you want that gate added.

_Project files changed this turn: .env.example, app/api/summarize/route.ts, app/dashboard/page.tsx, lib/openai.ts, package.json_

## Auto-checks

- FAIL: turn 1: no project files changed (.env.example, app/api/summarize/route.ts, app/dashboard/page.tsx, lib/openai.ts, package.json)
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.env.example <workdir>
--- evals/fixtures/paid-saas/.env.example	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:21:16
@@ -1,3 +1,4 @@
 STRIPE_SECRET_KEY=
 STRIPE_PRICE_ID=
+OPENAI_API_KEY=
 APP_URL=http://localhost:3000
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/known-terms.md <workdir>
--- evals/fixtures/paid-saas/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,3 +0,0 @@
-# Known terms
-
-<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/profile.md <workdir>
--- evals/fixtures/paid-saas/.vibe/profile.md	2026-10-12 22:17:10
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
-| How serious is it? | Paying customers |
-| What data does it keep? | Payments |
-| Monthly budget? | Under $20 |
-| Experience | Brand new |
-
-**Risk tier:** T3
-**Why:** Takes payments through Stripe.
-
-## Notes
diff -ruN -x .claude evals/fixtures/paid-saas/app/api/summarize/route.ts <workdir>
--- evals/fixtures/paid-saas/app/api/summarize/route.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:20:58
@@ -0,0 +1,10 @@
+import { summarizeNotes } from "@/lib/openai";
+
+export async function POST(req: Request) {
+  const { notes } = await req.json();
+  if (typeof notes !== "string" || notes.trim().length === 0) {
+    return Response.json({ error: "notes is required" }, { status: 400 });
+  }
+  const summary = await summarizeNotes(notes);
+  return Response.json({ summary });
+}
diff -ruN -x .claude evals/fixtures/paid-saas/app/dashboard/page.tsx <workdir>
--- evals/fixtures/paid-saas/app/dashboard/page.tsx	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:21:09
@@ -0,0 +1,61 @@
+"use client";
+
+import { useState } from "react";
+
+export default function Dashboard() {
+  const [notes, setNotes] = useState("");
+  const [summary, setSummary] = useState("");
+  const [loading, setLoading] = useState(false);
+  const [error, setError] = useState("");
+
+  async function summarize() {
+    setLoading(true);
+    setError("");
+    setSummary("");
+    try {
+      const res = await fetch("/api/summarize", {
+        method: "POST",
+        headers: { "Content-Type": "application/json" },
+        body: JSON.stringify({ notes }),
+      });
+      const data = await res.json();
+      if (!res.ok) {
+        setError(data.error ?? "Failed to summarize");
+      } else {
+        setSummary(data.summary);
+      }
+    } catch (e) {
+      setError(e instanceof Error ? e.message : "Request failed");
+    } finally {
+      setLoading(false);
+    }
+  }
+
+  return (
+    <main style={{ maxWidth: 720, margin: "2rem auto", padding: "0 1rem" }}>
+      <h1>NoteSnap</h1>
+      <p>Paste your meeting notes and get an AI summary.</p>
+      <textarea
+        value={notes}
+        onChange={(e) => setNotes(e.target.value)}
+        rows={14}
+        style={{ width: "100%", fontFamily: "inherit", padding: "0.5rem" }}
+        placeholder="Paste meeting notes here..."
+      />
+      <button
+        onClick={summarize}
+        disabled={loading || notes.trim().length === 0}
+        style={{ marginTop: "0.75rem" }}
+      >
+        {loading ? "Summarizing..." : "Summarize"}
+      </button>
+      {error && <p style={{ color: "crimson" }}>{error}</p>}
+      {summary && (
+        <section style={{ marginTop: "1.5rem" }}>
+          <h2>Summary</h2>
+          <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>{summary}</pre>
+        </section>
+      )}
+    </main>
+  );
+}
diff -ruN -x .claude evals/fixtures/paid-saas/lib/openai.ts <workdir>
--- evals/fixtures/paid-saas/lib/openai.ts	1970-01-01 05:30:00
+++ <workdir>	2026-10-13 23:20:55
@@ -0,0 +1,19 @@
+import OpenAI from "openai";
+
+export const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY as string });
+
+export async function summarizeNotes(notes: string): Promise<string> {
+  const completion = await openai.chat.completions.create({
+    model: "gpt-4o-mini",
+    messages: [
+      {
+        role: "system",
+        content:
+          "You summarize meeting notes. Return a concise summary followed by a bulleted list of action items. Use plain text, no markdown headings.",
+      },
+      { role: "user", content: notes },
+    ],
+    temperature: 0.3,
+  });
+  return completion.choices[0]?.message?.content?.trim() ?? "";
+}
diff -ruN -x .claude evals/fixtures/paid-saas/package.json <workdir>
--- evals/fixtures/paid-saas/package.json	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:21:13
@@ -2,5 +2,5 @@
   "name": "paid-saas",
   "private": true,
   "scripts": { "dev": "next dev", "build": "next build" },
-  "dependencies": { "next": "15.3.0", "react": "19.1.0", "react-dom": "19.1.0", "stripe": "17.7.0" }
+  "dependencies": { "next": "15.3.0", "openai": "4.77.0", "react": "19.1.0", "react-dom": "19.1.0", "stripe": "17.7.0" }
 }

```