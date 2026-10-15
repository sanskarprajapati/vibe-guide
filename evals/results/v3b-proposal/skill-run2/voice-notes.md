# voice-notes (skill)

**Persona:** You're a freelance designer who records voice memos on your phone after client calls. You're not technical. You want them turned into written notes you can read. You're careful with money and have heard AI APIs can get expensive. You don't want to share any passwords or keys with the AI. Short messages.

## Turn 1

**User:** /vibe make me a tool that turns my voice memos into tidy written notes

`[tool] Bash {"command": "ls -la <workdir> 2>/dev/null && echo \"---\" && ls -la <workdir> 2>/dev/null", "description": "Check project folder and vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

Love this one — a voice-memos-to-notes tool is a thing you'll use every week once it works.

Nothing in the folder yet, so I'm starting fresh. I'll assume it's just for you, runs on your Mac, no logins, $0 budget — tell me if that's wrong.

First thing that shapes everything else: **what does "tidy" mean to you?** The same recording can become very different notes depending on this.

`[tool] AskUserQuestion {"questions": [{"question": "What should the finished notes look like when the tool is done with a voice memo?", "header": "Note shape", "multiSelect": false, "options": [{"label": "Structured notes", "description": "Headings, key points as bullets, and an \"Action items\" list at the bottom. Looks like meeting notes. Good if you ramble through topics. (my pick)"}, {"label": "Clean transcript", "d`

What should your tidy notes actually look like? Pick the one that sounds right:

a. **Structured notes** — headings, bullets, and an "Action items" list at the bottom. Reads like meeting notes. Good if you ramble between topics. *(my pick)*
b. **Clean transcript** — everything you said, with ums removed and punctuation added. Nothing summarised, nothing lost.
c. **Short summary** — a paragraph or a handful of bullets. Fast to scan; details disappear.
d. **All three in one file** — summary and action items on top, full clean transcript below. More to read, but you never lose anything.

_words: 167 · questions: 1 · files changed: 0 _

## Turn 2

**User:** a sounds right, structured notes with action items at the bottom. that's basically what i need after a client call.

Structured notes with action items — perfect for client calls. Those usually need names, decisions, next steps, and dates captured cleanly.

Next decision: **how do you want to actually use it?** This shapes whether we build a page, a folder, or a command.

a. **A small webpage on your Mac** — open it, drag your voice memo in, click a button, notes appear. Copy them or save as a file. No Terminal, no setup once built. *(my pick for v1 — simplest to try, we can add the folder trick later)*
b. **A watched folder** — drop a voice memo into a special folder, a note file appears next to it a minute later. Lovely once set up, but needs a small helper running in the background on your Mac.
c. **A single Terminal command** — type `notes my-memo.m4a` and the notes print out. Fastest to build, but you live in Terminal.

_words: 152 · questions: 1 · files changed: 0 _

## Turn 3

**User:** webpage sounds good, let's start there. one thing tho - how much is this gonna cost me per memo? i keep hearing ai stuff gets pricey

Good question to raise early — here are the real numbers.

The tool has two jobs: **transcribe** (audio → words) and **tidy up** (words → structured notes). Both cost pennies.

- A **30-minute call**: roughly **20¢** total via cloud services.
- A **1-hour call**: roughly **40¢**.
- You pay as you go, so if you only do a couple of client calls a week, you're looking at **$1–$3 a month**, tops.

So "AI stuff gets pricey" is mostly true for people running it constantly or on huge files — for your use, this is coffee-change.

But there's a bigger question than cost: **client calls can be sensitive**. The two paths differ there.

a. **Cloud (OpenAI + Claude)** — ~20¢ per 30-min memo. Audio briefly travels to US servers, then is deleted after 30 days. They promise not to train on API data. Fast (a 30-min memo takes ~1 min to process). You'll need to make a free OpenAI account and paste an API key (a password-like string) into a settings file — I'll never see it. *(my pick if your calls aren't under NDA)*
b. **Local on your Mac** — **free forever**, audio never leaves your laptop. Slower: a 30-min memo takes ~5 min to process on an M-series Mac. Needs a one-time install of a transcription model (~1GB download), which I'll walk you through. *(my pick if calls are confidential)*

Which fits your calls better?

_words: 236 · questions: 1 · files changed: 0 _

## Turn 4

**User:** local please, some clients get weird about that stuff

Smart call. Local means audio, transcript, and notes all stay on your Mac — nothing to explain to a nervous client.

**How it'll work when done:**
1. You open a small page in your browser (one bookmark, one click).
2. Drop your voice memo into a box, type the client's name, click "Make notes."
3. A progress bar shows "transcribing..." then "tidying up..."
4. Your notes appear — **Summary**, **Decisions**, **Action items**, **Full details** — ready to copy or save.

**What's in front, what's behind:**
- **What you see** (front end): a single page that opens in Safari or Chrome.
- **Behind the scenes** (back end): a small program running on your Mac that uses **Whisper.cpp** (a free, open-source tool that turns speech into text locally) and **Ollama** (a free app that runs small AI models directly on your Mac — think "ChatGPT, but on your laptop"). Nothing leaves the machine.

**Features I'd suggest** (pick any, or none):
- **Client name + date header**: you type the client's name before processing, so each note gets a proper title and files itself by date. *(I'd do this first)*
- **Notes archive**: every finished note auto-saves to a `~/Client Notes/` folder, so you can scroll back through old calls.
- **Promise-catcher**: pulls out things *you* said you'd do ("I'll send that over by Friday") into their own section — easy to miss when you listen back.

Which of these do you want? (You can say "all three" or pick a couple.)

_words: 249 · questions: 1 · files changed: 0 _

## Turn 5

**User:** All three sound good. The promise-catcher is actually the main thing I need, I always forget what I said I'd do.

Promise-catcher as the hero feature — got it. The prompt will be tuned to specifically hunt for anything *you* said you'd do, so it doesn't get lost.

Here's how I'd build it, in **5 small steps**:

1. **The webpage shell** — a drop zone, a client name box, and a "Make notes" button that doesn't do anything yet. You'll see the shape and tell me if it looks right. ← *we start here*
2. **Whisper on your Mac** — one-time install, then we test transcription on one of your real voice memos in Terminal (not wired to the page yet).
3. **Wire the page to Whisper** — drop a file, click the button, watch the transcript appear live.
4. **Ollama + the structuring prompt** — install the local AI, tune a prompt specifically for client-call notes with the promise-catcher.
5. **Full pipeline + auto-save** — wire structuring into the page, save each finished note to `~/Client Notes/<date> — <client>.md`.

**Why this way:** each step is independently testable, so if the transcript is off or the notes feel wrong, we fix *just that piece* without unpicking everything.

**Worth knowing:** steps 2 and 4 need Terminal and roughly 5GB of one-time downloads — I'll hand you one copy-paste at a time. Also, if your Mac has 8GB of RAM (the base model), the structuring step will be noticeably slower; tell me when we get there and I'll pick a lighter AI model.

Start with step 1?

_words: 244 · questions: 1 · files changed: 0 _

## Turn 6

**User:** yeah go for it. mine's a macbook air with 16gb so should be ok.

Building step 1. One file, no setup — you'll be able to open it immediately.

`[tool] Write {"file_path": "<workdir>", "content": "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n  <title>Client call notes</title>\n  <style>\n    :root {\n      --ink: #1b1b1b;\n      --muted: #6b6b6b;\n      --line: #e6e3dd;\n `

**Step 1 done: the webpage shell.**

**Try it:** paste this into Terminal to open it:

```
open <workdir>
```

You'll see a page where you can type a client name, pick a date, drop a voice memo in, and click **Make notes** — the button is a stub right now (it just prints "no backend yet"), which is on purpose for this step.

**The idea:** we built just the **front end** first — the part you see — so you can tell me if the shape is right before any processing is wired up. If something looks off (wrong wording, missing field, needs a notes field for your own thoughts), say so now and I'll adjust before step 2.

**Next is step 2: installing Whisper on your Mac** so it can turn an audio file into text. That involves one Terminal command (`brew install whisper-cpp`) and one small model download (~150MB). Does the page look right to you, and are you ready for step 2?

`[tool] Write {"file_path": "<workdir>", "content": "# Project profile\n\n- **Users:** just the user (personal tool).\n- **Runs:** locally on their Mac (MacBook Air, 16GB RAM).\n- **Stage:** personal / productivity tool for client-call notes.\n- **Data:** voice memos from client calls \u2014 potentially sensitive / NDA-covered.\n- `

_words: 176 · questions: 1 · files changed: 1 ['index.html']_

## Turn 7

**User:** Page looks good, that's basically what I need. Yeah go ahead with step 2.

**Step 2: Whisper on your Mac.**

Open Terminal (Cmd+Space, type "Terminal", Enter) and paste these one at a time. Short "what it does" is above each.

**1. Move into the project folder** (so later commands land in the right place):
```
cd <workdir>
```

**2. Install Homebrew** — the standard tool for installing other Mac Terminal tools. Skip this if `which brew` already prints a path. On a fresh Mac this takes 5–10 min and asks for your password:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**3. Install Whisper and ffmpeg** (ffmpeg converts audio formats — Whisper needs a specific one):
```
brew install whisper-cpp ffmpeg
```

**4. Download the English Whisper model** (~142MB, one time):
```
mkdir -p models && curl -L -o models/ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

**The idea:** Whisper is the AI that turns speech into text. These three things live together: Homebrew installs stuff, Whisper does the transcribing, the model file is Whisper's "brain" for English.

Let me know when all four finish — or paste any error you hit, and I'll help debug. Then I'll give you the test command to try it on a real voice memo.

_words: 163 · questions: 1 · files changed: 0 _

## Turn 8

**User:** ok hold on this is a lot. the install part is fine but how much does this cost to run? i thought i had to pay for the AI part

Zero cost to run. Nothing to pay, no API key, no subscription.

The 20¢-per-memo figure was for the **cloud** option — you chose **local**, which is a different trade entirely. Whisper and Ollama are free, open-source programs that live on your Mac and do all the work there. The only things you're "paying" with are:

- **Disk space**: ~5GB total once everything is installed (the two models are the bulk of it).
- **A bit of CPU** while a memo is processing — like watching a YouTube video. Fan might spin for a minute or two.

No bill ever arrives. That's exactly why I pushed for local given your "clients get weird" line — the privacy and the price are the same win.

Keep going with the install when you're ready, or ask anything else first.

_words: 136 · questions: 0 · files changed: 0 _

## Metrics

| Turn | Words | Questions | Files changed | Proposal |
|---|---|---|---|---|
| 1 | 167 | 1 | 0 |  |
| 2 | 152 | 1 | 0 |  |
| 3 | 236 | 1 | 0 |  |
| 4 | 249 | 1 | 0 | yes |
| 5 | 244 | 1 | 0 |  |
| 6 | 176 | 1 | 1 |  |
| 7 | 163 | 1 | 0 |  |
| 8 | 136 | 0 | 0 |  |

- Turns: 8
- First file change on turn: 6
- Most files changed in one turn: 1
- Proposal (how it works, front/back, suggested features) on turn: 4 (before first code change)
- Turns asking more than one question: 0
- Turns ending with no question: 1
- Average words per turn: 190
