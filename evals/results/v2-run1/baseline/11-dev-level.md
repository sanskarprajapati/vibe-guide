# 11-dev-level (baseline)

**Pass if:** Brief is compact and technical: no bracket explanations, but still has the plan, alternatives, one-line risks, and waits for go.

## Turn 1: `add user login so only paying users can see /dashboard`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory contents"}`

`[tool] Bash {"command": "find <workdir> -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -50", "description": "List all files in project"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Before I start, this touches on some choices I shouldn't make alone — the project currently has no auth system and no database (users and their paid status need to live somewhere, and Stripe needs a way to link a payment back to a user).

`[tool] AskUserQuestion {"questions": [{"question": "Which auth + user storage approach do you want?", "header": "Auth stack", "multiSelect": false, "options": [{"label": "NextAuth + Prisma/SQLite (Recommended)", "description": "Self-hosted. Auth.js with email/Google login, Prisma schema with User + isPaid field, Stripe webhook flips the flag. Full control, no new vendor."}, {"label": "Clerk + Stripe", "description": "Ma`

The user cancelled the question prompt, so I'll wait for them to respond directly rather than retry. I need to know their auth stack preference before I can implement — the project has no DB, no auth, and no way to associate a Stripe payment with a user, so I can't move forward without a direction. Which approach would you like?

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/known-terms.md <workdir>
--- evals/fixtures/paid-saas/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,3 +0,0 @@
-# Known terms
-
-<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
diff -ruN -x .claude evals/fixtures/paid-saas/.vibe/profile.md <workdir>
--- evals/fixtures/paid-saas/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,17 +0,0 @@
-# Vibe profile
-
-<!-- Written by the /vibe skill. Edit by hand or run /vibe profile. -->
-
-| Question | Answer |
-|---|---|
-| Who will use it? | Anyone on the internet |
-| Where does it run? | Online |
-| How serious is it? | Paying customers |
-| What data does it keep? | Payments |
-| Monthly budget? | Under $20 |
-| Experience | Brand new |
-
-**Risk tier:** T3
-**Why:** Takes payments through Stripe.
-
-## Notes

```