# habit-tracker (old)

**Persona:** You work in marketing and have never written code. You want a simple habit tracker for yourself (things like walking, reading, drinking water). You like clean, minimal looks. You don't know technical words and say so if confused. You're happy to answer questions but get impatient with long walls of text.

## Turn 1

**User:** /vibe build me a habit tracker I can use in my browser, just for me

`[tool] Bash {"command": "ls -la <workdir> 2>&1 | head -50 && echo \"---\" && ls -la <workdir> 2>&1 | head -20", "description": "Check project state and vibe folder"}`

`[tool] Bash {"command": "ls <workdir> 2>&1 && echo \"---templates---\" && ls <workdir> 2>&1", "description": "Check vibe skill templates"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Write {"file_path": "<workdir>", "content": "# Vibe profile\n\n<!-- Written by the /vibe skill. Edit by hand or run /vibe profile. -->\n\n| Question | Answer |\n|---|---|\n| Who will use it? | Just the user (said \"just for me\") |\n| Where does it run? | In a browser, on their own machine (guessed) |\n| How serious is it? `

Here's the plan — a quick read, then your call.

## Plan: a personal habit tracker that opens in your browser

**What you'll end up with:** One file on your computer. Double-click it, your habits open in the browser. Add habits (like "drink water", "read 20 min"), tap a box each day you did it, see your streaks grow.

**How it fits together:**
```
  habit-tracker.html  ──►  your browser  ──►  browser's local storage
  (the whole app:                             (your habits + check marks
   one file)                                   live here, on your machine)
```
That's it. No server, no account, no internet needed after it's built.

**Steps:**
1. Build one `habit-tracker.html` file with the full app inside (list of habits, today's check marks, a weekly grid, streak counts).
2. Save data to your browser's **local storage** (a small built-in notepad every browser has — your habits stay there between visits).
3. Add an **Export** button (downloads your habits as a file) and **Import** (loads it back) — so you can back up, or move to a new computer.
4. Simple, clean styling. Dark mode by default (easier on eyes). Works on phone browser too if you open the file from there.

**Why this way:** You said "just for me", so there's no reason to pay for or set up a database, a login, or a web host. A single HTML file is the smallest thing that works, the easiest to understand, and the hardest to break. You'll own the file forever.

**Other ways to do it:**

| Option | Good | Not so good |
|---|---|---|
| **One HTML file + local storage (plan)** | Free, offline, no setup, nothing to maintain | Data lives in one browser — if you clear browser data without exporting, it's gone |
| Hosted on a free site (GitHub Pages / Netlify) | Open it from any device via a URL | Still per-browser data unless we add a database (which "just for me" doesn't need) |
| Full web app with login + cloud database | Syncs across phone + laptop | Overkill — real monthly cost, accounts, setup; a tutorial would suggest this but it's wrong for your ask |

**Risks, and what I'll do:**
- Losing data if you clear browser cookies/storage → add Export/Import buttons from day one; I'll tell you where to click.
- Only works in the browser you open it in → fine for "just for me"; if you want phone sync later, we add that then.

**Cost:** $0. No services, no accounts.

**You'll need to:** Nothing before I start. After it's done, just double-click the file.

**What changes:** 1 new file (`habit-tracker.html`). No packages installed, no services.

One small question so I build the right thing — pick any (or say "surprise me"):

**Which style feels right?**

`[tool] AskUserQuestion {"questions": [{"question": "Which look and feel do you want for the tracker?", "header": "Style", "multiSelect": false, "options": [{"label": "Clean & minimal, dark mode (Recommended)", "description": "Dark background, soft colors, lots of breathing room. Easy on the eyes, feels calm. Good default for daily use."}, {"label": "Colorful & playful", "description": "Bright colors, rounded corners, li`

(The question picker didn't open — here it is inline.)

**1. Which look and feel for the tracker?**
- **a.** Clean & minimal, dark mode (recommended — easy on eyes, feels calm for daily use)
- **b.** Colorful & playful (bright, rounded, little animations when you check things off)
- **c.** Spreadsheet-style grid (habits down, days across — dense but shows a lot at once)
- **d.** Surprise me (I'll go with **a**)

Reply with the letter (or just **go** for the default), or tell me what to change.

_words: 530 · questions: 2 · files changed: 0 _

## Turn 2

**User:** a sounds good, go for it

Building the file now.

`[tool] Write {"file_path": "<workdir>", "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\" />\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n<title>Habit Tracker</title>\n<style>\n  :root {\n    --bg: #0f1115;\n    --panel: #171a21;\n    --panel-2: #1f232c;\n    --tex`

Now updating the app map so you have a plain-language record of the pieces.

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Write {"file_path": "<workdir>", "content": "# App map\n\n<!-- Kept up to date by /vibe after each big task. Plain words, current state only. -->\n\n**What it does:** A personal habit tracker that runs entirely in your browser. Add habits, check them off daily, see weekly grid and streaks. No account, no internet needed after o`

`[tool] Write {"file_path": "<workdir>", "content": "# Known terms\n\n<!-- Terms explained to the user already. Don't re-explain. -->\n\n- **local storage** \u2014 a small built-in notepad every browser has; stores small bits of data (like your habit list) between visits, scoped to that browser on your machine.\n"}`

Done. Here's what you have.

## Done: your habit tracker

**What changed:**
- New file: `habit-tracker.html` — the whole app in one file.

**How it works now:**
Open `habit-tracker.html` in any browser (double-click it, or drag it onto a browser window). Type a habit at the top, press **Add**. Each habit shows the last 7 days as little squares — tap today's square (it has an outline) to mark it done. Your streak counts the days in a row leading up to today. Everything saves automatically to your browser.

**Check it yourself:**
1. Double-click `habit-tracker.html`. You should see "Habits" at the top and an empty state saying *"No habits yet."*
2. Type "Drink water" and press Add. A row appears with 7 day-squares.
3. Click today's square (the one with the outlined border). It fills with the accent color and your streak jumps to "🔥 1-day streak".
4. Close the tab, reopen the file — your habit is still there.
5. Click **Export** → you get a `habits-2026-10-15.json` file. Save that somewhere (iCloud, Dropbox, email to yourself). That's your backup.

**You still need to:**
- Nothing to run it. One thing to remember: **export every once in a while.** If you ever clear your browser's cookies/history for "all time", or switch browsers, local storage goes with it. The export file is your safety net — click Import to restore.

**Worth understanding:**
- Your data lives *in this one browser*, not on the internet. That's why it's free and private — but it also means it won't appear automatically on your phone or another computer. If you ever want sync, that's a separate (bigger) build with a server; we can revisit then.
- The whole app is readable HTML + JavaScript in one file. If you want to peek at how it works, or tweak colors/text, open it in any text editor — nothing is compiled or hidden.

_words: 335 · questions: 1 · files changed: 1 ['habit-tracker.html']_

**User:** DONE

## Metrics

| Turn | Words | Questions | Files changed |
|---|---|---|---|
| 1 | 530 | 2 | 0 |
| 2 | 335 | 1 | 1 |

- Turns: 2
- First file change on turn: 2
- Most files changed in one turn: 1
- Turns asking more than one question: 1
- Turns ending with no question: 0
- Average words per turn: 432
