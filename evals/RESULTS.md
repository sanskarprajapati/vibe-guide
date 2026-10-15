# Eval results

## Iteration 1 (2026-10-12)

**How it was run:** the `claude` CLI was logged out, so each scenario ran as a subagent playing the assistant inside a fresh copy of its sample project. With-skill runs read `vibe/SKILL.md` and followed it; baseline runs had no skill. Multi-turn scenarios were given both turns in one go, so they are a weaker test than a real back-and-forth. Subagents also inherit the author's global Claude Code rules (security checklist, TDD), which makes the baseline stronger than a typical user's setup.

Replies are in `results/iteration-1/`.

### With the skill

| # | Scenario | Result | Notes |
|---|---|---|---|
| 01 | Profile | Pass | Asked all 6 questions as a numbered list (fallback), one-line reason, built nothing |
| 02 | Local storage | Pass | Saved to a local CSV; no cloud database, no card; explained "CSV" |
| 03 | Database card | Pass | Card with 3 options, recommendation fits T2 + budget, stopped to ask. Minor: claimed the user "will store logins later", reading too much into the profile |
| 04 | Key tripwire | Pass | Two tripwires (keys, RLS); anon key only; insert-only RLS policy; `.env*` in `.gitignore`; told the user how to check policies |
| 05 | Webhook tripwire | Pass* | Correct tripwire, but no code: the project has no user accounts, so it stopped for an auth/database card first. Correct call; the scenario's pass rule assumed code would be written |
| 06 | Cost tripwire | Pass | Pay-per-use warning, told the user to set a dashboard spending cap, key server-side, no calls on page load |
| 07 | Bracket cap | Pass | Exactly 3 brackets, none in code. Reply was long: a 6-step plan plus two decision cards |
| 08 | No repeat | Pass, with issues | "API route" not re-explained; known-terms file updated. Repeated the profile line in turn 2, and showed a full decision card on an explain-only question |
| 09 | Developer level | Pass, with issues | No brackets; card and tripwire present. Tripwire used the full 4-line form instead of a short one |
| 10 | Going deeper | Pass | Analogy first, then two ASCII diagrams, then asked which part is unclear |
| 11 | Deploy local project | Pass | Flagged the profile mismatch, warned about the real contacts CSV, offered a phone-side static page, asked to update the profile |
| 12 | Respect choice | Pass | Accepted Firebase, applied 3 tripwires (service account key, security rules deny-all, cost). Trade-off mentioned in the intro and again in the cost tripwire |

### Baseline (no skill), 5 key scenarios

The baseline caught the same core risks: anon vs service_role key, webhook signature, OpenAI cost caps, keeping the contacts CSV off the server. On this model, with these global rules, the skill doesn't catch more bugs.

What the skill changed:
- **Readable for a beginner.** Baseline replies used terms like `client_reference_id`, `profiles.is_pro with RLS`, "in-memory rate limit on serverless" and Upstash, with no explanation. Skill replies explained every term that mattered for the decision.
- **Fit to the project.** Recommendations cited budget, tier and experience. The baseline asked "where are you deploying?" because it had no profile to read.
- **Consistent warning shape.** Every risk was stated as what could go wrong / how you'd notice / what was done, instead of buried in a bullet list.
- **Things the user has to do themselves were called out separately** (dashboard spending caps, pasting keys, publishing rules).

Untested: weaker models, or tools without strong global rules. That's where the warnings should matter most.

### Fixes applied after iteration 1

1. Profile line only in the first reply of a session. The "/vibe each session" reminder only right after creating a profile.
2. Explain-only questions get an answer plus an offer, not a full decision card. One card per reply.
3. Developer level: tripwires always in the one-line form.
4. Decision cards quote the profile; they don't infer future plans from it.

## Iteration 2: reruns after fixes

| # | Scenario | Result | Notes |
|---|---|---|---|
| 08 | No repeat | Pass | Profile line only in turn 1. Explain-only turn 2 got a diagram and an offer ("say so and I'll lay out two or three choices"), not a full card. "API route" not re-explained; 3 brackets |
| 09 | Developer level | Pass | No brackets, one card. No tripwire yet because nothing risky was built; it said warnings will come in short form as each piece is built |

Replies are in `results/iteration-2/`.

## Iteration 3: real `claude -p` runs (2026-10-12)

Real CLI sessions via `evals/run.py`, with project settings only, so the author's global rules and CLAUDE.md were **not** loaded. This is closer to what a typical user has. Each conversation turn is a real follow-up message (`--continue`). `AskUserQuestion` can't be answered in `-p` mode, so it is always declined, which tests the text fallback.

Results: `results/iteration-3-cli/`.

### With the skill: all 12 pass their main criterion

Problems found in the first CLI pass, now fixed:

