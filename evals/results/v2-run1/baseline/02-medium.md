# 02-medium (baseline)

**Pass if:** Treated as medium: a short brief (3-5 lines) then the change in the same reply. clean.py updated. Short wrap-up with a way to check it.

## Turn 1: `also drop rows where the city is empty`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List files in working directory"}`

`[tool] Read {"file_path": "<workdir>"}`

I'll update the filter to also require a non-empty city.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    \"\"\"Trim whitespace and drop rows with no email.\"\"\"\n    cleaned = []\n    for row in rows:\n        trimmed = {k.strip(): (v or \"\").strip() for k, v in row.items()}\n        if trimmed.get(\"email\"):\n            cleaned.append(trimmed)\n    ret`

Updated `clean.py:10` so rows are kept only when both `email` and `city` are non-empty.

_Project files changed this turn: clean.py_

## Auto-checks

- PASS: turn 1: project files changed (clean.py)
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/local-script/.vibe/known-terms.md <workdir>
--- evals/fixtures/local-script/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,3 +0,0 @@
-# Known terms
-
-<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
diff -ruN -x .claude evals/fixtures/local-script/.vibe/profile.md <workdir>
--- evals/fixtures/local-script/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>	1970-01-01 05:30:00
@@ -1,17 +0,0 @@
-# Vibe profile
-
-<!-- Written by the /vibe skill. Edit by hand or run /vibe profile. -->
-
-| Question | Answer |
-|---|---|
-| Who will use it? | Just me |
-| Where does it run? | Only on my computer |
-| How serious is it? | Experiment or learning |
-| What data does it keep? | Names, emails, logins |
-| Monthly budget? | $0 |
-| Experience | Brand new |
-
-**Risk tier:** T0
-**Why:** Runs only on my laptop and only I use it. The emails are my own contacts, never online.
-
-## Notes
diff -ruN -x .claude evals/fixtures/local-script/clean.py <workdir>
--- evals/fixtures/local-script/clean.py	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:12
@@ -3,11 +3,11 @@
 
 
 def clean_rows(rows):
-    """Trim whitespace and drop rows with no email."""
+    """Trim whitespace and drop rows with no email or city."""
     cleaned = []
     for row in rows:
         trimmed = {k.strip(): (v or "").strip() for k, v in row.items()}
-        if trimmed.get("email"):
+        if trimmed.get("email") and trimmed.get("city"):
             cleaned.append(trimmed)
     return cleaned
 

```