# 03-big-brief (skill)

**Pass if:** Full brief: end result, a diagram, plain steps, why this way, an alternatives table with pros/cons (SQLite shown as not a fit on serverless), risks with what it will do, cost, what the user must do, what changes. Ends asking for go. No project files changed.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir> && echo \"---\" && ls -la <workdir> 2>/dev/null || echo \"no .vibe dir yet\"", "description": "List project and check for .vibe dir"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls -la <workdir> && echo \"---package.json---\" && cat <workdir>", "description": "Inspect app dir and package.json"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls -la <workdir> && find <workdir> -type f", "description": "List api dir contents"}`

`[tool] Read {"file_path": "<workdir>"}`

Working from your profile: public waitlist with emails, tier T2.

Right now `/api/signup` just prints the email to the server log and forgets it. The console entry disappears when the server restarts, so no one is actually on the list. Let me brief you before I touch anything.

---

## Brief: store waitlist signups in a database

**What I'll do**
- Add a hosted **database** (an online table that keeps data between restarts) with one table: `signups` (email, signed-up-at, source).
- Rewrite `app/api/signup/route.ts` to insert the email instead of logging it. Handle "already signed up" quietly (no error for the visitor).
- Keep the key for writing to the database in a `.env.local` file (not committed to git) and in your hosting provider's secrets.
- Lock the database so strangers on the internet **cannot read the signup list** — only your server can.
- Give you a dashboard URL where you can view/export your signups.

**Options** (all have a free tier that fits under $20/mo for a waitlist)

| Option | Good | Trade-off |
|---|---|---|
| **Supabase** (recommended) | Free tier is generous (500MB, 50k rows). Nice web dashboard to view/export emails as CSV. Built-in **access rules** (settings that say who can read what) so emails can't leak. Signup with GitHub, no card. | One more account to manage. |
| **Vercel Postgres / Neon** | If you deploy to Vercel, it slots in with one click. | Dashboard is less friendly for just "show me my emails." Free tier smaller. |
| **Google Sheet via API** | Zero new accounts, you already know Sheets. | Slower, flakier, harder to lock down, not a real database — fine for 50 signups, bad at 5,000. |

**Risks I'll handle for you**
- *Email list leaking:* I'll set access rules so only your server (holding a secret key) can read or write. The public key the browser could see cannot read the table.
- *Duplicate signups / spam clicks:* I'll make `email` unique so the same person can't fill the table.
- *Bots:* No bot protection in this task. Fine for a quiet launch; if the page goes viral I'd add a check later (own brief).
- *Legal (strangers' emails):* You'll want a one-line note on the page saying "we'll email you about Plantpal." Not blocking — flagging now.

**What you'll need to do** (if you pick Supabase)
1. Sign in at supabase.com with GitHub (free, no card).
2. Create a project; copy two values from Settings → API into a file I'll make.
3. Everything else I do.

**Not doing** (unless you ask): sending welcome emails, admin page in the app, bot protection, analytics.

---

Which way do you want to go?

`[tool] AskUserQuestion {"questions": [{"question": "Which database should I use for the signups?", "header": "Database", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "Hosted Postgres with a nice dashboard to view/export emails. Free tier easily covers a waitlist. Best fit for your tier and budget."}, {"label": "Vercel Postgres / Neon", "description": "Hosted Postgres from the same`

Which database should I use?

1. Pick one:
   - **a)** Supabase (recommended) — hosted database with a friendly dashboard, free tier easily covers a waitlist.
   - **b)** Vercel Postgres / Neon — hosted database that slots in if you deploy on Vercel; plainer dashboard.
   - **c)** Google Sheet — signups land in a sheet; simplest to peek at but not a real database.
   - **d)** Something else — tell me what you have in mind.

I'll wait for your pick before changing any files or signing anything up.

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
(no file changes)
```