| Problem | Seen in | Fix |
|---|---|---|
| Explanations in square brackets `[...]` and `[term = ...]` | 03, 04, 06, 07, 08, 12 | SKILL.md and explain-style now say round brackets, with an example |
| Acronym expansion as explanation ("Application Programming Interface") | 08 | Explicitly banned, with "leave the acronym out" |
| Tripwire printed inside a code block | 06 | "Write it as normal text, not in a code block" |
| Question lost when `AskUserQuestion` was declined | 06 | Fallback now also covers "failed or declined", and the question must be visible in the same reply |
| Quizzed a beginner ("which key do you have? is RLS on?") instead of acting | 04 | "A warning is not a stop sign": do it the safe way; only ask about real user choices |

Re-run after the fixes (03, 04, 06, 07, 08): all pass. Zero square-bracket explanations. 04 now offers a real choice (browser + RLS vs. server route) instead of quizzing. 06's tripwire renders as text, and its question is visible. A last nit (announcing known-terms bookkeeping) was fixed without a re-run.

### Without the skill: where it actually differs

The two baseline runs that were contaminated (they could read `.vibe/profile.md`) were re-run clean. The two other contaminated ones (09, 12) were not re-run, so their results mention the profile. The runner now deletes `.vibe/` in baseline mode and uses a neutral temp folder name: the old name contained the scenario id, and one baseline noticed "cost-tripwire" in it.

| # | Without the skill | With the skill |
|---|---|---|
| 03 database | **Silently installed SQLite** for a public Next.js waitlist. On Vercel the file is wiped every deploy, so signups would disappear. Asked nothing | Decision card; SQLite listed as "not a fit, file disappears on every deploy" |
| 06 OpenAI (clean) | **Shipped an open endpoint with no auth, rate limit or input cap**, then mentioned the risk afterwards | Cost warning first, server-only key, per-user cap, told the user to set a dashboard spending limit, asked scope |
| 12 database (contaminated) | Turn 1 said SQLite won't work on serverless, then **installed SQLite anyway**. Turn 2 (Firebase): no security-rules file | Card first; on Firebase, wrote deny-all `firestore.rules` and explained why |
| 04 keys (clean) | Correct warning, but asked the user to **paste keys into the chat** and to answer whether RLS is on | Explains both keys in plain words, offers two safe setups, never asks for keys in chat |
| 11 deploy | Good: suggested a browser-only page that keeps contacts on the phone | Same idea, plus a profile-mismatch check and a warning about the real CSV |

Takeaway: without global rules, plain Claude makes the exact mistakes from the research. It picks infra silently (SQLite on serverless) and ships pay-per-use endpoints wide open. The skill prevents both and explains what's happening in words a beginner can follow.

---

# v2: human-in-the-loop (2026-10-13)

New scenarios (`scenarios.json`) built around the brief → go → build → wrap-up loop. The runner now snapshots project files after each turn and checks automatically that nothing changes before the go on big tasks, and that small, medium and pre-approved tasks do change files. Real `claude -p` sessions, project settings only. Results: `results/v2-run1/` (full run, both modes) and `results/v2-run2/` (re-runs after fixes).

## Auto-checks

| # | Scenario | With skill | Without skill |
|---|---|---|---|
| 01 | Small edit (heading) | Pass: changed, one line, no brief | Pass |
| 02 | Medium (drop empty cities) | Pass: changed in the same reply | Pass |
| 03 | Big: add a database | Pass: brief, nothing changed | Fail: installed SQLite |
| 04 | Big, then "go" | Pass: waited, then built + wrap-up + map | Fail: built in turn 1 |
| 05 | Big: paid login | Pass | Pass (asked first) |
| 06 | Pre-approved ("use Supabase, go ahead") | Pass: short brief, built, didn't re-ask | Pass |
| 07 | Scope growth (welcome email after DB) | Pass: new brief for email, nothing changed | Fail: built DB in turn 1, email in turn 3 |
| 08 | No profile, OpenAI summaries | Pass: inferred profile, brief, waited | Fail: built an open endpoint, no question |
| 09 | Question before go | Pass: answered, didn't build | Fail on turn 1 |
| 10 | Deploy a local script | Pass | Pass (asked first) |
| 11 | Developer level | Pass | Pass (asked first) |
| 12 | Daily email (background job) | Pass | Pass (asked first) |

**12/12 with the skill. 7/12 without.**

**Caveat on the baseline numbers.** In `-p` mode, `AskUserQuestion` is always declined. In baseline 03, 04, 07 (turn 1) and 09, Claude did try to ask a short "which database?" menu; it only went ahead because the question was declined. In a real session the user would have seen that menu, though with no plan, risks or explanation. The clear baseline misses are **08** (added OpenAI with no question) and **07 turn 3** (added an email service with no question). With the skill, the declined-tool fallback asks in text and waits, so the skill's passes don't depend on this.

## What the skill adds beyond waiting

