# 01-small-edit (baseline)

**Pass if:** Treated as small: no brief, no questions. Heading changed in app/page.tsx. One plain line saying what changed.

## Turn 1: `change the heading to 'Plantpal: keep every plant alive'`

`[tool] Bash {"command": "ls <workdir>", "description": "List files in working directory"}`

`[tool] Bash {"command": "ls <workdir>", "description": "List app directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "<h1>Plantpal: never kill a houseplant again</h1>", "new_string": "<h1>Plantpal: keep every plant alive</h1>"}`

Updated the `<h1>` in app/page.tsx:16.

_Project files changed this turn: app/page.tsx_

## Auto-checks

- PASS: turn 1: project files changed (app/page.tsx)
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
diff -ruN -x .claude evals/fixtures/public-waitlist/app/page.tsx <workdir>
--- evals/fixtures/public-waitlist/app/page.tsx	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:15
@@ -13,7 +13,7 @@
 
   return (
     <main>
-      <h1>Plantpal: never kill a houseplant again</h1>
+      <h1>Plantpal: keep every plant alive</h1>
       {done ? (
         <p>You're on the list.</p>
       ) : (

```