# 02-medium (skill)

**Pass if:** Treated as medium: a short brief (3-5 lines) then the change in the same reply. clean.py updated. Short wrap-up with a way to check it.

## Turn 1: `/vibe also drop rows where the city is empty`

`[tool] Bash {"command": "ls -la <workdir> 2>&1 | head -50", "description": "List project directory contents"}`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List .vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Small change — adding a city check next to the existing email check.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    \"\"\"Trim whitespace and drop rows with no email.\"\"\"\n    cleaned = []\n    for row in rows:\n        trimmed = {k.strip(): (v or \"\").strip() for k, v in row.items()}\n        if trimmed.get(\"email\"):\n            cleaned.append(trimmed)\n    ret`

Quick test to confirm it does what you'd expect on your sample file.

`[tool] Bash {"command": "python3 clean.py", "description": "Run clean.py on contacts.csv"}`

Done. `clean.py` now drops any row where email **or** city is empty.

On your file:
- Asha (Pune) kept
- Ravi — dropped (no email, was already)
- Meera (Jaipur) kept

Nothing with an empty city in your current sample, but if you add one it'll be dropped the same way.

_Project files changed this turn: clean.py_

## Auto-checks

- PASS: turn 1: project files changed (clean.py)
- .vibe/map.md exists: False

## File changes

```diff
diff -ruN -x .claude evals/fixtures/local-script/clean.py <workdir>
--- evals/fixtures/local-script/clean.py	2026-10-12 22:16:59
+++ <workdir>	2026-10-13 23:20:34
@@ -3,11 +3,11 @@
 
 
 def clean_rows(rows):
-    """Trim whitespace and drop rows with no email."""
+    """Trim whitespace and drop rows with no email or no city."""
     cleaned = []
     for row in rows:
         trimmed = {k.strip(): (v or "").strip() for k, v in row.items()}
-        if trimmed.get("email"):
+        if trimmed.get("email") and trimmed.get("city"):
             cleaned.append(trimmed)
     return cleaned
 

```