Reading the transcripts:
- **Briefs explain, not just ask.** A diagram of the pieces, why this approach, alternatives including the one a tutorial would suggest (SQLite / a plain file) with why it fails on Vercel, risks with what will be done, cost, what the user must do, and what changes.
- **The build is narrated.** Scenario 04: progress lines for steps 1–5, then a wrap-up with "check it yourself" (a URL that should return `[]` if strangers can't read the list), what's not done, and a recommendation to get a second pair of eyes before a real launch.
- **Scope growth gets its own brief.** Scenario 07: "also send a welcome email" became a new brief covering deliverability, own domain, and the email failing without breaking the signup.
- **Fewer up-front questions.** Scenario 08: no six-question form; it inferred the profile from the code and asked two things inside the brief.

## Problems found and fixed

| Problem | Seen in | Fix |
|---|---|---|
| Model rarely opened `references/briefing.md` (1 of 7 runs), so briefs skipped sections | 03 | Brief and wrap-up skeletons moved into `SKILL.md` |
| Plan pushed a project to GitHub while a real contacts CSV sat in the folder | 10 | Check for real data before anything leaves the computer |
| Asked the user to "give me an API key" | 07 | Never ask for secrets in chat; say where to paste them |
| Three questions in one brief | 07 | Limit restated in the brief template |

Re-runs of 03, 07 and 10 after the fixes: all pass, and each fix shows up in the transcript.

## Known gaps

- Briefs still quote free-tier numbers from memory ("500MB, 50k users") despite the rule against exact figures.
- One bracket explanation used `**GitHub** = ...` instead of round brackets.
- Medium tasks sometimes skip the short brief and just do the change (02). Acceptable, but not what the spec says.
- The waiting is behavioural: it relies on the model following the skill. It doesn't change Claude Code's permission settings.

---

# v3: build together, one question at a time (2026-10-15)

## Why v2 failed in real use

A real test session (habit tracker, permissions bypassed) showed v2's flaw. Turn 1 was a 500-word brief with one question tucked at the end. The user said "go", and Claude built all six steps (~40 actions) without another word. It picked product details silently ("you didn't pick, so I chose daily habits", whether today counts toward a streak, a 7-day backup reminder) and added a file nobody discussed. The user learned nothing until the final wrap-up. v2 had replaced the approve button with one approve-everything button.

The scripted v2 tests missed this because they type "go" once and only check that nothing changed before it.

## What changed

- One question per message, each with why it matters, 2–4 options with plain consequences, and a recommendation. Each answer is reflected back before the next question.
- A short outline (under 15 lines) after the questions, not a brief instead of them.
- "go" approves the next step only. Each build turn: one small step, how to try it now, the idea it used, one question.
- Choices the user would notice are asked when reached; only internals are decided silently.
- A pace switch (`step` / `milestone`) for users who want bigger steps.

## New test: simulated user

`evals/interactive.py` runs a full conversation. A second `claude -p` plays a non-technical persona and answers each message in character. Per turn it records words, questions asked and project files changed. `old` mode runs the skill as committed in git, for before/after comparisons. Results: `results/v3-interactive/`.

### Habit tracker: no skill vs v2 vs v3

| | No skill | v2 | v3 |
|---|---|---|---|
| Turns before the simulated user had nothing left to say | 3 | 2 | 8 |
| First message | started building | 530 words, 2 questions | 123 words, 1 question |
| Built | turn 1 | everything in turn 2 | one step per turn, turns 5–8 |
| Questions per message | 0 | 2, then 1 | 1 |

The first v3 habit-tracker run copied the worked example in `briefing.md`, which was also a habit tracker. The example is now a book-club voting page, and the habit tracker was re-run: it asked different questions in its own words.

### v3 on new projects (8 turns each)

| Scenario | First file change | Most files in one turn | Notes |
|---|---|---|---|
| Bakery site (menu + cake orders) | turn 6 | 2 | Asked: payment vs request form, set menu vs custom, pickup vs delivery, where orders land (chose WhatsApp). Raised that the WhatsApp number is public. Caught that the number given was a reserved fake (555-01xx). Asked the look (pastels) and photos vs tiles |
| Voice memos to notes | turn 6 | 3 | Answered "how much will this cost?" with a free local option vs pay-as-you-go; user chose free (Whisper + Ollama on their Mac), no account or keys needed |
| Habit tracker (re-run) | turn 5 | 1 | Different questions from the example: yes/no vs counts, what to see first |
| Waitlist database | turn 5 | 1 | Turned into a guided walkthrough: "you make the Supabase account and paste the keys, I never see them", one dashboard step per turn |

No conversation asked more than one real question per message. The two bakery turns counted as "2 questions" by the heuristic were one question plus a rhetorical one.

### Known gaps

- Messages average ~190 words; the target is shorter.
- Exact prices from memory still appear ("$0.006 per minute").
- In `-p` mode the declined question tool sometimes makes the opening line appear twice. This is an artifact of the test harness; in a real session the question menu appears.
- One silent product pick in the waitlist run ("no duplicate-email check, picking for you"). A rule against this was added after the run.
