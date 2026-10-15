# voice-notes (skill)

**Persona:** You're a freelance designer who records voice memos on your phone after client calls. You're not technical. You want them turned into written notes you can read. You're careful with money and have heard AI APIs can get expensive. You don't want to share any passwords or keys with the AI. Short messages.

## Turn 1

**User:** /vibe make me a tool that turns my voice memos into tidy written notes

`[tool] Bash {"command": "ls -la <workdir> 2>&1 && echo \"---VIBE---\" && ls -la <workdir> 2>&1", "description": "Check project folder and .vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

Empty folder, fresh start. Before I plan anything, I need to know how you'd actually use this tool day-to-day — that shapes everything else.

`[tool] AskUserQuestion {"questions": [{"question": "How do you want to get your voice memos into this tool?", "header": "How to feed it", "multiSelect": false, "options": [{"label": "Drop files on a webpage", "description": "A simple page on your computer (or online) where you drag audio files in and get notes back. Works with any recording \u2014 Apple Voice Memos, Google Recorder, phone calls you've exported. My pick `

Empty folder, fresh start. Before I plan anything, I want to know how you'd actually use this day-to-day — that shapes everything else.

**How do you want to get your voice memos into this tool?**

a. **Drop files on a webpage.** A simple page where you drag audio files in and get notes back. Works with any recording — Apple Voice Memos, phone, anything you can export. *(my pick if you record on your phone and want to send a few at a time)*

b. **A folder on your Mac.** Drop audio into a watched folder and notes appear next to them automatically. Nice if you record a lot and want it hands-off, but it only works on this one computer.

c. **Paste a link.** You give it a link to an audio file (iCloud, Dropbox) and get notes back. Good if your memos already live in the cloud.

_words: 173 · questions: 1 · files changed: 0 _

## Turn 2

**User:** a sounds good. how much is this gonna cost me to run though? i've heard these ai things add up fast

Good instinct to ask up front. Honest answer: it depends which **transcription** (turning speech into text — that's the pricey bit) option we use. The "tidy it up" step costs pennies either way.

Rough costs for turning speech into text:

a. **Free, runs on your Mac.** Uses a model called Whisper that lives on your computer. $0 forever. Downside: slower (a few minutes to process a long memo), and takes a one-time install. *(my pick for keeping it cheap and private)*

b. **Pay-as-you-go cloud service.** About **$0.006 per minute** of audio — so an hour of memos = ~$0.36, a whole month of daily 10-min memos = **~$2**. Fast, no install, but needs a paid account (OpenAI or similar) with your card on file.

Which fits you better — free-but-slower, or a couple dollars a month for speed?

_words: 138 · questions: 1 · files changed: 0 _

## Turn 3

**User:** Free one please, I don't want another account with my card on it.

Good call — fully local then. Whisper will do all the audio work on your Mac, nothing leaves the computer.

Next thing shapes what you see: **what should "tidy notes" actually look like?**

a. **Clean paragraphs.** Just the transcript with the "um"s, repetitions and false starts cleaned up. Good if your memos are already pretty coherent and you mostly want them readable.

b. **Bullet points.** Key points pulled out as a list, no fluff. Good if memos ramble and you want the gist.

c. **Structured notes.** A short summary at the top, bullet points in the middle, any "to-do" items pulled out at the bottom. *(my pick — most useful across different kinds of memos)*

d. **Something else** — describe how you'd like them laid out.

Heads-up: (b) and (c) need a bit of extra brainpower that Whisper alone doesn't have, so I'll ask you one more small question after this about a free thing to install. (a) can be done with Whisper only.

_words: 164 · questions: 1 · files changed: 0 _

## Turn 4

**User:** c sounds perfect, that's what i want

Structured notes it is — summary, bullets, to-dos.

For the brainpower that writes the summary and pulls out to-dos, we need a small **AI model** (a program that understands text) running on your Mac. The free, no-account way is **Ollama** — a free app that lets your Mac run AI models offline. One install, no sign-up, no card.

a. **Install Ollama.** Takes about 5 minutes. Free forever, works offline, nothing leaves your Mac. Works best on an Apple Silicon Mac (M1/M2/M3/M4). On an older Intel Mac it still works but is slow. *(my pick)*

b. **Skip the smart stuff for now.** I'll build it with just Whisper and show you clean paragraphs; we can add Ollama later if you want the summary + to-do format.

Quick check so I know which: **is your Mac Apple Silicon (M1/M2/M3/M4) or an older Intel one?** And are you up for installing Ollama?

_words: 149 · questions: 1 · files changed: 0 _

## Turn 5

**User:** it's an M2 air. yeah ollama sounds good if it's really free and stays on my mac. let's do it.

M2 Air is plenty — this'll fly on your machine.

Here's how I'd build it, in 4 small steps:

1. **The webpage** — drag an audio file, see a placeholder "got it" message  ← we start here
2. **Transcription working** — Whisper turns the audio into raw text, shown on the page
3. **Tidy notes** — Ollama rewrites the raw text as summary + bullets + to-dos
4. **Save & polish** — a Copy button and auto-save to a notes folder

**Why this way:** every step gives you something you can try before we move on. The page sits on your Mac and talks to Whisper and Ollama locally, so nothing leaves your computer.

**Worth knowing:**
- To let the webpage talk to Whisper/Ollama, I'll run a tiny **helper program** (a small program that sits in the background and takes orders from the page). You start it with one command in Terminal; closing it stops the tool.
- First time you use Whisper and Ollama, each downloads a model file (a few hundred MB). After that, they work offline.

Start with step 1?

_words: 183 · questions: 1 · files changed: 0 _

## Turn 6

**User:** yeah let's go

Building the webpage now.

`[tool] Bash {"command": "mkdir -p <workdir>", "description": "Create .vibe directory"}`

`[tool] Write {"file_path": "<workdir>", "content": "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <title>Voice memo \u2192 tidy notes</title>\n  <style>\n    :root {\n      --bg: #fafaf7;\n      --ink: #1a1a1a;\n      --muted: #6b6b6`

`[tool] Write {"file_path": "<workdir>", "content": "# Profile\n\n- Level: new to coding. Non-technical.\n- Pace: step (one step per turn).\n- Mac: Apple Silicon M2 Air.\n- Values: free tools, no new accounts, no card on file, data stays on the Mac.\n- Current project: voice-memo-to-tidy-notes tool.\n  - Interface: drag-and-drop we`

`[tool] Write {"file_path": "<workdir>", "content": "# Known terms (already explained \u2014 don't re-explain)\n\n- transcription \u2014 turning speech into text\n- AI model \u2014 a program that understands text\n- Whisper \u2014 a model that lives on your computer for transcription\n- Ollama \u2014 a free app that lets your M`

**Step 1 done: the webpage.**

**Try it:** double-click `index.html` in Finder (or open the file in your browser). You'll see a clean page with a drop zone. Drag any audio file onto it — or click the "pick one" link — and it'll show the filename, size, and a green "Got it" message. Nothing is actually processed yet, that's step 2.

**The idea:** right now this is a plain **webpage** (an HTML file on your Mac). It runs entirely in your browser — no internet, no server. The drop zone just reads the file into memory and shows its name. In step 2, when you drop a file, the page will hand it off to Whisper on your Mac and wait for the transcript.

Next is step 2: **install Whisper + wire it in so dropping an audio file shows you the raw transcript**. Ready?

_words: 149 · questions: 1 · files changed: 1 ['index.html']_

## Turn 7

**User:** tried it, drop zone works, filename shows up fine. go ahead with step 2.

Building step 2 now. This step adds a tiny helper program on your Mac and installs Whisper, so a dropped file actually comes back as text.

`[tool] Write {"file_path": "<workdir>", "content": "#!/bin/bash\n# One-time setup. Run with: bash setup.sh\nset -e\n\ncd \"$(dirname \"$0\")\"\n\necho \"\u2192 Checking Homebrew (the Mac tool that installs other tools)...\"\nif ! command -v brew >/dev/null 2>&1; then\n  echo \"   Homebrew not found. Installing (this will ask for your pass`

`[tool] Write {"file_path": "<workdir>", "content": "\"\"\"\nHelper program: serves the webpage and runs Whisper on dropped audio.\nStart with:  python3 server.py\nThen open:   http://localhost:5555\n\"\"\"\nimport http.server\nimport json\nimport os\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\nimport tempfile\n\nHERE = `

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    .status {\n      background: var(--accent-soft);\n      color: var(--accent);\n      padding: 10px 12px;\n      border-radius: 8px;\n      font-size: 14px;\n    }", "new_string": "    .status {\n      background: var(--accent-soft);\n      color: var(--acce`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    <div class=\"result\" id=\"result\">\n      <p class=\"filename\" id=\"filename\"></p>\n      <p class=\"meta\" id=\"meta\"></p>\n      <div class=\"status\">Got it. Transcription comes in step 2.</div>\n    </div>", "new_string": "    <div class=\"result\"`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    const drop = document.getElementById('drop');\n    const fileInput = document.getElementById('file');\n    const result = document.getElementById('result');\n    const filenameEl = document.getElementById('filename');\n    const metaEl = document.getElement`

`[tool] Bash {"command": "chmod +x <workdir>", "description": "Make setup.sh executable"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "- helper program \u2014 a small program that sits in the background and takes orders from the page", "new_string": "- helper program \u2014 a small program that sits in the background and takes orders from the page\n- Homebrew \u2014 the Mac tool that`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "- helper program \u2014 a small program that sits in the background and takes orders from the page", "new_string": "- helper program \u2014 a small program that sits in the background and takes orders from the page\n- Homebrew \u2014 the Mac tool that`

**Step 2 done: Whisper wired in.**

**Try it** (first time takes ~5 min of installing — mostly waiting; after that it's seconds):

1. Open **Terminal** (Cmd+Space, type "terminal", Enter).
2. Move into the project folder — type `cd ` (with the space), then drag the project folder from Finder onto the Terminal window, hit Enter.
3. Run: `bash setup.sh` — this installs Homebrew (if needed), Whisper, and ffmpeg, then downloads the Whisper model (~466 MB, one time). It will ask for your Mac password at least once.
4. When it finishes, run: `python3 server.py`
5. Open **http://localhost:5555** in your browser. Drop any voice memo. You should see "Transcribing…" for a few seconds, then the raw transcript appears.

**The idea:** the page now talks to the helper on your Mac over a local-only address (`localhost` = your own computer; nothing goes to the internet). The helper converts the audio to the format Whisper expects, runs Whisper, and sends back the text.

**I added one thing without asking:** I made Whisper look for its model inside a `models/` folder in the project (not in your home folder), so if you ever delete the project everything goes with it.

**Worth knowing:** processing takes roughly a quarter of the audio length on your M2 (e.g. a 4-minute memo → ~1 minute). The server only listens on your own machine, not the wider internet.

Give it a go — tell me if `setup.sh` finishes cleanly and if a dropped memo returns a transcript. Then we move to step 3: tidy structured notes.

_words: 283 · questions: 1 · files changed: 3 ['index.html', 'server.py', 'setup.sh']_

## Turn 8

**User:** Ok did it, setup ran fine after a while and I dropped a memo in — got the transcript back. Go.

Building step 3 now — adds Ollama so the raw transcript becomes a tidy structured note.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "echo \"\u2192 Installing Whisper + ffmpeg (handles audio) + Python...\"\nbrew install whisper-cpp ffmpeg python", "new_string": "echo \"\u2192 Installing Whisper + ffmpeg (handles audio) + Python + Ollama...\"\nbrew install whisper-cpp ffmpeg python ollama\n\nech`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "import http.server\nimport json\nimport os\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\nimport tempfile\n\nHERE = pathlib.Path(__file__).parent.resolve()\nMODEL = HERE / \"models\" / \"ggml-small.en.bin\"\nPORT = 5555", "new_string": "import ht`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "def transcribe(audio_bytes: bytes, suffix: str) -> str:", "new_string": "def tidy_notes(transcript: str) -> str:\n    payload = json.dumps({\n        \"model\": OLLAMA_MODEL,\n        \"messages\": [\n            {\"role\": \"system\", \"content\": TIDY_SYSTEM_P`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "        try:\n            text = transcribe(audio_bytes, suffix)\n            self._send_json(200, {\"transcript\": text})\n        except subprocess.CalledProcessError as e:\n            err = (e.stderr or b\"\").decode(errors=\"replace\")[-800:]\n            s`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    .transcript {\n      margin-top: 14px;\n      padding: 14px 16px;\n      background: #f3f1ea;\n      border-radius: 8px;\n      font-size: 15px;\n      line-height: 1.5;\n      white-space: pre-wrap;\n      max-height: 360px;\n      overflow-y: auto;\n    }`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    <div class=\"result\" id=\"result\">\n      <p class=\"filename\" id=\"filename\"></p>\n      <p class=\"meta\" id=\"meta\"></p>\n      <div class=\"status\" id=\"status\"></div>\n      <div class=\"transcript\" id=\"transcript\" style=\"display:none\"></di`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    const drop = document.getElementById('drop');\n    const fileInput = document.getElementById('file');\n    const result = document.getElementById('result');\n    const filenameEl = document.getElementById('filename');\n    const metaEl = document.getElement`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    async function handleFile(file) {\n      if (!file) return;\n      filenameEl.textContent = file.name;\n      metaEl.textContent = humanSize(file.size) + ' \u00b7 ' + (file.type || 'audio');\n      result.classList.add('show');\n      transcriptEl.style.dis`

**Step 3 done: tidy notes.**

**Try it:**

1. In Terminal, stop the server if it's running (press **Ctrl+C** in that window).
2. Run `bash setup.sh` again — it'll skip what's already installed, add Ollama, and download the writing model (~2 GB, one time).
3. Start the server: `python3 server.py`
4. Reload **http://localhost:5555** and drop a voice memo.

You should now see a tidy card with **Summary**, **Key points**, and **To-dos** sections. The raw transcript is tucked under a "Show raw transcript" toggle underneath.

**The idea:** your transcript now takes a second trip through **Ollama**. The helper sends the raw text along with a short instruction ("rewrite this as summary + bullets + to-dos") and Ollama's **llama3.2:3b** (a small, fast open model that fits on your Mac) sends back the tidy version. It'll be slightly slower than step 2 — maybe 5–15 extra seconds while the model thinks.

**Worth knowing:**
- Ollama now runs quietly in the background on your Mac via Homebrew Services (so it's ready whenever you open the page). To stop it later: `brew services stop ollama`.
- Small local models can occasionally miss a nuance or over-trim. If a particular memo comes out off, drop it again — results vary slightly each time.

Give it a go. Next is step 4: **Copy button + auto-save notes to a folder on your Mac** so you can keep them. Ready, or anything to tweak about how the notes look first?

_words: 257 · questions: 1 · files changed: 3 ['index.html', 'server.py', 'setup.sh']_

## Metrics

| Turn | Words | Questions | Files changed |
|---|---|---|---|
| 1 | 173 | 1 | 0 |
| 2 | 138 | 1 | 0 |
| 3 | 164 | 1 | 0 |
| 4 | 149 | 1 | 0 |
| 5 | 183 | 1 | 0 |
| 6 | 149 | 1 | 1 |
| 7 | 283 | 1 | 3 |
| 8 | 257 | 1 | 3 |

- Turns: 8
- First file change on turn: 6
- Most files changed in one turn: 3
- Turns asking more than one question: 0
- Turns ending with no question: 0
- Average words per turn: 187
