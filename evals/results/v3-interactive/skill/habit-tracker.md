# habit-tracker (skill)

**Persona:** You work in marketing and have never written code. You want a simple habit tracker for yourself (things like walking, reading, drinking water). You like clean, minimal looks. You don't know technical words and say so if confused. You're happy to answer questions but get impatient with long walls of text.

## Turn 1

**User:** /vibe build me a habit tracker I can use in my browser, just for me

`[tool] Bash {"command": "ls -la <workdir> 2>&1 | head -30", "description": "List project folder contents"}`

`[tool] Bash {"command": "ls -la <workdir> 2>&1", "description": "Check for existing vibe profile"}`

`[tool] Bash {"command": "ls <workdir> 2>&1", "description": "Check skill references"}`

`[tool] Read {"file_path": "<workdir>"}`

A habit tracker just for you, in the browser — nice. Before I start, one shaping question.

`[tool] AskUserQuestion {"questions": [{"question": "What does \"tracking a habit\" look like for you day to day?", "header": "Habit style", "multiSelect": false, "options": [{"label": "Daily yes/no tick", "description": "Each habit is one checkbox per day: did it, or didn't. Simplest to use and simplest to build. Great if your habits are things like 'meditate' or 'no soda'. (my pick to start)"}, {"label": "A count per d`

A habit tracker just for you, in the browser — nice. Before I start, one shaping question that decides the whole look of the app.

**What does "tracking a habit" look like for you day to day?**

a. **Daily yes/no tick.** Each habit is one checkbox per day: did it, or didn't. Simplest to build and simplest to use. Great if your habits are things like "meditate" or "no soda". *(my pick to start)*

b. **A count per day.** Each habit has a number: "3 pushup sets", "20 pages read". More flexible, but more taps to log. Good if daily targets matter more than streaks.

c. **Mix of both.** Some habits are yes/no, others are counts — you pick when adding one. Most flexible, slightly more interface to learn.

_words: 146 · questions: 1 · files changed: 0 _

## Turn 2

**User:** A, let's keep it simple.

Simple it is. Yes/no ticks keep both the screen and the data tiny.

Next shaping question: **when you open it, what do you want to see first?**

a. **Just today.** A short list of your habits with a checkbox next to each. Tap one, it's ticked. Yesterday is gone from view. Cleanest to look at. *(my pick)*

b. **A grid of the last 7 days.** Habits down the side, days across the top, a dot in each cell you ticked. Harder to misread a streak, but busier on screen.

c. **Both, side by side.** Today's list on top, the grid underneath. More to look at every morning, but you see your streaks without clicking.

_words: 114 · questions: 1 · files changed: 0 _

## Turn 3

**User:** a sounds perfect, keep it clean

Clean today-view, got it. Yesterday fades away as soon as the clock turns over.

Next thing to decide — and this one has a small catch worth knowing: **where should your ticks be saved?**

a. **Only in this browser** (called **local storage** — a small notebook your browser keeps for this page). No setup, instant, nothing leaves your computer. Catch: if you clear your browser's site data, or use a different browser, your history is gone. *(my pick, given "just for me")*

b. **Local, plus a download button.** Same as (a), but there's a "Backup" button that saves a tiny file you can keep somewhere safe. One extra button on the screen, but your history isn't one accidental "clear cookies" away from gone.

c. **Online storage.** Syncs across phone and laptop. Needs a free account somewhere and about 5 minutes of setup. Overkill if it's truly just this browser.

_words: 149 · questions: 1 · files changed: 0 _

## Turn 4

**User:** B sounds good, i'd feel better having a backup just in case.

Good call — backups cost almost nothing and save you from one bad "clear history" day.

I have enough to sketch it. Here's how I'd build it, in 4 small steps:

1. **Today-screen with placeholder habits** — you see the look, nothing's saved yet ← we start here
2. **Add and remove habits** — your real list
3. **Save ticks in your browser** — they stick between visits
4. **Backup button** — download your data as a tiny file, and load it back if needed

**Why this way:** each step is something you can open and try before the next one. The visuals come first so we agree on the feel; the saving comes once you know what you're saving.

