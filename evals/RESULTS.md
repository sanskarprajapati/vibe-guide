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
