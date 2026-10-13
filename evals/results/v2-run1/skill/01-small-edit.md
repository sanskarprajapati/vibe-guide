# 01-small-edit (skill)

**Pass if:** Treated as small: no brief, no questions. Heading changed in app/page.tsx. One plain line saying what changed.

## Turn 1: `/vibe change the heading to 'Plantpal: keep every plant alive'`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory"}`

`[tool] Bash {"command": "ls -la <workdir> <workdir>", "description": "List .vibe and app directories"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "<h1>Plantpal: never kill a houseplant again</h1>", "new_string": "<h1>Plantpal: keep every plant alive</h1>"}`

Done. Updated the heading in `app/page.tsx:16` to "Plantpal: keep every plant alive".

_Project files changed this turn: app/page.tsx_

## Auto-checks

- PASS: turn 1: project files changed (app/page.tsx)
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/app/page.tsx <workdir>
--- evals/fixtures/public-waitlist/app/page.tsx	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:14
@@ -13,7 +13,7 @@
 
   return (
     <main>
-      <h1>Plantpal: never kill a houseplant again</h1>
+      <h1>Plantpal: keep every plant alive</h1>
       {done ? (
         <p>You're on the list.</p>
       ) : (

```