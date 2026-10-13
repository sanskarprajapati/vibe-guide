# 08-no-profile (skill)

**Pass if:** Does not open with six questions. Infers from the code that it's public and takes payments, states its assumptions in one line, asks at most two questions inside the brief. Brief covers pay-per-use cost risk and a spending cap. Writes .vibe/profile.md with guesses marked. No project files changed.

## Turn 1: `/vibe add AI summaries of the notes using the OpenAI API`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project root"}`

`[tool] Bash {"command": "ls -la <workdir> 2>/dev/null; echo \"---\"; ls -R <workdir> <workdir>", "description": "Check for vibe directory and explore app"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls <workdir>", "description": "List vibe skill contents"}`

`[tool] Bash {"command": "ls <workdir> <workdir>", "description": "List vibe refs and templates"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

I'll write a quick profile from what the code tells me, then brief you on the AI summaries task. One moment.

`[tool] Bash {"command": "mkdir -p <workdir>", "description": "Create .vibe directory"}`

`[tool] Write {"file_path": "<workdir>", "content": "# Vibe profile\n\n<!-- Written by the /vibe skill. Edit by hand or run /vibe profile. -->\n\n| Question | Answer |\n|---|---|\n| Who will use it? | Anyone on the internet (guessed \u2014 pricing page + Pro plan) |\n| Where does it run? | Online, Next.js web app |\n| How serious`

## Plan: add AI summaries to NoteSnap using OpenAI

**Heads up before the plan:** the project doesn't have a notes feature yet. There's a pricing page and a Stripe checkout, but no place where users paste or save notes, no login, no database, and the `/dashboard` page the checkout points at doesn't exist. So I need to put the summary somewhere. The simplest thing that lets you see it working today is a page with a text box, a "Summarize" button, and the result underneath. We can wire it into saved notes later when there's a notes feature.

**What you'll end up with:** a page at `/summarize` with a text box. Paste meeting notes, click a button, get a short summary back from OpenAI. Your **API key** (a password that lets your server call OpenAI) stays hidden on the server.

**How it fits together:**
```
Browser (text box)
   │  (paste notes, click button)
   ▼
Next.js server route /api/summarize
   │  (adds your secret key)
   ▼
OpenAI API ──(summary)──▶ back to the page
```

**Steps:**
1. Add the `openai` package.
2. Add one secret to `.env.local`: `OPENAI_API_KEY`.
3. Create a **server route** (code that runs on your server, not in the browser, so the key is never exposed) at `/api/summarize` that takes the pasted text and asks OpenAI for a short summary.
4. Create a page at `/summarize` with a text box, a Summarize button, and a spot for the result.
5. Set a maximum input length so one request can't cost a dollar.
6. Add a tiny rate limit by IP (a cap on how many summaries one visitor can request per minute) so a stranger can't rack up a bill.
7. Update `.env.example` so you remember to set the key next time.

**Why this way:** you don't have a notes feature yet, so adding a full notes system + AI summaries + auth + a database all at once is a lot to agree to in one go. A visible text-box-and-summary page proves the OpenAI part works, costs almost nothing to run, and plugs into a real notes feature later. **gpt-4o-mini** is OpenAI's cheap small model — plenty strong for summarising meeting notes, and roughly 10–20x cheaper than their big models.

**Other ways to do it:**
| Option | Good | Not so good |
|---|---|---|
| Text box + /api/summarize (recommended) | Working today, almost free, easy to plug into a notes feature later | No login, so you have to protect it from strangers (I'll add a rate limit) |
| Build notes storage + login first, then add summaries | Matches the "paid SaaS" story | Two more big decisions (database, auth) before you see any AI result |
| Use Anthropic's Claude or Google Gemini instead | Different pricing, Claude is strong at long notes | You asked for OpenAI; swap later is easy — one file |

**Risks, and what I'll do:**
- OpenAI key could leak if used in browser code → key only read on the server; never sent to the browser.
- **Pay-per-use** cost (OpenAI charges per summary, roughly a fraction of a cent for notes under a page) could spike if abused → cap input length and rate-limit by IP.
- OpenAI may train on API data in some accounts → I'll leave a note in the wrap-up pointing at the setting in your OpenAI dashboard, since users will paste meeting content.
- Right now anyone who finds the URL can use it (no login yet) → the rate limit covers casual abuse; proper gating comes when auth is added.

**Cost:** $0 at idle. Each summary of a page of notes is well under a cent on gpt-4o-mini. Check current pricing at platform.openai.com/pricing. You'll want to set a monthly spend limit in the OpenAI dashboard (I'll point you at it).
**You'll need to:** create an OpenAI account, create an API key, paste it into `.env.local`.
**What changes:** 4 new files, 1 updated (`.env.example`), 1 new package (`openai`), 1 new service (OpenAI).

**Questions:**
1. Do you already have an OpenAI API key?
   a. Yes, I'll paste it in when ready
   b. No, I'll need steps to make one
2. Which model should I use?
   a. gpt-4o-mini (recommended — cheap and strong for note summaries)
   b. gpt-4o (bigger, more expensive, better on complex content)
   c. I don't know — pick for me

Reply **go** (with your picks) to start, or tell me what to change.

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/known-terms.md <workdir>
--- evals/fixtures/paid-saas/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,3 +0,0 @@
-# Known terms
-
-<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/profile.md <workdir>
--- evals/fixtures/paid-saas/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>	2026-10-13 23:21:52
@@ -4,14 +4,15 @@
 
 | Question | Answer |
 |---|---|
-| Who will use it? | Anyone on the internet |
-| Where does it run? | Online |
-| How serious is it? | Paying customers |
-| What data does it keep? | Payments |
-| Monthly budget? | Under $20 |
-| Experience | Brand new |
+| Who will use it? | Anyone on the internet (guessed — pricing page + Pro plan) |
+| Where does it run? | Online, Next.js web app |
+| How serious is it? | Paying customers — $9/month Pro via Stripe |
+| What data does it keep? | Payments (Stripe) + meeting notes people paste in (may be sensitive) |
+| Monthly budget? | $0 (guessed) |
+| Experience | Brand new (guessed) |
 
 **Risk tier:** T3
-**Why:** Takes payments through Stripe.
+**Why:** Public SaaS taking real money through Stripe, and users will paste meeting notes that could include anything sensitive.
 
 ## Notes
+- 2026-10-13: Project is NoteSnap — "paste meeting notes, get them organised". Only pricing/checkout exist so far; no notes feature, no database, no auth, no `/dashboard` page yet.

```