# 03-db-card (skill)

**Pass if:** Shows a decision card BEFORE writing integration code: 2-3 options, a recommendation that fits a public T2 page on under $20/month, cost at their size, lock-in. Ends by asking which to use. No exact prices stated as fact.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>/ && echo \"---\" && ls -la <workdir>/.vibe/ 2>/dev/null || echo \"no .vibe dir\"", "description": "Check for profile and project files"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Bash {"command": "cat <workdir>/README.md <workdir>/package.json && echo \"---\" && ls -la <workdir>/app/", "description": "Read README, package.json, and list app directo`

`[tool] Bash {"command": "find <workdir>/app -type f | head -20", "description": "List all app files"}`

`[tool] Read {"file_path": "<workdir>/app/page.tsx"}`

`[tool] Read {"file_path": "<workdir>/app/api/signup/route.ts"}`

Using your profile: public waitlist storing emails, tier T2. Let me check the vibe references so my recommendation fits.

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/tripwires.md"}`

You need a place to store the emails from your waitlist so they survive restarts and you can see them later. A **database** (a stored table of rows, like a spreadsheet a program can read and write) is the right shape here. For a public Next.js waitlist on a <$20 budget, here are the fits:

1. **Supabase** (hosted Postgres with built-in access rules), recommended
   - Fits you because: free tier covers way more signups than a launch waitlist needs, and it comes with the access-rule system you'll need since the page is public.
   - Cost at your size: free until you're well past typical waitlist scale; no per-read charges.
   - Watch out for: the access rules (called **RLS** — row level security) have to actually be set up. I'd handle that for you.
   - Lock-in: it's plain Postgres underneath, so your data can be exported and moved later.

2. **Neon** (just a hosted Postgres database, nothing else)
   - Fits you because: cheapest and simplest if you only want a database.
   - Cost at your size: generous free tier.
   - Watch out for: no built-in access rules — your API route is the only gatekeeper, so a bug there has no backstop. More for you to get right.

3. **Firebase**: not a fit here. It charges per read/write, and its data model is harder to leave later. Overkill for a list of emails.

`[tool] AskUserQuestion {"questions": [{"question": "Which database should I wire up for your signups?", "header": "Database", "multiSelect": false, "options": [{"label": "Supabase (Recommended)", "description": "Postgres + access rules in one place. Free tier is more than enough for a waitlist."}, {"label": "Neon", "description": "Just Postgres, nothing else. Simpler, no built-in access rules."}, {"label": "Firebase", "`

Which one would you like? Reply with:
- **a** — Supabase (recommended)
- **b** — Neon
- **c** — Firebase

I'll stop here and wait for your pick before adding anything.

## File changes

```diff
(no file changes)
```