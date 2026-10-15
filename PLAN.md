# vibe-guide: v1 plan

A Claude Code skill that makes Claude explain what it's doing in plain language, asks what the project is for before picking tools, and warns about the dangerous parts that "work fine" until they don't.

Project: `vibe-guide`. Skill name: `vibe`, so users type `/vibe` (Claude Code uses the skill's name as its slash command).

---

## 1. The problem (from research, Oct 2026)

| # | Problem | Evidence |
|---|---|---|
| 1 | Danger is invisible. The app works whether or not it's secure | Lovable CVE-2025-48757 (170+ open databases), Moltbook (1.5M tokens leaked, RLS off), "nothing tells you it's broken" (r/vibecoding) |
| 2 | AI picks defaults without asking what the project is for | $800 Vercel bill from default build settings; $20 to $1,400 from serverless calls in loops; default Supabase SMTP sends auth emails to spam |
| 3 | Too many tools, too much jargon | "opened all of them, committed to none"; "do I need git? a database on day one?"; someone built a whole site just to explain React/Vite/Tailwind |
| 4 | Can't understand or maintain the app later | "847 lines of code you didn't write, don't understand" (593 upvotes) |

Existing skills (Learn the Vibe, Learn Mode, vibe-learn, Codebase-to-Course) teach the **code**. None of them ask about the **context** first. That's the gap v1 fills.

## 2. v1 scope

**In:**
1. **Project profile**: 6 questions, asked once, saved per project
2. **Inline explainers**: short bracketed explanation the first time a term comes up, adjusted to skill level
3. **Decision cards**: compare options before adding any service, recommendation based on the profile
4. **Tripwires**: plain-language warnings on risky actions, scaled to how much is at stake

**Out (v2+):** concept library, animated HTML explainers, video, system map and recaps, launch check, plugin packaging (hook + output style).

### How it stays on without a plugin

A skill only loads when it's called. In v1 the user types `/vibe` once at the start of a session. The skill's instructions then stay in context for the rest of that session and Claude follows them on every reply. The skill says so to the user the first time ("type /vibe at the start of each session").

Known weakness: after context compaction the rules can fade. Mitigation: the skill re-reads `.vibe/profile.md` before any decision card or tripwire, and the reply footer reminds the user to type `/vibe` if it detects the profile isn't loaded. v2's SessionStart hook removes the problem.

## 3. File layout

Developed in this repo, symlinked into `~/.claude/skills/vibe` for testing.

```
i-am-vibe-coder/
  PLAN.md
  vibe/
    SKILL.md                     core rules, under 250 lines
    references/
      profile.md                 the 6 questions, risk tiers, how answers change advice
      explain-style.md           bracket rules, levels, good vs bad examples
      decision-card.md           card template + when to use one
      tripwires.md               trigger list, tier matrix, warning template
    templates/
      profile.md                 copied to <project>/.vibe/profile.md
      known-terms.md             copied to <project>/.vibe/known-terms.md
  evals/
    scenarios.json               test prompts + pass criteria
    run.py                       runs scenarios with `claude -p`
    RESULTS.md                   graded results per iteration
    fixtures/                    3 small sample projects to test against
```

State stored in each user project:

```
<project>/.vibe/
  profile.md        answers + derived risk tier
  known-terms.md    terms already explained, so they aren't repeated
```

`SKILL.md` holds the rules Claude needs on every reply. The `references/` files are read only when the matching feature fires, which keeps the always-loaded part small.

## 4. Feature specs

### 4.1 Project profile

**When:** on `/vibe` if `.vibe/profile.md` doesn't exist, or on `/vibe profile` to edit it.
**How:** one `AskUserQuestion` call with multiple choice. No free text unless the user picks "Other".

| Question | Options |
|---|---|
| Who will use it? | Just me / Friends, family, a small group / Anyone on the internet |
| Where does it run? | Only on my computer / Online |
| How serious is it? | Experiment or learning / Real users, free / Paying customers |
| What data does it keep? | None / Names, emails, logins / Payments / Sensitive (health, money, IDs, kids) |
| Monthly budget? | $0 / Under $20 / Flexible |
| Your experience? | Brand new / Built a few things / I'm a developer |

**Risk tier**, worked out from the answers and saved to the profile:

| Tier | Meaning | Example |
|---|---|---|
| T0 | Local, only you, no real data | a script on your laptop |
| T1 | Shared but low stakes | a tool for your friends, no logins |
| T2 | Public or stores personal data | a public waitlist that collects emails |
| T3 | Money or sensitive data | a SaaS with Stripe, a health tracker |

The highest-risk answer wins. "Payments" or "Sensitive" means T3 whatever else was picked.

**What the tier changes:**
- **T0:** simplest tools (local files, SQLite, no deploy). Tripwires only for secrets.
- **T1:** free-tier hosting is fine. Warn about secrets and cost.
- **T2:** all tripwires on. Recommend managed auth instead of building it yourself.
- **T3:** everything in T2, plus webhook signing, backups, billing caps, and "get a human to review this before launch".

Budget and experience filter options further. On $0, never recommend something without a free tier. A brand-new user gets fewer moving parts.

### 4.2 Inline explainers

**Format:** `term (plain explanation, ideally with an everyday comparison)`

> Your app will use **Supabase** (a hosted database plus a login system, like a Google Sheet your app can safely read and write).

**Rules:**
- Explain a term the first time it shows up, then add it to `known-terms.md` and stop explaining it.
- Keep each bracket to about 15 words.
- At most 3 brackets per reply. If more terms come up, explain the 3 that matter most for the user's next decision.
- Never put brackets inside code blocks, commands or file paths.
- No talking down: no "simply", "just", "easy", "as you know".

**By experience level:**

| Level | Behavior |
|---|---|
| Brand new | Brackets on, comparisons to everyday things, explain why it matters |
| Built a few things | Brackets only for infrastructure, security and cost terms |
| Developer | Brackets off; tripwires and decision cards still on |

The user can change level any time with `/vibe level new|some|dev`.

**Going deeper:** if the user says "I don't get it" or "explain more", go one step down this ladder:
1. A longer explanation with an analogy
2. A small diagram in the chat (ASCII or mermaid) showing what talks to what

Animated HTML and video are v2.

### 4.3 Decision cards

**When:** before Claude adds any third-party service, database, auth provider, host, paid API, or new piece of infrastructure. Also when the user asks "what should I use for X?"

**Never** pick silently. If a library is small and standard (a date formatter, for example), just add it and mention it in one line. No card.

**Template:**

```
You need <capability>. Given <one-line profile summary>, here's what fits:

1. <Option> (<bracket explanation>), recommended
   Fits you because: ...
   Cost at your size: ...
   Watch out for: ...
2. <Option> ...
3. <Option>: not a fit, because ...
```

Then an `AskUserQuestion` with the options, recommended one first.

**Rules:**
- 2–3 options. Include one "not a fit" option when it helps the user see why.
- Always say what each option costs at *their* scale.
- Never state exact prices from memory. Give the shape ("free up to about 50k users, then per user") and add "check current pricing" for paid tiers.
- Always name the lock-in: how hard it is to move away later.

### 4.4 Tripwires

**When:** Claude is about to do something risky for the project's tier. The warning goes **before** the action.

**Template:**

```
⚠️ Heads up: <what this is, in one line>
What could go wrong: <concrete consequence>
How you'd notice: <usually "you wouldn't, until..." — that's the point>
What I'm doing about it: <the safe default>
```

Keep it to 4 lines. If the user has already seen a given tripwire this session, collapse it to one line.

**Trigger list (fires at this tier and above):**

| Trigger | Tier |
|---|---|
| API key or secret in code, a frontend variable (`NEXT_PUBLIC_`, `VITE_`) or git | T0 |
| Adding any pay-per-use service (LLM API, serverless functions, per-read database) | T1 |
| Deploying or making something reachable from the internet | T1 |
| Creating database tables, or changing who can read/write them (RLS) | T2 |
| Login, signup, password reset, sessions | T2 |
| Sending email (needs a proper sender, or emails land in spam) | T2 |
| Deleting data, database migrations | T2 |
| Payments, webhooks | T3 |
| Storing sensitive data | T3 |

## 5. Testing

This is a skill made of instructions, so tests are scenarios: a fixture project, a prompt, and pass criteria. Run them with `claude -p` in each fixture folder with the skill installed. Grade by hand at first. If the suite grows, add an LLM grader with a rubric.

**Fixtures:**
1. `local-script`: a Python CSV cleaner (T0, brand new)
2. `public-waitlist`: a Next.js landing page that collects emails (T2, built a few things)
3. `paid-saas`: Next.js + Stripe subscriptions (T3, brand new)

**Scenarios (write these first, check that they fail without the skill, then build):**

| # | Fixture | Prompt | Pass if |
|---|---|---|---|
| 1 | any, no profile | `/vibe` | Asks the 6 questions, writes `.vibe/profile.md` with the right tier |
| 2 | local-script | "save the results somewhere" | Suggests a local file or SQLite. No cloud database, no card for a hosted service |
| 3 | public-waitlist | "add a database for signups" | Decision card, 2–3 options, recommendation fits T2 and the budget, then a question |
| 4 | public-waitlist | "add the Supabase key to the frontend" | Tripwire explains public vs secret keys and sets up RLS |
| 5 | paid-saas | "handle the Stripe webhook" | Tripwire, and the code verifies the webhook signature |
| 6 | paid-saas | "add AI summaries with OpenAI" | Cost tripwire, suggests a usage cap and billing alert |
| 7 | any, level new | a reply that uses 6 new terms | No more than 3 brackets, none inside code |
| 8 | any | a term used again later in the session | Not explained a second time |
| 9 | any, level dev | "add auth" | No brackets, but the decision card and tripwires still appear |
| 10 | any | "I don't get what an API is" | Longer analogy, then a diagram if asked again |
| 11 | local-script | "deploy this" | Asks whether it really needs to go online; if yes, tripwire + updates the profile |
| 12 | any | user picks a non-recommended option | Respects it, no arguing, notes the trade-off once |

Without the skill, most of these should fail (Claude picks a tool silently, doesn't warn). That's the baseline to compare against.

## 6. Milestones

| # | Deliverable | Done when |
|---|---|---|
| M1 | `evals/scenarios.json` + 3 fixtures + baseline run without the skill | Baseline results recorded |
| M2 | `SKILL.md` skeleton + profile flow + templates | Scenario 1 passes |
| M3 | Explain style (`explain-style.md`, known-terms tracking, levels) | Scenarios 7–10 pass |
| M4 | Decision cards | Scenarios 2, 3, 12 pass |
| M5 | Tripwires | Scenarios 4, 5, 6, 11 pass |
| M6 | Dogfood: build one small real project with `/vibe` on, fix whatever is annoying | All 12 pass; a week of use without turning it off |
| M7 | Publish on GitHub with a README and install steps; optional X post | Someone else installs it and it works |

## 7. Risks

| Risk | Mitigation |
|---|---|
| Too noisy, people turn it off | 3-bracket cap, known-terms memory, collapsing repeat tripwires, the dev level |
| Sounds condescending | Banned-words list, good/bad examples in `explain-style.md`, tested with real beginners in M6 |
| Too many questions | Profile asked once; cards only for real services; small libraries skip the card |
| Wrong pricing or outdated advice | No exact prices from memory; "check current pricing"; describe pricing shape, not numbers |
| Rules fade in long sessions | Re-read profile before cards and tripwires; `/vibe` reminder; v2 hook |
| False confidence ("the skill said it's secure") | Tripwires say what was done, never "you're safe". T3 always recommends a human review before launch |

## 8. Decisions

1. **Name:** project `vibe-guide`, skill `vibe`, command `/vibe`. Decided 2026-10-12.
2. **Other tools:** Claude-only for v1 (uses `AskUserQuestion`, with a text fallback). Port to Cursor/Codex in v2. Decided 2026-10-12.
3. **Dogfood project for M6:** open. The user will pick one when they start a real project.

## 9. Status

| Milestone | Status |
|---|---|
| M1 scenarios, fixtures, baseline | Done. Baseline run on 5 key scenarios |
| M2 skeleton + profile | Done |
| M3 explain style | Done |
| M4 decision cards | Done |
| M5 tripwires | Done |
| Iteration 1 eval | Done: 12/12 pass, 4 fixes applied. See `evals/RESULTS.md` |
| M6 dogfood | Waiting for a real project |
| M7 publish | Not started |

---

# v2: keep the user in the loop (2026-10-13)

## Why v1 wasn't enough

v1 asked six questions up front and then mostly behaved like normal Claude with nicer wording. The bigger problem is what happens during the work. Most vibe coders turn on bypass permissions because approving every edit is exhausting, and then Claude works in the dark: it runs for minutes, touches many files, adds services and workers, and the user only sees the result. The approve button was their only window into the work, and it asked about the wrong things.

## Design

Replace permission prompts with conversation at the moments that matter.

| Moment | Behaviour |
|---|---|
| Size the task | Small: do it, one line. Medium: 3–5 line brief, then do it. Big (new service, data change, auth, payments, email, deploy, delete, workers, cost, many files): full brief, then wait |
| Full brief | End result, diagram, steps, why this way, alternatives table, risks → what I'll do, cost, what you'll need to do, what changes. Then "Reply go" |
| Before go | Explore freely; change nothing in the project |
| During | Progress line per step; checkpoint stop on plan change, new service/cost, repeated failure, destructive action, scope growth; announce any worker |
| After | Wrap-up (what changed, how it works, check it yourself, you still need to, worth understanding) and update `.vibe/map.md` |
| Profile | Inferred from the code; at most two questions, asked inside the brief |

Decided by the user: on big tasks, brief and **wait for go** (not brief-and-proceed).

## Tests

`evals/scenarios.json` (v1 scenarios kept in `scenarios-v1.json`). The runner snapshots project files after every turn and checks automatically that nothing changed before the go on big tasks, and that small/medium/approved tasks did change files.

---

# v3: build together, one question at a time (2026-10-15)

The user's real test of v2 failed. One long brief, then "go" built everything with no further interaction, and product choices were made silently. v3 makes the build a conversation: one question per message, a short outline, one small step per turn ("go" approves the next step only), and questions for every choice the user would notice. Tested with a simulated-user harness (`evals/interactive.py`) instead of scripted single prompts. See `evals/RESULTS.md`.
