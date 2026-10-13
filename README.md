# vibe-guide

A Claude Code skill that keeps you in the loop while Claude builds, for people who build with AI but don't come from a coding background.

Most people end up turning on "bypass permissions" because clicking approve on every file edit is exhausting. After that, Claude works in the dark: you ask for a feature, it runs for ten minutes, touches fifteen files, adds services and background workers, and you get back something you can't explain and didn't really choose.

`/vibe` replaces the approve button with a conversation at the moments that matter:

1. **Brief, before anything big.** What you'll end up with, a small map of how the pieces fit, the steps in plain words, **why this approach**, other ways to do it with pros and cons, the risks and what it'll do about them, the cost, and what you'll have to do yourself. Then it **waits for your go**.
2. **Checkpoints during the work.** A short line as each step finishes. If something changes the plan (a new service is needed, the approach isn't working, something would cost money or delete data), it stops and asks.
3. **Wrap-up after.** What changed, how it works now, how to check it yourself, what's left, and the one or two ideas worth understanding.
4. **Answers anytime.** "Why?" or "what's that?" gets a plain answer, with a diagram if needed.

Small things (a text change, a one-file fix) it just does. Along the way it explains new terms in brackets the first time they come up, like **webhook** (a doorbell Stripe rings when someone pays), and it keeps `.vibe/map.md`, a plain-language map of your app, so you're not lost in your own project two weeks later.

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

Or `/vibe <what you want to build>`. The first time, it reads your project to work out what it is (public or local, does it take payments, what data it keeps), saves that to `.vibe/profile.md`, and asks only what it can't tell, inside its first plan. Type `/vibe` at the start of each session.

How much it talks depends on the size of the task:

| Size | Example | What happens |
|---|---|---|
| Small | change a heading, fix a typo | Done, with one line saying what changed |
| Medium | a feature like ones already in the app | A 3–5 line heads-up, then it builds |
| Big | a database, logins, payments, email, deploys, background jobs, anything that costs money | Full brief, then it waits for your **go** |

| Command | What it does |
|---|---|
| `/vibe` | Turn the mode on for this session |
| `/vibe profile` | Review and update what it knows about your project |
| `/vibe map` | Show the plain-language map of your app |
| `/vibe level new\|some\|dev` | Change how much it explains |
| `/vibe off` | Turn it off for the rest of the session |

At the `dev` level the bracket explanations go away; briefs, alternatives and risks stay, in a compact form.

## How it works

The skill is plain Markdown. No code runs.

```
vibe/
  SKILL.md                     the loop: size the task, brief, build, checkpoint, wrap up
  references/
    briefing.md                templates for briefs, checkpoints, progress lines, wrap-ups
    profile.md                 what to infer from the code, risk tiers (T0 local … T3 money)
    explain-style.md           how to explain, with good and bad examples
    decision-card.md           comparing options, with starting points per tier
    tripwires.md               which risks to raise, at which tier, and what to do
  templates/                   profile, known terms and app map for your project's .vibe/ folder
```

Your answers set a **risk tier**:

| Tier | Meaning | Example |
|---|---|---|
| T0 | Local, only you | a script on your laptop |
| T1 | Shared, low stakes | a tool for friends, no logins |
| T2 | Public or stores personal data | a waitlist that collects emails |
| T3 | Money or sensitive data | a SaaS with Stripe |

The tier decides which tools fit and which risks the brief raises. A T0 script won't get database warnings; a T3 app gets all of them, plus a suggestion to have someone experienced review it before launch.

## Tests

`evals/` has three small sample projects (a local script, a public waitlist, a paid SaaS) and 12 scenarios: small and medium edits, big tasks, saying "go", a question before go, scope growth mid-task, a project with no profile, a background job. After every turn the runner checks automatically whether project files changed, so "nothing happens before your go" is tested, not eyeballed.

```bash
python3 evals/run.py skill
```

```bash
python3 evals/run.py baseline
```

With the skill, 12 of 12 pass. Without it, 7 of 12 pass. Some of the baseline failures happened because the test mode auto-declines Claude's question menu; the clear misses are adding OpenAI and an email service with no question at all. [evals/RESULTS.md](evals/RESULTS.md) has the full write-up, caveats included.

## Limits

- It only works after you type `/vibe`. A skill can't switch itself on in every session; a plugin with a session-start hook can, and that's planned.
- It asks for your go in the chat. It doesn't change Claude Code's permission settings, so it relies on the model following the skill.
- It never claims your app is secure. It tells you what it set up and how to check it.
- It's tested on Claude Code with recent Claude models. Other tools that read `SKILL.md` files may behave differently.

## Roadmap

- Plugin packaging with a session-start hook, so it's on without typing `/vibe`.
- A library of pre-written explainers for common concepts, and animated diagrams you can click through.
- A pre-launch checklist.
- Short explainer videos for concepts that still don't click.

## License

MIT
