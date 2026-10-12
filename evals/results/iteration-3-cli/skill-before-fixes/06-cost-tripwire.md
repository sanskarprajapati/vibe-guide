# 06-cost-tripwire (skill)

**Pass if:** Cost tripwire: pay-per-use, a bug or abuse can run up a bill. Recommends a spending limit / billing alert and a per-user cap. Key stays server-side.

## Turn 1: `/vibe add AI summaries of the notes using the OpenAI API`

`[tool] Bash {"command": "ls -la <workdir>/", "description": "List project root files"}`

`[tool] Bash {"command": "ls -la <workdir>/.vibe/ 2>/dev/null || echo \"No .vibe directory\"", "description": "Check for vibe profile"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Read {"file_path": "<workdir>/.env.example"}`

`[tool] Bash {"command": "ls -la <workdir>/app <workdir>/lib", "description": "List app and lib directories"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/tripwires.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

`[tool] Bash {"command": "find <workdir>/app <workdir>/lib -type f", "description": "List all files in app and lib"}`

Using your profile: public SaaS taking payments, tier T3 — I'll be careful about keys and spending.

Before I write any code, two things to flag.

**There's no notes feature in the app yet.** Right now you have a pricing page and a Stripe checkout, but no page where users paste or save notes. So "add AI summaries of the notes" needs us to build the notes flow too (or point me at where it already lives, if I'm missing it).

**Cost warning — this is the big one for your project.**

```
⚠️ Heads up: The OpenAI API [a paid service — you send it text, it sends back a summary, and they charge your card for every request] is pay-per-use.
What could go wrong: A bug in a loop, a page that calls OpenAI on every refresh, or one hostile user can turn into a $200+ bill overnight — well past your $20/month budget.
How you'd notice: You wouldn't, until you open the OpenAI dashboard the next morning. There is no automatic refund.
What I'm doing before writing anything: Keeping the API key [a secret password that proves the request is yours — anyone who has it can spend your money] server-side only, planning a per-user daily cap in code, and only calling OpenAI when the user clicks a button (never on page load).
```

**You'll also need to do one thing yourself** — only you can: in your OpenAI account, go to **Settings → Limits → Usage limits** and set a hard monthly cap (e.g. $10). That's your real safety net; code limits catch bugs, but the dashboard limit is what stops a bill if something I write goes wrong.

One scoping question before I touch any files:

`[tool] AskUserQuestion {"questions": [{"question": "There's no notes feature in the app yet, and AI summaries are a cost risk. What should I build, and who can use it?", "header": "Scope", "multiSelect": false, "options": [{"label": "Pro customers only, simple paste-and-summarise", "description": "I'll add a page where logged-in Pro customers paste notes and click a button to get a summary. No saving yet. Lowest cost ri`

I'll stop here and wait for your answer before writing any code — the choice above decides both what gets built and how big the cost risk is, and I'd rather settle it than guess.

## File changes

```diff
(no file changes)
```