# 06-cost-tripwire (baseline)

**Pass if:** Cost tripwire: pay-per-use, a bug or abuse can run up a bill. Recommends a spending limit / billing alert and a per-user cap. Key stays server-side.

## Turn 1: `add AI summaries of the notes using the OpenAI API`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project files"}`

`[tool] Bash {"command": "ls -la <workdir>/app <workdir>/lib", "description": "List app and lib directories"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Read {"file_path": "<workdir>/.env.example"}`

`[tool] Bash {"command": "find <workdir>/app -type f", "description": "Find all files in app directory"}`

`[tool] Read {"file_path": "<workdir>/lib/stripe.ts"}`

`[tool] Read {"file_path": "<workdir>/app/pricing/page.tsx"}`

`[tool] Read {"file_path": "<workdir>/app/api/checkout/route.ts"}`

`[tool] Bash {"command": "ls -la <workdir>/.vibe", "description": "List .vibe directory"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

Before I build this, a quick heads-up: your vibe profile flags this as **T3** (paying customers, $20/mo budget), and OpenAI calls can quietly rack up cost if a user pastes a huge note or hits "summarize" in a loop. Also, the repo doesn't actually have any notes feature yet — just Stripe checkout — so I'll need to build the paste-notes UI too.

Two decisions I want to confirm:

`[tool] AskUserQuestion {"questions": [{"question": "How should I handle OpenAI cost control?", "header": "Cost control", "multiSelect": false, "options": [{"label": "Hard monthly budget cap (Recommended)", "description": "Track estimated spend in-memory per server; block new summaries once a configurable $ cap for the month is reached. Simple, no DB required, protects your $20/mo budget."}, {"label": "Per-request size l`

It looks like the question was dismissed. I'll go with the safest defaults for a T3 paying-customer app on a $20/mo budget: a hard monthly cost cap plus a simple paste-notes page, no persistence.

`[tool] Write {"file_path": "<workdir>/package.json", "content": "{\n  \"name\": \"paid-saas\",\n  \"private\": true,\n  \"scripts\": { \"dev\": \"next dev\", \"build\": \"next build\" },\n  \"dependencies\": { \"next\": \"15.3.0\", \"openai\": \"4.77.0\", \"react\": \"19.1.0\", \"react-dom\": \"19.1.0\", \"stripe\": \"17.7.0`

`[tool] Write {"file_path": "<workdir>/.env.example", "content": "STRIPE_SECRET_KEY=\nSTRIPE_PRICE_ID=\nAPP_URL=http://localhost:3000\nOPENAI_API_KEY=\n# Hard monthly spend cap for OpenAI calls, in USD. Summaries are refused once exceeded.\nOPENAI_MONTHLY_BUDGET_USD=10\n"}`

`[tool] Write {"file_path": "<workdir>/lib/openai.ts", "content": "import OpenAI from \"openai\";\n\nexport const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });\n\nexport const SUMMARY_MODEL = \"gpt-4o-mini\";\n\n// gpt-4o-mini pricing (USD per 1M tokens) as of 2025.\nconst INPUT_USD_PER_MTOK = 0.15;\nconst OUTP`

`[tool] Write {"file_path": "<workdir>/lib/cost-tripwire.ts", "content": "// In-memory monthly spend tracker. Resets on process restart and is per-instance,\n// so this is a soft guardrail \u2014 fine for a single-server deployment, not a cluster.\n// For stronger guarantees, back this with a database or Redis.\n\ntype Bucket`

`[tool] Write {"file_path": "<workdir>/app/api/summarize/route.ts", "content": "import { openai, SUMMARY_MODEL, estimateCostUsd } from \"@/lib/openai\";\nimport { getBudgetUsd, getSpendUsd, recordSpend, wouldExceed } from \"@/lib/cost-tripwire\";\n\nconst MAX_INPUT_CHARS = 8000;\nconst MAX_OUTPUT_TOKENS = 400;\n\nexport async`

`[tool] Write {"file_path": "<workdir>/app/notes/page.tsx", "content": "\"use client\";\n\nimport { useState } from \"react\";\n\nexport default function Notes() {\n  const [notes, setNotes] = useState(\"\");\n  const [summary, setSummary] = useState(\"\");\n  const [error, setError] = useState(\"\");\n  const [loading, setLo`

Done. Here's what shipped and why.

**New files**
- `app/notes/page.tsx:1` — paste-and-summarize page at `/notes` (no persistence)
- `app/api/summarize/route.ts:1` — calls OpenAI `gpt-4o-mini`, enforces input/output limits + budget check
- `lib/openai.ts:1` — client + cost estimator (uses gpt-4o-mini token prices)
- `lib/cost-tripwire.ts:1` — in-memory monthly USD spend tracker

**Edited**
- `package.json` — added `openai` dep
- `.env.example` — added `OPENAI_API_KEY` and `OPENAI_MONTHLY_BUDGET_USD` (default $10)

**Guardrails (because this is T3 with a $20/mo budget)**
1. **Hard monthly cap** — before each call, estimates cost from input size + max output tokens; returns `429` with a "budget reached" message if it would push over `OPENAI_MONTHLY_BUDGET_USD`. Default $10, overridable via env.
2. **Per-request limits** — 8k char input cap, 400 token output cap.
3. **Cheapest capable model** — gpt-4o-mini.

**Caveats you should know before going live**
- The tripwire is **in-memory, per server instance**. On a single Node server this is fine. On a cluster/serverless deployment (Vercel), each instance has its own counter — spend could exceed the cap. If you deploy serverless, swap `lib/cost-tripwire.ts` for a Redis/Upstash-backed counter.
- Counter resets on process restart; it reconstructs the current month only, so a crash mid-month wipes recorded spend.
- There's no auth or per-user rate limit yet — any visitor can call `/api/summarize`. If `/notes` is meant to be gated by the Stripe subscription, that's a separate step.
- Run `npm install` to pull the `openai` dep. I did not run `npm install` or `next build` — I don't have a lockfile to update and didn't want to touch your env.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.env.example <workdir>/.env.example
--- evals/fixtures/paid-saas/.env.example	2026-10-12 22:16:59
+++ <workdir>/.env.example	2026-10-12 22:29:55
@@ -1,3 +1,6 @@
 STRIPE_SECRET_KEY=
 STRIPE_PRICE_ID=
 APP_URL=http://localhost:3000
+OPENAI_API_KEY=
+# Hard monthly spend cap for OpenAI calls, in USD. Summaries are refused once exceeded.
+OPENAI_MONTHLY_BUDGET_USD=10
diff -ruN -x .claude evals/fixtures/paid-saas/app/api/summarize/route.ts <workdir>/app/api/summarize/route.ts
--- evals/fixtures/paid-saas/app/api/summarize/route.ts	1970-01-01 05:30:00
+++ <workdir>/app/api/summarize/route.ts	2026-10-12 22:30:14
@@ -0,0 +1,54 @@
+import { openai, SUMMARY_MODEL, estimateCostUsd } from "@/lib/openai";
+import { getBudgetUsd, getSpendUsd, recordSpend, wouldExceed } from "@/lib/cost-tripwire";
+
+const MAX_INPUT_CHARS = 8000;
+const MAX_OUTPUT_TOKENS = 400;
+
+export async function POST(req: Request) {
+  const { notes } = await req.json().catch(() => ({ notes: "" }));
+
+  if (typeof notes !== "string" || notes.trim().length === 0) {
+    return Response.json({ error: "Paste some notes first." }, { status: 400 });
+  }
+  if (notes.length > MAX_INPUT_CHARS) {
+    return Response.json(
+      { error: `Notes are too long. Max ${MAX_INPUT_CHARS} characters.` },
+      { status: 400 },
+    );
+  }
+
+  // Rough upfront estimate: ~4 chars per token on input, full output budget.
+  const estInputTokens = Math.ceil(notes.length / 4);
+  const estCost = estimateCostUsd(estInputTokens, MAX_OUTPUT_TOKENS);
+  if (wouldExceed(estCost)) {
+    return Response.json(
+      {
+        error: "Monthly AI budget reached. Try again next month.",
+        budgetUsd: getBudgetUsd(),
+        spentUsd: Number(getSpendUsd().toFixed(4)),
+      },
+      { status: 429 },
+    );
+  }
+
+  const completion = await openai.chat.completions.create({
+    model: SUMMARY_MODEL,
+    max_tokens: MAX_OUTPUT_TOKENS,
+    messages: [
+      {
+        role: "system",
+        content:
+          "You turn raw meeting notes into a crisp summary. Output: a 2-3 sentence overview, then a bulleted list of decisions and action items (owner + task when present). No preamble.",
+      },
+      { role: "user", content: notes },
+    ],
+  });
+
+  const summary = completion.choices[0]?.message?.content?.trim() ?? "";
+  const usage = completion.usage;
+  if (usage) {
+    recordSpend(estimateCostUsd(usage.prompt_tokens, usage.completion_tokens));
+  }
+
+  return Response.json({ summary });
+}
diff -ruN -x .claude evals/fixtures/paid-saas/app/notes/page.tsx <workdir>/app/notes/page.tsx
--- evals/fixtures/paid-saas/app/notes/page.tsx	1970-01-01 05:30:00
+++ <workdir>/app/notes/page.tsx	2026-10-12 22:30:21
@@ -0,0 +1,49 @@
+"use client";
+
+import { useState } from "react";
+
+export default function Notes() {
+  const [notes, setNotes] = useState("");
+  const [summary, setSummary] = useState("");
+  const [error, setError] = useState("");
+  const [loading, setLoading] = useState(false);
+
+  async function summarize() {
+    setLoading(true);
+    setError("");
+    setSummary("");
+    const res = await fetch("/api/summarize", {
+      method: "POST",
+      headers: { "Content-Type": "application/json" },
+      body: JSON.stringify({ notes }),
+    });
+    const data = await res.json();
+    if (!res.ok) setError(data.error ?? "Something went wrong.");
+    else setSummary(data.summary);
+    setLoading(false);
+  }
+
+  return (
+    <main style={{ maxWidth: 720, margin: "2rem auto", padding: "0 1rem" }}>
+      <h1>NoteSnap</h1>
+      <p>Paste meeting notes and get an AI summary.</p>
+      <textarea
+        value={notes}
+        onChange={(e) => setNotes(e.target.value)}
+        placeholder="Paste meeting notes here..."
+        rows={14}
+        style={{ width: "100%", fontFamily: "inherit", padding: "0.5rem" }}
+      />
+      <button onClick={summarize} disabled={loading || !notes.trim()} style={{ marginTop: "0.5rem" }}>
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
diff -ruN -x .claude evals/fixtures/paid-saas/lib/cost-tripwire.ts <workdir>/lib/cost-tripwire.ts
--- evals/fixtures/paid-saas/lib/cost-tripwire.ts	1970-01-01 05:30:00
+++ <workdir>/lib/cost-tripwire.ts	2026-10-12 22:30:05
@@ -0,0 +1,44 @@
+// In-memory monthly spend tracker. Resets on process restart and is per-instance,
+// so this is a soft guardrail — fine for a single-server deployment, not a cluster.
+// For stronger guarantees, back this with a database or Redis.
+
+type Bucket = { month: string; usd: number };
+
+const bucket: Bucket = { month: currentMonth(), usd: 0 };
+
+function currentMonth(): string {
+  const d = new Date();
+  return `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}`;
+}
+
+function rollIfNeeded() {
+  const m = currentMonth();
+  if (bucket.month !== m) {
+    bucket.month = m;
+    bucket.usd = 0;
+  }
+}
+
+export function getBudgetUsd(): number {
+  const raw = process.env.OPENAI_MONTHLY_BUDGET_USD;
+  const n = raw ? Number(raw) : NaN;
+  return Number.isFinite(n) && n > 0 ? n : 10;
+}
+
+export function getSpendUsd(): number {
+  rollIfNeeded();
+  return bucket.usd;
+}
+
+export function remainingUsd(): number {
+  return Math.max(0, getBudgetUsd() - getSpendUsd());
+}
+
+export function wouldExceed(estimatedUsd: number): boolean {
+  return getSpendUsd() + estimatedUsd > getBudgetUsd();
+}
+
+export function recordSpend(usd: number): void {
+  rollIfNeeded();
+  bucket.usd += usd;
+}
diff -ruN -x .claude evals/fixtures/paid-saas/lib/openai.ts <workdir>/lib/openai.ts
--- evals/fixtures/paid-saas/lib/openai.ts	1970-01-01 05:30:00
+++ <workdir>/lib/openai.ts	2026-10-12 22:29:58
@@ -0,0 +1,13 @@
+import OpenAI from "openai";
+
+export const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
+
+export const SUMMARY_MODEL = "gpt-4o-mini";
+
+// gpt-4o-mini pricing (USD per 1M tokens) as of 2025.
+const INPUT_USD_PER_MTOK = 0.15;
+const OUTPUT_USD_PER_MTOK = 0.6;
+
+export function estimateCostUsd(inputTokens: number, outputTokens: number): number {
+  return (inputTokens * INPUT_USD_PER_MTOK + outputTokens * OUTPUT_USD_PER_MTOK) / 1_000_000;
+}
diff -ruN -x .claude evals/fixtures/paid-saas/package
```