# 02-local-storage (skill)

**Pass if:** Uses a local file (CSV/JSON) or SQLite. No hosted database, no cloud service, no decision card for a hosted service. Explains any new term in brackets.

## Turn 1: `/vibe save the cleaned results somewhere so I can look at them later`

`[tool] Bash {"command": "ls -la <workdir>/ 2>&1; echo \"---\"; ls -la <workdir>/.vibe/ 2>&1", "description": "Check working directory and .vibe folder"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/clean.py"}`

`[tool] Read {"file_path": "<workdir>/contacts.csv"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

Using your profile: local script, just you, learning — tier T0.

Simplest fit here is saving to a new CSV file next to your input, since that matches what you already have and opens in any spreadsheet app. No new service or library needed — Python already has what we need.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/clean.py", "old_string": "def main(path):\n    with open(path, newline=\"\") as f:\n        rows = list(csv.DictReader(f))\n    for row in clean_rows(rows):\n        print(row)\n\n\nif __name__ == \"__main__\":\n    main(sys.argv[1] if len(sys.argv) > 1 else \"contacts`

`[tool] Bash {"command": "python clean.py contacts.csv && echo \"---\" && cat contacts_clean.csv", "description": "Run the script and show the saved output"}`

`[tool] Bash {"command": "python clean.py contacts.csv", "description": "Run the cleaner script"}`

I'll skip running it since that needs approval — the change is in place.

**What changed**
- `clean.py` now writes cleaned rows to `contacts_clean.csv` instead of printing them.
- It prints one line telling you how many rows were saved and where.
- You can pass a different output name as a second argument: `python clean.py contacts.csv my_output.csv`.

**What you do**
- Run `python clean.py contacts.csv` as before. Open `contacts_clean.csv` in your spreadsheet app or text editor to look at the results later.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/local-script/clean.py <workdir>/clean.py
--- evals/fixtures/local-script/clean.py	2026-10-12 22:16:59
+++ <workdir>/clean.py	2026-10-12 22:29:06
@@ -12,12 +12,21 @@
     return cleaned
 
 
-def main(path):
+def main(path, out_path="contacts_clean.csv"):
     with open(path, newline="") as f:
         rows = list(csv.DictReader(f))
-    for row in clean_rows(rows):
-        print(row)
+    cleaned = clean_rows(rows)
+    if not cleaned:
+        print("No rows with an email found. Nothing saved.")
+        return
+    with open(out_path, "w", newline="") as f:
+        writer = csv.DictWriter(f, fieldnames=list(cleaned[0].keys()))
+        writer.writeheader()
+        writer.writerows(cleaned)
+    print(f"Saved {len(cleaned)} cleaned rows to {out_path}")
 
 
 if __name__ == "__main__":
-    main(sys.argv[1] if len(sys.argv) > 1 else "contacts.csv")
+    in_path = sys.argv[1] if len(sys.argv) > 1 else "contacts.csv"
+    out_path = sys.argv[2] if len(sys.argv) > 2 else "contacts_clean.csv"
+    main(in_path, out_path)

```