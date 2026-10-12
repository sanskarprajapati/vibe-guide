# 03-db-card (skill)

**Pass if:** Shows a decision card BEFORE writing integration code: 2-3 options, a recommendation that fits a public T2 page on under $20/month, cost at their size, lock-in. Ends by asking which to use. No exact prices stated as fact.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>/", "description": "List project root directory"}`

`[tool] Bash {"command": "ls -la <workdir>/.vibe/ <workdir>/app/", "description": "List .vibe and app directories"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/app/page.tsx"}`

`[tool] Bash {"command": "ls -la <workdir>/app/api/", "description": "List api directory"}`

`[tool] Bash {"command": "ls <workdir>/app/api/signup/ && cat <workdir>/package.json", "description": "Check signup api and package.json"}`

`[tool] Read {"file_path": "<workdir>/app/api/signup/route.ts"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

Using your profile: public waitlist storing emails, tier T2.

Right now your signup route just logs the email to the terminal and forgets it — nothing is actually saved. Let's pick where to store signups before I wire it up.

You need a place to keep each email address (a **database** [a storage service you can read and write to from your app]). For a public Next.js waitlist on a sub-$20/month budget, here's what fits:

1. **Supabase** (hosted Postgres with built-in access rules), recommended
   - Fits you because: free tier easily covers a waitlist, and it gives you one dashboard for the data plus access rules (**RLS** [row level security — rules that decide which rows the public can read or write]) so random visitors can't read everyone's emails.
   - Cost at your size: free until you're well past a waitlist's worth of rows and traffic.
   - Watch out for: RLS has to be set up right — the default is "no access", which is good, but you need one explicit rule for inserts. I'll do that part.
   - Lock-in: low. Your data is plain Postgres, so you can export and move it.

2. **Firebase Firestore** (Google's hosted database)
   - Fits you because: also has a free tier that covers small waitlists.
   - Cost at your size: free at waitlist scale, but it charges per read and per write — a bug in a loop can cost real money.
   - Lock-in: higher. The data model is Firestore-specific, so moving later is harder.

3. **SQLite file on the server**: not a fit for you, because your app will likely run on serverless hosting (Vercel/Netlify), where the file disappears on every deploy and signups get lost.

`[tool] AskUserQuestion {"questions": [{"question": "Which database should I use to store the waitlist signups?", "header": "Database", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "Hosted Postgres + access rules in one dashboard. Free tier covers a waitlist. Easy to export your data later."}, {"label": "Firebase Firestore", "description": "Google's hosted database. Free at small s`

I'll pause here for your pick between Supabase and Firebase. Once you choose, I'll wire the signup route to store emails there, set up the access rules, and tell you what to paste into the dashboard.

## File changes

```diff
(no file changes)
```