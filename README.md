# vibe-guide

A Claude Code skill that builds **with** you instead of **for** you, for people who build with AI but don't come from a coding background.

Most people turn on "bypass permissions" because clicking approve on every edit is exhausting. After that, Claude works in the dark: you say "build me X", it runs for ten minutes, makes dozens of decisions, and hands back a folder you can't explain and never really chose.

`/vibe` turns the build into a conversation:

- **One question at a time.** Each one says why it matters, gives 2–4 options with what each means for you, and recommends one. Your answer shapes the next question.
- **A pitch before any code.** Like a good developer: how it'll work when it's done (from your side), what's on screen vs what happens behind the scenes, and 2–4 features you didn't think of but will probably need. For a bakery: a minimum notice period and a sold-out switch. For a yoga booking page: confirmation emails and self-serve cancellation.
- **A short plan, then small steps.** "Go" starts the next step only. After each step: what was built, how to try it right now, the idea behind it, and the next question.
- **You make the choices you'd notice.** How it looks, how it behaves, what it saves, what it costs, what happens in odd cases. Claude decides only the internals.
- **You learn as you go.** New terms get a plain explanation the first time, like **webhook** (a doorbell Stripe rings when someone pays), and risks come up at the step where they matter.

A real example from the tests, a bakery website: it asked whether orders should be paid online or sent as requests (requests, no card setup yet), then a set menu or custom cakes (both), then pickup or delivery (pickup), then where orders should land (WhatsApp, "I check it all day"). Then it built it in small steps, each one tried before moving on. Along the way it flagged that the WhatsApp number would be public on the page.

Small things (a text change, a colour) it just does. It also keeps `.vibe/map.md`, a plain-language map of your app, so you're not lost in your own project later.

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
| Medium | a feature like ones already in the app | One question if there's a choice you'd notice, then it builds |
| Big | a new app, a database, logins, payments, email, deploys, background jobs, anything that costs money | Questions one at a time, a short plan, then one step per turn |

If you want it to go faster, say "just build the rest" or `/vibe pace milestone`. It will take bigger steps but still stop for choices you'd notice.

| Command | What it does |
|---|---|
| `/vibe` | Turn the mode on for this session |
| `/vibe profile` | Review and update what it knows about your project |
| `/vibe map` | Show the plain-language map of your app |
| `/vibe pace step\|milestone` | One step per turn (default), or bigger steps |
| `/vibe level new\|some\|dev` | Change how much it explains |
| `/vibe off` | Turn it off for the rest of the session |

At the `dev` level the bracket explanations go away; the questions, steps and risks stay.

## How it works

The skill is plain Markdown. No code runs.

```
vibe/
  SKILL.md                     the conversation: one question at a time, short plan, one step per turn
  references/
    briefing.md                a worked example conversation, plus templates for questions and steps
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

The tier decides which tools fit and which risks it raises. A T0 script won't get database warnings; a T3 app gets all of them, plus a suggestion to have someone experienced review it before launch.

## Tests

Two kinds, both using real `claude -p` sessions on small sample projects in `evals/fixtures/`.

**Conversation tests** (`evals/interactive.py`): a second Claude plays a non-technical person and answers each message in character, for up to 10 turns. Each turn records how many questions were asked, how long the message was, and how many files changed.

```bash
python3 evals/interactive.py skill habit-tracker bakery-orders voice-notes waitlist-db
```

On the habit tracker, plain Claude Code built the app in its first reply, and the previous version of this skill sent a 530-word plan and then built everything at once. The current version asked one question per message for four turns, then built one step per turn.

**Scripted tests** (`evals/run.py`): fixed prompts that check, for example, that nothing changes before you agree to a big task.

```bash
python3 evals/run.py skill
```

[evals/RESULTS.md](evals/RESULTS.md) has every round, including what went wrong and the caveats.

## Limits

- It only works after you type `/vibe`. A skill can't switch itself on in every session; a plugin with a session-start hook can, and that's planned.
- It asks for your go in the chat. It doesn't change Claude Code's permission settings, so it relies on the model following the skill.
- Messages still run longer than ideal (about 190 words on average in tests).
- It never claims your app is secure. It tells you what it set up and how to check it.
- It's tested on Claude Code with recent Claude models. Other tools that read `SKILL.md` files may behave differently.

## Roadmap

- Plugin packaging with a session-start hook, so it's on without typing `/vibe`.
- A library of pre-written explainers for common concepts, and animated diagrams you can click through.
- A pre-launch checklist.
- Short explainer videos for concepts that still don't click.

## License

MIT