**Worth knowing:** I'll leave streak counters out, since you said "keep it clean" — easy to add later if you miss them.

Start with step 1?

_words: 146 · questions: 1 · files changed: 0 _

## Turn 5

**User:** yes go

`[tool] Write {"file_path": "<workdir>", "content": "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\" />\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n<title>Habits</title>\n<style>\n  :root {\n    --bg: #f7f5f0;\n    --card: #ffffff;\n    --ink: #22201c;\n    --muted: #8a847a;\n    --ri`

**Step 1 done: the today-screen.**

**Try it:** double-click `index.html` (it should open in your browser). You'll see today's date and three placeholder habits — "Meditate 5 minutes", "Read 10 pages", "Walk outside". Tap a row and the circle fills green and the name gets a soft strikethrough. Reload the page and the ticks reset — that's expected, saving comes in step 3.

**The idea:** right now the whole app is one file. Your browser opens it the same way it opens any webpage, but there's no server behind it — everything happens on your computer. The ticks live only in the page's memory, which is why they vanish on reload.

Next is step 2: **add and remove habits** so the list is yours, not my placeholders. One small choice first — **how do you want to manage your habit list?**

a. **A pencil button at the top** that flips the list into "edit mode": each row gets a delete X, and there's an "Add habit" field at the bottom. Tap pencil again to go back to the clean view. *(my pick — keeps the daily screen clean)*

b. **Always visible.** A small X next to every habit all the time, and an "Add" field always at the bottom. Less tidy but one less tap.

_words: 214 · questions: 1 · files changed: 1 ['index.html']_

## Turn 6

**User:** Go with the pencil button, I like the clean look.

`[tool] Write {"file_path": "<workdir>", "content": "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\" />\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n<title>Habits</title>\n<style>\n  :root {\n    --bg: #f7f5f0;\n    --card: #ffffff;\n    --ink: #22201c;\n    --muted: #8a847a;\n    --ri`

**Step 2 done: edit mode.**

**Try it:** reload the page. There's now a small pencil icon in the top-right corner. Tap it — the ticks disappear, a red-ish ✕ appears next to each habit, and a "New habit..." field slides in at the bottom. Add one, delete one, then tap the pencil again to go back to the clean today-view and tick things normally.

**The idea:** the habit list now lives in a little JavaScript list in the page's memory, not written into the HTML. When you add or remove, that list changes and the page redraws itself from it. That's the shape we need for step 3 — once the data is in one place, saving it is just "write this list to local storage whenever it changes."

Also added, since you'd notice: an empty-state message if you delete everything ("No habits yet. Tap the pencil to add one.") so the screen never feels broken.

Next is step 3: **save your list and today's ticks to the browser so they stick between visits.** One choice first — **when you reopen the page tomorrow, what should today's ticks do?**

a. **Reset to empty.** A new day, a fresh list to tick off. Yesterday's ticks are kept in history for backups and future features. *(my pick — matches "just today")*

b. **Keep showing until you un-tick.** Ticks only clear when you tap them off. Simpler, but you might find yesterday's ticks still green on Tuesday morning.

_words: 245 · questions: 1 · files changed: 1 ['index.html']_

## Turn 7

**User:** a sounds right, fresh start each day makes sense

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  <footer id=\"footer\">Tap a row to tick it. Nothing's saved yet \u2014 that's step 3.</footer>", "new_string": "  <footer id=\"footer\">Tap a row to tick it. Everything's saved automatically.</footer>"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "<script>\n  const state = {\n    habits: [\n      { id: 1, name: \"Meditate 5 minutes\", done: false },\n      { id: 2, name: \"Read 10 pages\", done: false },\n      { id: 3, name: \"Walk outside\", done: false },\n    ],\n    editing: false,\n    nextId: 4,\n`

**Step 3 done: your list and today's ticks are saved.**

