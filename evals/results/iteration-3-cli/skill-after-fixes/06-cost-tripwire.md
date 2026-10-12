# 06-cost-tripwire (skill)

**Pass if:** Cost tripwire: pay-per-use, a bug or abuse can run up a bill. Recommends a spending limit / billing alert and a per-user cap. Key stays server-side.

## Turn 1: `/vibe add AI summaries of the notes using the OpenAI API`

`[tool] Bash {"command": "ls -la <workdir>/ && echo \"---\" && ls -la <workdir>/.vibe/ 2>/dev/null || echo \"No .vibe directory\"", "description": "Check for vibe profile and project files"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

`[tool] Bash {"command": "cat <workdir>/package.json <workdir>/.env.example && echo \"---APP---\" && ls -R <workdir>/app <workdir>`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/tripwires.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

Using your profile: paid SaaS on Stripe, tier T3.

Before I write code, two things I want to flag — because for a paid app like NoteSnap, "add OpenAI summaries" has some invisible landmines.

**1. Your project doesn't have a notes feature yet.** Right now the code is a pricing page + Stripe checkout, nothing to paste notes into. So "summaries of the notes" has to be built together with a notes page (or at least a textarea + button), unless you have another version somewhere.

**2. Tripwire — pay-per-use AI, no gating yet.**

⚠️ Heads up: OpenAI charges you a small amount **(a few hundredths of a cent to a few cents)** every single time your app asks it to summarise something. That's called pay-per-use.
What could go wrong: a bug that loops, a page that re-summarises on every refresh, or one noisy visitor can turn into a surprise bill. Your profile says budget is under $20/month.
How you'd notice: you wouldn't, until the OpenAI dashboard shows a jump — often days later.
What I'm doing: putting the OpenAI **API key** (a secret password that lets your code talk to OpenAI) only on the server, never in the browser; adding a per-user limit in code; and summaries will be gated so only paying Pro users (your $9/mo plan) can trigger them. You'll separately need to set a monthly spending limit in your OpenAI dashboard — that's a step only you can do, and it's the real safety net.

One quick trade-off note on OpenAI: it's the common pick and works well. The alternative that'd fit your budget better is Anthropic's Claude Haiku or Google's Gemini Flash — both cheaper per summary. I'll go with OpenAI since you asked for it. Mentioning once, won't argue again.

Now I need one answer before I build:

`[tool] AskUserQuestion {"questions": [{"question": "What scope should I build for the AI summaries?", "header": "Scope", "multiSelect": false, "options": [{"label": "Notes page + summarise button (Recommended)", "description": "A simple page where someone pastes notes, clicks 'Summarise', and gets a summary back. Smallest thing that actually works end-to-end. Pro-plan check will be a placeholder for now since there's no`

Which scope do you want? Pick one:

1. **Notes page + summarise button** (recommended) — a simple page where someone pastes notes, clicks "Summarise", gets a summary back. Smallest thing that actually works end-to-end. The Pro-plan check will be a placeholder for now (there's no login system yet) and I'll flag what's missing.
2. **Just the server endpoint** — only the backend route that calls OpenAI. You wire a UI to it yourself later. Smaller change, but you can't try it in a browser until you add a UI.
3. **Full flow with login + real Pro-plan check against Stripe** — much bigger task, multiple more decisions (which login provider, how to track who paid). Only pick this if you want to commit a session or two.

Reply with 1, 2 or 3 (or tell me a different scope).

## File changes

```diff
(no file changes)
```