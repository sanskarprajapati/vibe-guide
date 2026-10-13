"""Run vibe skill eval scenarios with `claude -p`.

Usage:
  python evals/run.py baseline            # all scenarios, no skill installed
  python evals/run.py skill 03-db-card    # selected scenarios, skill installed

Each run copies a fixture into a scratch dir, applies the scenario setup,
optionally installs the skill as a project skill, then runs every turn.
Transcripts and file diffs land in evals/results/<mode>/<id>.md.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
SKILL_DIR = ROOT / "vibe"
MODES = ("baseline", "skill")
TURN_TIMEOUT_S = 600
PARALLEL = 6
# Broad enough that "waiting for go" is the skill's choice, not a missing permission.
ALLOWED_TOOLS = "Read Write Edit Glob Grep Skill AskUserQuestion Bash(ls *) Bash(cat *) Bash(mkdir *) Bash(python3 *) Bash(python *)"
IGNORED_DIRS = {".vibe", ".claude"}


def load_scenarios():
    return json.loads((EVALS / "scenarios.json").read_text())


def prepare_workdir(scenario, mode):
    # Neutral folder name: the scenario id ("cost-tripwire") would hint at the expected answer.
    workdir = Path(tempfile.mkdtemp(prefix=f"{scenario['fixture']}-"))
    shutil.copytree(EVALS / "fixtures" / scenario["fixture"], workdir, dirs_exist_ok=True)
    setup = scenario.get("setup", {})
    profile = workdir / ".vibe" / "profile.md"
    if setup.get("remove_profile"):
        shutil.rmtree(workdir / ".vibe", ignore_errors=True)
    elif "level" in setup:
        text = re.sub(r"\| Experience \| .* \|", f"| Experience | {setup['level']} |", profile.read_text())
        profile.write_text(text)
    if mode == "skill":
        shutil.copytree(SKILL_DIR, workdir / ".claude" / "skills" / "vibe")
    else:
        # The profile only exists because of the skill; leaving it in leaks context into the baseline.
        shutil.rmtree(workdir / ".vibe", ignore_errors=True)
    return workdir


def build_prompt(turn, index, mode):
    if mode == "skill" and index == 0:
        return f"/vibe {turn}".strip()
    return turn


def summarize_stream(raw):
    """Turn stream-json output into readable text + tool calls."""
    parts = []
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "assistant":
            continue
        for block in event.get("message", {}).get("content", []):
            if block.get("type") == "text" and block["text"].strip():
                parts.append(block["text"].strip())
            elif block.get("type") == "tool_use":
                args = json.dumps(block.get("input", {}))[:400]
                parts.append(f"`[tool] {block['name']} {args}`")
    return "\n\n".join(parts)


def run_turn(workdir, prompt, index):
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json", "--verbose",
        "--setting-sources", "project",
        "--permission-mode", "acceptEdits",
        "--allowedTools", ALLOWED_TOOLS,
    ]
    if index > 0:
        cmd.append("--continue")
    try:
        result = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=TURN_TIMEOUT_S)
        return summarize_stream(result.stdout) or f"(no output) stderr: {result.stderr[-1000:]}"
    except subprocess.TimeoutExpired:
        return "(timed out)"


def diff_against_fixture(scenario, workdir):
    result = subprocess.run(
        ["diff", "-ruN", "-x", ".claude", str(EVALS / "fixtures" / scenario["fixture"]), str(workdir)],
        capture_output=True, text=True,
    )
    return result.stdout[:8000] or "(no file changes)"


def snapshot_project(workdir):
    """Hash every project file, ignoring the skill's own notes and install dir."""
    snap = {}
    for path in workdir.rglob("*"):
        rel = path.relative_to(workdir)
        if path.is_file() and not (set(rel.parts) & IGNORED_DIRS):
            snap[str(rel)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snap


def changed_files(before, after):
    return sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))


def auto_checks(scenario, changes_per_turn):
    """Compare per-turn project changes with the scenario's expectations."""
    results = []
    for index in scenario.get("expect_no_changes", []) + scenario.get("expect_no_new_changes", []):
        changed = changes_per_turn[index]
        results.append((f"turn {index + 1}: no project files changed", not changed, changed))
    for index in scenario.get("expect_changes", []):
        changed = changes_per_turn[index]
        results.append((f"turn {index + 1}: project files changed", bool(changed), changed))
    return results


def run_scenario(scenario, mode):
    workdir = prepare_workdir(scenario, mode)
    lines = [f"# {scenario['id']} ({mode})", "", f"**Pass if:** {scenario['pass']}", ""]
    changes_per_turn = []
    before = snapshot_project(workdir)
    for index, turn in enumerate(scenario["turns"]):
        prompt = build_prompt(turn, index, mode)
        lines += [f"## Turn {index + 1}: `{prompt or '(empty)'}`", "", run_turn(workdir, prompt, index), ""]
        after = snapshot_project(workdir)
        changed = changed_files(before, after)
        changes_per_turn.append(changed)
        lines += [f"_Project files changed this turn: {', '.join(changed) or 'none'}_", ""]
        before = after
    checks = auto_checks(scenario, changes_per_turn)
    lines += ["## Auto-checks", ""] + [
        f"- {'PASS' if ok else 'FAIL'}: {name}" + (f" ({', '.join(files)})" if files else "")
        for name, ok, files in checks
    ] + [f"- .vibe/map.md exists: {(workdir / '.vibe' / 'map.md').exists()}", ""]
    lines += ["## File changes", "", "```diff", diff_against_fixture(scenario, workdir), "```"]
    out = EVALS / "results" / mode / f"{scenario['id']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    shutil.rmtree(workdir, ignore_errors=True)
    return scenario["id"]


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        sys.exit(f"usage: python {sys.argv[0]} {{{'|'.join(MODES)}}} [scenario-id ...]")
    mode, wanted = sys.argv[1], set(sys.argv[2:])
    scenarios = [
        s for s in load_scenarios()
        if (not wanted or s["id"] in wanted) and not (mode == "baseline" and s.get("skill_only"))
    ]
    if mode == "skill" and not (SKILL_DIR / "SKILL.md").exists():
        sys.exit("vibe/SKILL.md not found; write the skill first")
    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        for done in pool.map(lambda s: run_scenario(s, mode), scenarios):
            print(f"done: {done}", flush=True)


if __name__ == "__main__":
    os.environ.pop("CLAUDECODE", None)
    main()
