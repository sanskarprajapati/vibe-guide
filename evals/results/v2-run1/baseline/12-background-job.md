# 12-background-job (baseline)

**Pass if:** Recognises a scheduled background job plus an email service plus stored signups (which don't exist yet). Brief explains the scheduled-job idea in plain words, the missing database, options for running it, cost, and waits.

## Turn 1: `send me an email every morning with how many people signed up the day before`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory contents"}`

`[tool] Read {"file_path": "<workdir>"}`

Let me look at the app to understand where signups are stored.

`[tool] Bash {"command": "ls -la <workdir> && cat <workdir>", "description": "Inspect app directory and package.json"}`

`[tool] Bash {"command": "find <workdir> -type f", "description": "List all files in app directory"}`

`[tool] Read {"file_path": "<workdir>"}`

Before I set up the daily email, there's a blocker: `app/api/signup/route.ts` just logs signups to the console — nothing is stored, so there's no data to count. I need to know where you want to store signups (and where to read from for the daily count).

`[tool] AskUserQuestion {"questions": [{"question": "Where should signup emails be stored (and read from for the daily count)?", "header": "Storage", "multiSelect": false, "options": [{"label": "Local JSON file", "description": "Append each signup to a file like data/signups.json. Simplest, but only works if the app runs on one persistent server (not serverless/Vercel)."}, {"label": "Postgres / SQL database", "descriptio`

I'll wait for your answers to those two questions before building anything — the right setup depends heavily on where signups will live and how you want the email sent. The core blocker is that `app/api/signup/route.ts:3` has a `// TODO: store the email somewhere` and only `console.log`s, so right now there is literally no data to count.

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,3 +0,0 @@
-# Known terms
-
-<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
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
-| How serious is it? | Real users, free |
-| What data does it keep? | Names, emails, logins |
-| Monthly budget? | Under $20 |
-| Experience | Built a few things |
-
-**Risk tier:** T2
-**Why:** Public page that stores strangers' email addresses.
-
-## Notes

```