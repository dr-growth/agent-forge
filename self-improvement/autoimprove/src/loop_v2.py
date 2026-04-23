"""
autoimprove v2 orchestrator.

Differences from v1 loop:
  - Applies a behavioral gate on deterministic assertions over output.
    Iterations whose behavioral_pass_rate drops below
    V2_BEHAVIORAL_GATE_THRESHOLD are rejected regardless of prose score.
  - Uses the three-signal evaluator (evaluate_v2): behavioral + Opus rubric
    against Anthropic's building-skills doc + v1 prose score.
  - Propose prompt is fed failing behavioral assertions as primary signal.
  - Commit rule is gate-aware (see decide_action below).

Known scope limit (tracked as v2.1 follow-up):
  True filesystem sandbox execution (where the skill actually creates files
  we can stat) requires extending runner.py to accept a workdir. Until that
  ships, behavioral checks run against the text output only. The assertion
  library is already shaped to support filesystem checks — they just
  activate when `sandbox_root` is populated, which is None for now.
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import anthropic

from .config import (
    get_api_key,
    PROJECT_ROOT,
    TEST_CASES_DIR,
    DIRECTIVES_DIR,
    RESULTS_DIR,
    SKILL_TYPES,
    V2_BEHAVIORAL_GATE_THRESHOLD,
    V2_COST_CAP_PER_RUN,
)
from .evaluate_v2 import evaluate_v2
from .propose_v2 import propose_modification_v2, estimate_propose_cost
from .runner import TestCase, run_skill
from .zones import (
    ZoneViolation,
    assert_source_readable,
    assert_writable,
    zone_of,
)


V2_EXPERIMENTS_LOG = RESULTS_DIR / "experiments_v2.jsonl"
WORK_DIR = PROJECT_ROOT / "work"

# v2 test cases contain extra fields beyond the v1 TestCase dataclass.
# Extract the v1-shaped subset when invoking the runner.
V1_TESTCASE_FIELDS = {"name", "input_prompt", "ground_truth", "schema"}


# ---------------------------------------------------------------------------
# Test case + directive loading
# ---------------------------------------------------------------------------

def load_v2_test_cases(skill_name: str) -> list[dict]:
    """Load all v2 test cases for a skill as raw dicts (preserving v2 fields)."""
    test_dir = TEST_CASES_DIR / f"{skill_name}-v2"
    if not test_dir.exists():
        raise FileNotFoundError(
            f"v2 test cases missing at {test_dir}. "
            f"Create {skill_name}-v2/ directory with scenario JSON files first."
        )
    return [
        json.loads(p.read_text())
        for p in sorted(test_dir.glob("*.json"))
    ]


def to_v1_testcase(v2_case: dict) -> TestCase:
    """Slice a v2 case dict down to the v1 TestCase signature."""
    return TestCase(**{k: v for k, v in v2_case.items() if k in V1_TESTCASE_FIELDS})


def load_directive(skill_name: str) -> str:
    """Load the v2 improvement directive for a skill, falling back to v1 then default."""
    for candidate in (f"{skill_name}-v2.md", f"{skill_name}.md"):
        path = DIRECTIVES_DIR / candidate
        if path.exists():
            return path.read_text()
    return (
        "Improve the skill file against Anthropic's building-skills rubric "
        "while keeping behavioral assertions passing."
    )


# ---------------------------------------------------------------------------
# Work copy + git helpers (skill source lives at ~/.claude/skills/{name}/SKILL.md;
# the modification loop operates on a git-tracked copy inside this repo)
# ---------------------------------------------------------------------------

def skill_source_path(skill_name: str) -> Path:
    return Path.home() / ".claude" / "skills" / skill_name / "SKILL.md"


def work_copy_path(skill_name: str) -> Path:
    return WORK_DIR / f"{skill_name}-v2.md"


def setup_work_copy_v2(skill_name: str) -> Path:
    """Copy the current skill file into the v2 work directory.

    Zone checks:
      - source must pass assert_source_readable (rejects red-zone source paths)
      - destination must be GREEN (enforced by assert_writable)
    """
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    source = skill_source_path(skill_name)
    if not source.exists():
        raise FileNotFoundError(f"skill source missing: {source}")
    assert_source_readable(source)
    dest = work_copy_path(skill_name)
    assert_writable(dest, reason="initial work copy")
    shutil.copy2(source, dest)
    return dest


def git(cmd: str) -> str:
    result = subprocess.run(
        ["git"] + cmd.split(),
        capture_output=True, text=True, cwd=PROJECT_ROOT,
    )
    return result.stdout.strip()


def git_commit(file_path: Path, message: str) -> str:
    subprocess.run(["git", "add", str(file_path)], cwd=PROJECT_ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=PROJECT_ROOT, capture_output=True, check=True,
    )
    return git("rev-parse --short HEAD")


def setup_branch_v2(skill_name: str) -> str:
    tag = datetime.now().strftime("%Y%m%d")
    branch = f"autoimprove/v2-{skill_name}-{tag}"
    existing = git(f"branch --list {branch}")
    if existing:
        git(f"checkout {branch}")
    else:
        git(f"checkout -b {branch}")
    return branch


# ---------------------------------------------------------------------------
# Scoring (single iteration)
# ---------------------------------------------------------------------------

def run_iteration(
    skill_name: str,
    iteration: int,
    skill_path_override: Path | None = None,
) -> dict:
    """
    Execute all v2 test cases for a skill once, aggregate results.
    If `skill_path_override` is provided, runner uses that copy instead of
    the ~/.claude/ source — this is how the propose loop tests modifications
    without touching the live skill file.
    """
    skill_path = skill_path_override or skill_source_path(skill_name)
    if not skill_path.exists():
        raise FileNotFoundError(f"skill not found: {skill_path}")

    skill_content = skill_path.read_text()
    skill_type = SKILL_TYPES.get(skill_name, "execution")
    v2_cases = load_v2_test_cases(skill_name)

    per_case_results = []
    total_pass_rate = 0.0
    total_rubric = 0.0
    total_prose = 0.0
    total_composite = 0.0
    total_cost = 0.0
    any_gate_failed = False

    for v2_case in v2_cases:
        v1_case = to_v1_testcase(v2_case)
        run_result = run_skill(
            skill_name=skill_name,
            test_case=v1_case,
            skill_path=skill_path,
        )
        total_cost += run_result.cost_usd

        eval_result = evaluate_v2(
            output=run_result.output,
            test_case=v2_case,
            skill_content=skill_content,
            sandbox_root=None,  # v2.1
            skill_type=skill_type,
        )
        per_case_results.append({
            "case": v2_case["name"],
            "runner_cost_usd": run_result.cost_usd,
            "runner_tokens_in": run_result.tokens_in,
            "runner_tokens_out": run_result.tokens_out,
            "output_excerpt": run_result.output[:2000],
            "output_full_length": len(run_result.output),
            "eval": eval_result.to_dict(),
        })
        total_pass_rate += eval_result.behavioral_pass_rate
        total_rubric += eval_result.rubric_score
        total_prose += eval_result.prose_score
        total_composite += eval_result.composite
        if not eval_result.gate_passed:
            any_gate_failed = True

    n = max(1, len(v2_cases))
    def avg(x: float) -> float:
        return round(x / n, 2)

    return {
        "skill": skill_name,
        "iteration": iteration,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "num_cases": len(v2_cases),
        "avg_behavioral_pass_rate": avg(total_pass_rate),
        "avg_rubric_score": avg(total_rubric),
        "avg_prose_score": avg(total_prose),
        "avg_composite": avg(total_composite),
        "gate_passed_all_cases": not any_gate_failed,
        "gate_threshold": V2_BEHAVIORAL_GATE_THRESHOLD,
        "run_cost_usd": round(total_cost, 4),
        "per_case": per_case_results,
    }


def append_log(entry: dict) -> None:
    V2_EXPERIMENTS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with V2_EXPERIMENTS_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# Commit decision rule
# ---------------------------------------------------------------------------

NOISE_THRESHOLD = 1.0  # composite deltas below this are treated as noise

ESCALATIONS_LOG = RESULTS_DIR / "escalations.jsonl"


def _log_escalation(rule: str, path: Path, context: str) -> None:
    """Append a structured escalation entry. Human reviews before next run."""
    ESCALATIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "rule": rule,
        "path": str(path),
        "zone": zone_of(path),
        "context": context,
    }
    with ESCALATIONS_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def _recent_commits_for(path: Path, days: int) -> int:
    """Count autoimprove commits that touched `path` in the last N days."""
    since = f"{days}.days.ago"
    rel = path.relative_to(PROJECT_ROOT) if path.is_absolute() else path
    try:
        log = subprocess.run(
            ["git", "log", f"--since={since}", "--oneline", "--", str(rel)],
            capture_output=True, text=True, cwd=PROJECT_ROOT, check=True,
        )
        lines = [l for l in log.stdout.splitlines() if "autoimprove" in l.lower()]
        return len(lines)
    except subprocess.CalledProcessError:
        return 0


def decide_action(prev: dict, new: dict) -> tuple[str, str]:
    """
    v2 commit/revert decision. Returns (action, reason).

    Actions:
      - "commit":  keep the change, update baseline to `new`
      - "revert":  discard the change, restore previous skill file

    Rules (in priority order):
      1. Gate regression (was passing, now failing) → revert
      2. Gate improvement (was failing, now passing) → commit
      3. Both gates in same state:
         a. composite improved by > NOISE_THRESHOLD → commit
         b. composite regressed by > NOISE_THRESHOLD → revert
         c. otherwise (noise) → revert (avoid churn on non-improvements)
    """
    prev_gate = prev['gate_passed_all_cases']
    new_gate = new['gate_passed_all_cases']

    if prev_gate and not new_gate:
        return "revert", (
            f"gate regression: was passing, now failing "
            f"(behav {prev['avg_behavioral_pass_rate']:.2f} -> "
            f"{new['avg_behavioral_pass_rate']:.2f})"
        )
    if not prev_gate and new_gate:
        return "commit", (
            f"gate improvement: was failing, now passing "
            f"(behav {prev['avg_behavioral_pass_rate']:.2f} -> "
            f"{new['avg_behavioral_pass_rate']:.2f})"
        )

    delta = new['avg_composite'] - prev['avg_composite']
    if delta > NOISE_THRESHOLD:
        return "commit", f"composite improved by {delta:+.2f}"
    if delta < -NOISE_THRESHOLD:
        return "revert", f"composite regressed by {delta:+.2f}"
    return "revert", f"within noise (delta {delta:+.2f}), no commit"


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run_loop_v2(
    skill_name: str,
    max_iterations: int = 10,
    baseline_only: bool = False,
    baseline_runs: int = 1,
) -> None:
    """
    Full propose→apply→re-run cycle for a skill.

    The skill is copied into work/{skill}-v2.md. Runner and evaluator use
    that copy. The original at ~/.claude/skills/{skill}/SKILL.md is never
    touched during the loop. Promotion back to ~/.claude/ is a manual step
    after the loop finishes.
    """
    source = skill_source_path(skill_name)
    if not source.exists():
        print(f"ERROR: skill source missing: {source}")
        sys.exit(1)

    directive = load_directive(skill_name)
    client = anthropic.Anthropic(api_key=get_api_key())

    print(f"=== autoimprove v2: {skill_name} ===")
    print(f"source: {source}")
    work_path = setup_work_copy_v2(skill_name)
    print(f"work copy: {work_path}")

    branch = setup_branch_v2(skill_name)
    initial_commit = git_commit(
        work_path,
        f"autoimprove v2({skill_name}): initial copy for propose cycle",
    )
    print(f"branch: {branch}  initial: {initial_commit}")

    # Baseline
    print(f"\n--- baseline (n={baseline_runs}) ---")
    baseline_entries = []
    for i in range(baseline_runs):
        entry = run_iteration(skill_name, iteration=0, skill_path_override=work_path)
        entry["phase"] = "baseline"
        append_log(entry)
        baseline_entries.append(entry)
        print(
            f"  behav={entry['avg_behavioral_pass_rate']:.2f} "
            f"rubric={entry['avg_rubric_score']:.1f} "
            f"prose={entry['avg_prose_score']:.1f} "
            f"composite={entry['avg_composite']:.1f} "
            f"gate={entry['gate_passed_all_cases']} "
            f"cost=${entry['run_cost_usd']:.3f}"
        )
    current = baseline_entries[-1]
    total_cost = sum(e['run_cost_usd'] for e in baseline_entries)

    if baseline_only:
        print(f"\n[baseline-only] total cost ${total_cost:.3f}")
        return

    convergence_count = 0

    for iteration in range(1, max_iterations + 1):
        if total_cost >= V2_COST_CAP_PER_RUN:
            print(f"\n[stop] cost cap reached: ${total_cost:.3f} >= ${V2_COST_CAP_PER_RUN}")
            break

        print(f"\n--- iter {iteration} ---")

        # Propose
        skill_content = work_path.read_text()
        try:
            modified, summary, prop_in, prop_out = propose_modification_v2(
                skill_content=skill_content,
                directive=directive,
                aggregated=current,
                client=client,
            )
        except Exception as e:
            print(f"  [error] propose failed: {e}")
            continue
        prop_cost = estimate_propose_cost(prop_in, prop_out)
        total_cost += prop_cost

        if not modified.strip() or modified.strip() == skill_content.strip():
            print(f"  [skip] empty or identical proposal — likely convergence signal")
            convergence_count += 1
            if convergence_count >= 3:
                print(f"\n[stop] 3 consecutive no-op proposals, converged")
                break
            continue

        # Apply + re-score
        backup = skill_content
        try:
            assert_writable(work_path, reason=f"iter {iteration} apply")
        except ZoneViolation as zv:
            print(f"  [halt] zone violation on apply: {zv}")
            _log_escalation("zone_violation_apply", work_path, str(zv))
            break
        work_path.write_text(modified)
        try:
            new_entry = run_iteration(
                skill_name, iteration=iteration, skill_path_override=work_path
            )
        except Exception as e:
            print(f"  [error] re-score failed, reverting: {e}")
            work_path.write_text(backup)
            continue
        new_entry["phase"] = "propose"
        new_entry["change_summary"] = summary
        new_entry["propose_cost_usd"] = round(prop_cost, 4)
        total_cost += new_entry['run_cost_usd']

        action, reason = decide_action(current, new_entry)
        new_entry["action"] = action
        new_entry["action_reason"] = reason

        print(
            f"  behav={new_entry['avg_behavioral_pass_rate']:.2f} "
            f"rubric={new_entry['avg_rubric_score']:.1f} "
            f"prose={new_entry['avg_prose_score']:.1f} "
            f"composite={new_entry['avg_composite']:.1f} "
            f"gate={new_entry['gate_passed_all_cases']}"
        )
        print(f"  change: {summary}")
        print(f"  action: {action.upper()} — {reason}")

        # Drift watchdog: cooldown rule (max 5 commits to same file per 7 days).
        # Checked before committing so we stop cleanly if we've been churning.
        if action == "commit":
            recent = _recent_commits_for(work_path, days=7)
            if recent >= 5:
                print(
                    f"  [halt] cooldown rule: {recent} commits to "
                    f"{work_path.name} in last 7 days (limit 5)"
                )
                _log_escalation(
                    "cooldown_exceeded",
                    work_path,
                    f"{recent} commits in 7 days",
                )
                work_path.write_text(backup)
                break

        if action == "commit":
            msg = (
                f"autoimprove v2({skill_name}): "
                f"composite {current['avg_composite']:.1f} -> {new_entry['avg_composite']:.1f} "
                f"behav {current['avg_behavioral_pass_rate']:.2f} -> {new_entry['avg_behavioral_pass_rate']:.2f}\n\n"
                f"{summary}"
            )
            commit_hash = git_commit(work_path, msg)
            new_entry["commit"] = commit_hash
            current = new_entry
            convergence_count = 0
        else:
            work_path.write_text(backup)
            convergence_count += 1
            if convergence_count >= 3:
                append_log(new_entry)
                print(f"\n[stop] 3 consecutive reverts, converged")
                break

        append_log(new_entry)
        print(f"  total cost so far: ${total_cost:.3f}")

    # Summary
    print(f"\n=== summary ===")
    print(f"skill: {skill_name}")
    baseline = baseline_entries[-1]
    print(
        f"baseline: behav={baseline['avg_behavioral_pass_rate']:.2f}  "
        f"composite={baseline['avg_composite']:.1f}"
    )
    print(
        f"final:    behav={current['avg_behavioral_pass_rate']:.2f}  "
        f"composite={current['avg_composite']:.1f}"
    )
    delta_behav = current['avg_behavioral_pass_rate'] - baseline['avg_behavioral_pass_rate']
    delta_comp = current['avg_composite'] - baseline['avg_composite']
    print(f"delta:    behav={delta_behav:+.2f}  composite={delta_comp:+.1f}")
    print(f"branch: {branch}")
    print(f"work copy: {work_path}")
    print(f"total cost: ${total_cost:.3f}")
    if delta_comp > 0 or delta_behav > 0:
        print(f"\nTo promote the improved skill back to the toolkit:")
        print(f"  cp {work_path} {source}")


def main() -> None:
    parser = argparse.ArgumentParser(description="autoimprove v2 runner")
    parser.add_argument("--skill", required=True,
                         help="Skill name (e.g. scaffolding-projects)")
    parser.add_argument("--max-iterations", type=int, default=10,
                         help="Max propose iterations (default 10)")
    parser.add_argument("--baseline-only", action="store_true",
                         help="Run current skill without proposing changes")
    parser.add_argument("--baseline-runs", type=int, default=1,
                         help="How many runs to average for the initial baseline (default 1)")
    parser.add_argument("--iterations", type=int, default=None,
                         help="[deprecated alias for --baseline-runs when --baseline-only]")
    args = parser.parse_args()

    # Backward-compat: --iterations used to mean baseline runs in scaffold mode
    baseline_runs = args.baseline_runs
    if args.iterations is not None and args.baseline_only:
        baseline_runs = args.iterations

    print(f"[v2] skill={args.skill} gate_threshold={V2_BEHAVIORAL_GATE_THRESHOLD}")
    run_loop_v2(
        skill_name=args.skill,
        max_iterations=args.max_iterations,
        baseline_only=args.baseline_only,
        baseline_runs=baseline_runs,
    )


if __name__ == "__main__":
    main()
