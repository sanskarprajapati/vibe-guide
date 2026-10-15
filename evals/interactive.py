"""Interactive evals: a simulated non-technical user talks to Claude for several turns.

Usage:
  python evals/interactive.py skill habit-tracker      # current skill
  python evals/interactive.py old habit-tracker        # skill as committed in git HEAD
  python evals/interactive.py baseline habit-tracker   # no skill

Each assistant turn is a real `claude -p` call (continued session). After it, a second
`claude -p` call plays the user from the persona in interactive_scenarios.json and writes
the next message. Per-turn metrics: words, questions asked, project files changed.
Transcripts land in evals/results/interactive/<mode>/<id>.md.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run  # noqa: E402  (reuses fixture prep, turn runner, snapshots)

EVALS = run.EVALS
MODES = ("skill", "old", "baseline")
USER_TIMEOUT_S = 180
DONE_TOKEN = "DONE"

USER_PROMPT = """You are role-playing a user talking to an AI coding assistant. Stay in character.

Who you are: {persona}

Rules:
- Reply with ONE short message (1-3 sentences), in plain words, the way this person would type it.
- If the assistant asked you a question or gave options, answer it. Pick an option that fits who you are; you may have your own opinion.
- If it asked you to open or try something, pretend you did and say briefly what you saw (it looked as described).
- If it asked whether to continue, say yes or go.
- Never write code. Never mention that you are role-playing.
- If the assistant says the whole thing is finished and asks nothing, reply exactly: {done}

The assistant's latest message:
---
{message}
---

Your reply:"""


def load_scenarios():
    return {s["id"]: s for s in json.loads((EVALS / "interactive_scenarios.json").read_text())}


def prepare(scenario, mode):
    if scenario["fixture"] == "empty":
        workdir = Path(tempfile.mkdtemp(prefix="project-"))
    else:
        workdir = run.prepare_workdir({**scenario, "setup": {"remove_profile": True}}, "baseline")
    skills = workdir / ".claude" / "skills" / "vibe"
    if mode == "skill":
        shutil.copytree(run.SKILL_DIR, skills)
    elif mode == "old":
        export_git_skill(skills)
    return workdir


def export_git_skill(dest):
    """Write the vibe/ folder as committed in HEAD, for an old-vs-new comparison."""
    files = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "vibe"],
        cwd=run.ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    for name in files:
        content = subprocess.run(["git", "show", f"HEAD:{name}"], cwd=run.ROOT, capture_output=True, check=True).stdout
        target = dest / Path(name).relative_to("vibe")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


def visible_text(transcript):
    """Assistant prose only: drop tool lines and code blocks."""
    text = "\n".join(line for line in transcript.splitlines() if not line.startswith("`[tool]"))
    return re.sub(r"```.*?```", "", text, flags=re.S)


def count_questions(text):
    """Questions the user is asked to answer: '?' sentences plus lettered/numbered option groups beyond the first."""
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip().endswith("?")]
    option_groups = len(re.findall(r"(?m)^\s*(?:\*\*)?(?:a[.)]|1\.)\s", text))
    return max(len(sentences), option_groups)


def simulate_user(persona, message):
    prompt = USER_PROMPT.format(persona=persona, message=message[-6000:], done=DONE_TOKEN)
    with tempfile.TemporaryDirectory() as empty:
        try:
            result = subprocess.run(
                ["claude", "-p", prompt, "--setting-sources", "project", "--disallowedTools",
                 "Bash Read Write Edit Glob Grep Skill Agent WebFetch WebSearch"],
                cwd=empty, capture_output=True, text=True, timeout=USER_TIMEOUT_S,
            )
            return result.stdout.strip() or "ok"
        except subprocess.TimeoutExpired:
            return "ok"


def run_conversation(scenario, mode):
    workdir = prepare(scenario, mode)
    message = scenario["first_message"]
    lines = [f"# {scenario['id']} ({mode})", "", f"**Persona:** {scenario['persona']}", ""]
    metrics = []
    before = run.snapshot_project(workdir)
    for index in range(scenario["max_turns"]):
        prompt = f"/vibe {message}" if mode != "baseline" and index == 0 else message
        transcript = run.run_turn(workdir, prompt, index)
        after = run.snapshot_project(workdir)
        changed = run.changed_files(before, after)
        before = after
        text = visible_text(transcript)
        row = {"turn": index + 1, "words": len(text.split()), "questions": count_questions(text), "files": len(changed)}
        metrics.append(row)
        lines += [f"## Turn {index + 1}", "", f"**User:** {prompt}", "", transcript, "",
                  f"_words: {row['words']} · questions: {row['questions']} · files changed: {len(changed)} {changed if changed else ''}_", ""]
        message = simulate_user(scenario["persona"], text)
        if message.strip().upper().startswith(DONE_TOKEN):
            lines += [f"**User:** {message}", ""]
            break
    lines += ["## Metrics", "", summarize(metrics), ""]
    out = EVALS / "results" / "interactive" / mode / f"{scenario['id']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    shutil.rmtree(workdir, ignore_errors=True)
    return scenario["id"], mode, metrics


def summarize(metrics):
    if not metrics:
        return "(no turns)"
    first_change = next((m["turn"] for m in metrics if m["files"]), None)
    rows = ["| Turn | Words | Questions | Files changed |", "|---|---|---|---|"]
    rows += [f"| {m['turn']} | {m['words']} | {m['questions']} | {m['files']} |" for m in metrics]
    multi_q = sum(1 for m in metrics if m["questions"] > 1)
    stats = [
        f"- Turns: {len(metrics)}",
        f"- First file change on turn: {first_change}",
        f"- Most files changed in one turn: {max(m['files'] for m in metrics)}",
        f"- Turns asking more than one question: {multi_q}",
        f"- Turns ending with no question: {sum(1 for m in metrics if m['questions'] == 0)}",
        f"- Average words per turn: {sum(m['words'] for m in metrics) // len(metrics)}",
    ]
    return "\n".join(rows + [""] + stats)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in MODES:
        sys.exit(f"usage: python {sys.argv[0]} {{{'|'.join(MODES)}}} <scenario-id> [...]")
    mode, ids = sys.argv[1], sys.argv[2:]
    scenarios = load_scenarios()
    with ThreadPoolExecutor(max_workers=4) as pool:
        for sid, m, metrics in pool.map(lambda i: run_conversation(scenarios[i], mode), ids):
            print(f"done: {sid} ({m}), {len(metrics)} turns", flush=True)


if __name__ == "__main__":
    main()