**Try it:** reload the page — your habits and today's ticks are still there. Tick one, close the tab, reopen `index.html`: still ticked. Tomorrow when you open it, today's checks will be clear but your habit list stays. (You can test the "tomorrow" bit now by changing your computer's clock a day forward and reloading — a tick box or two will reset.)

**The idea:** your data lives in **local storage** (a small notebook your browser keeps for this page). The page reads it when it opens and writes to it every time you tick, add, or remove. Ticks are stored by date — `{ "2026-10-15": [1, 3] }` — so "today's ticks" is just "the row for today's date." A new day gets a new empty row.

Also added, since you'd notice: if the stored data is ever missing or broken, the app falls back to the three starter habits instead of showing a blank error.

Next is step 4, the last one: **the backup button.** It'll download a tiny file with everything in it, and let you load it back in a bad day.

Ready for step 4?

_words: 200 · questions: 1 · files changed: 1 ['index.html']_

## Turn 8

**User:** yep go for it

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  footer {\n    margin-top: 24px;\n    text-align: center;\n    color: var(--muted);\n    font-size: 13px;\n  }", "new_string": "  footer {\n    margin-top: 24px;\n    text-align: center;\n    color: var(--muted);\n    font-size: 13px;\n  }\n  .foot-actions {\n`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  <footer id=\"footer\">Tap a row to tick it. Everything's saved automatically.</footer>\n</main>", "new_string": "  <footer>\n    <div id=\"footer\">Tap a row to tick it. Everything's saved automatically.</div>\n    <div class=\"foot-actions\">\n      <button `

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  addBtn.addEventListener('click', addHabit);\n  addInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') addHabit(); });\n\n  render();\n</script>", "new_string": "  addBtn.addEventListener('click', addHabit);\n  addInput.addEventListener('keydown'`

**Step 4 done: backup and restore.**

**Try it:** reload the page. Two small links appear under the main message — "Download backup" and "Restore from file". Tap Download — you'll get a file called something like `habits-backup-2026-10-15.json` in your Downloads folder. Open it in a text editor if you're curious; it's human-readable. Then tap Restore, pick that file, say yes to the confirm, and the app reloads the data (no visible change this time, since it's the same data).

**The idea:** the backup file is just a copy of what's in local storage, as plain text. If one day your browser forgets everything, you reopen the page, tap Restore, pick the newest backup you saved, and you're back. I put a confirm dialog on Restore because loading a file *replaces* your current data — if you did it by accident, you'd lose today's ticks.

---

**Done: a clean, self-contained habit tracker.**

**How it works:** one file — `index.html` — opened directly by your browser. Your habit list and daily ticks live in **local storage** (your browser's little notebook for this page). "Today" resets automatically at midnight. Backups are plain JSON files you keep wherever you like.

**Try now:**
- Tap the pencil, add a couple of real habits, delete the placeholders.
- Download a backup — tuck it in a Dropbox/Drive folder for peace of mind.
- Tomorrow: reopen the page, enjoy a fresh row of empty circles.

**Worth understanding later:** your history is being saved every day under `ticks` by date — so if you ever want a weekly grid, streak counters, or stats, the data's already there waiting. Just ask.

Let me quickly update the project map so a future me (or you, in a new chat) can pick up where we left off.

`[tool] Bash {"command": "mkdir -p <workdir>", "description": "Create .vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Write {"file_path": "<workdir>", "content": "# App map\n\n**What it does:** A personal browser-only habit tracker. Shows a clean \"Today\" list with yes/no ticks, resets each day, and saves everything in the browser with a downloadable backup file.\n\n## How it fits together\n\n```\n  index.html  (one file)\n      \u2502\n     `

Map saved to `.vibe/map.md`. Enjoy the tracker — and if you want streaks, a weekly grid, dark mode, or anything else later, just say the word.

_words: 322 · questions: 0 · files changed: 1 ['index.html']_

**User:** DONE

## Metrics

| Turn | Words | Questions | Files changed |
|---|---|---|---|
| 1 | 146 | 1 | 0 |
| 2 | 114 | 1 | 0 |
| 3 | 149 | 1 | 0 |
| 4 | 146 | 1 | 0 |
| 5 | 214 | 1 | 1 |
| 6 | 245 | 1 | 1 |
| 7 | 200 | 1 | 1 |
| 8 | 322 | 0 | 1 |

- Turns: 8
- First file change on turn: 5
- Most files changed in one turn: 1
- Turns asking more than one question: 0
- Turns ending with no question: 1
- Average words per turn: 192
