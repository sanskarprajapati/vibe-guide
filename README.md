# vibe-guide

A Claude Code skill for people who build with AI but don't come from a coding background.

Type `/vibe` and Claude will:

1. **Explain new terms in plain words**, the first time they come up, in brackets: **webhook** (a doorbell Stripe rings when someone pays). It remembers what it has already explained, so it doesn't repeat itself.
2. **Ask what your project is for** before picking tools. Six quick questions: who uses it, where it runs, how serious it is, what data it keeps, your budget, your experience. A script on your laptop and a paid app get very different advice.
3. **Show you the options** before adding any database, login system, host or paid API. You get two or three choices, what each costs at your size, what the catch is, and a recommendation.
4. **Warn you before risky steps**: API keys, database access rules, logins, payments, email, pay-per-use services, deploys. The warning says what could go wrong, how you'd notice, and what it's doing about it.

## Why

Vibe-coded apps tend to break in ways you can't see. A leaked key or an open database looks exactly like a working app. Some examples from 2025–2026:

- 170+ apps built with Lovable shipped with open databases (CVE-2025-48757).
- Moltbook leaked about 1.5 million API tokens because database access rules were never turned on.
- People got surprise hosting bills ($800, $1,400) from default settings and code that called paid services in a loop.

On r/vibecoding, one beginner wrote that you can leave your database wide open and "nothing tells you it's broken."

The other half of the problem is defaults. AI tools pick a popular option without asking what you're building. In this repo's tests, plain Claude Code was asked to "add a database to store the signups" on a public Next.js page. It silently installed SQLite, which loses all its data on hosts like Vercel. With `/vibe`, it showed a choice first and listed SQLite as "not a fit, because the file disappears on every deploy."

## Install

Clone the repo and link the skill into your Claude Code skills folder:

```bash
git clone https://github.com/sanskarprajapati/vibe-guide.git
```

```bash
ln -s "$(pwd)/vibe-guide/vibe" ~/.claude/skills/vibe
```

Or copy the `vibe` folder into `.claude/skills/` inside one project if you only want it there.

## Use

Start a Claude Code session in your project and type:

```
/vibe
```

The first time, it asks the six questions and saves your answers to `.vibe/profile.md` in your project. After that, type `/vibe` at the start of each session, or `/vibe <what you want to build>`.

| Command | What it does |
|---|---|
| `/vibe` | Turn the mode on for this session |
| `/vibe profile` | Answer the six questions again |
| `/vibe level new\|some\|dev` | Change how much it explains |
| `/vibe off` | Turn it off for the rest of the session |

At the `dev` level the explanations go away, but the option cards and warnings stay, in short form.

## How it works

The skill is plain Markdown. No code runs.

```
vibe/
  SKILL.md                     rules that apply to every reply
  references/
    profile.md                 the six questions and risk tiers (T0 local … T3 money)
    explain-style.md           how to explain, with good and bad examples
    decision-card.md           the option template and starting points per tier
    tripwires.md               what to warn about, at which tier, and what to do
  templates/                   files copied into your project's .vibe/ folder
```

Your answers set a **risk tier**:

| Tier | Meaning | Example |
|---|---|---|
| T0 | Local, only you | a script on your laptop |
| T1 | Shared, low stakes | a tool for friends, no logins |
| T2 | Public or stores personal data | a waitlist that collects emails |
| T3 | Money or sensitive data | a SaaS with Stripe |

The tier decides which tools fit and which warnings appear. A T0 script won't get database warnings; a T3 app gets all of them, plus a suggestion to have someone experienced review it before launch.

## Tests

`evals/` has three small sample projects (a local script, a public waitlist, a paid SaaS) and 12 scenarios. Each one has a prompt and a pass rule.

```bash
python3 evals/run.py skill
```

```bash
python3 evals/run.py baseline
```

All 12 pass with the skill. [evals/RESULTS.md](evals/RESULTS.md) has the full write-up, including what plain Claude Code did without it. Two examples from those runs: it installed SQLite on a serverless app, and it shipped an OpenAI endpoint anyone could call with no limits.

## Limits

- It only works after you type `/vibe`. A skill can't switch itself on in every session; a plugin with a session-start hook can, and that's planned for v2.
- It never claims your app is secure. It tells you what it set up and how to check it.
- It's tested on Claude Code with recent Claude models. Other tools that read `SKILL.md` files may behave differently.

## Roadmap

- **v2:** a library of pre-written explainers for common concepts, animated diagrams you can click through, a pre-launch checklist, and plugin packaging so it's always on.
- **v3:** short explainer videos for concepts that still don't click.

## License

MIT
