"""
Main improvement loop engine.

Follows Karpathy's autoresearch pattern adapted for PAIOS skills:
1. Read current skill file
2. Run skill against test cases (runner.py)
3. Score output (evaluate.py)
4. Propose modification via Claude API
5. Apply modification to skill file
6. Run again, score again
7. If improved: git commit (preserve)
8. If regressed: git reset (discard)
9. Log experiment results
10. Repeat until convergence or interruption

Usage:
    uv run -m src.loop --skill scout
    uv run -m src.loop --skill scout --max-iterations 10
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic

from .config import (
    get_api_key,
    PROJECT_ROOT,
    SKILLS_DIR,
    TEST_CASES_DIR,
    DIRECTIVES_DIR,
    RESULTS_DIR,
    EXPERIMENTS_LOG,
    PROPOSER_MODEL,
    PROPOSER_MAX_TOKENS,
    SKILL_TYPES,
    CONVERGENCE_THRESHOLD,
    CONVERGENCE_RUNS,
    COST_CAP_PER_RUN,
    COST_PER_1M_INPUT,
    COST_PER_1M_OUTPUT,
)
from .runner import TestCase, run_skill_on_cases
from .evaluate import evaluate

# Working directory for skill copies (git-tracked within this project)
WORK_DIR = PROJECT_ROOT / "work"


# ---------------------------------------------------------------------------
# Proposal generation
# ---------------------------------------------------------------------------

PROPOSE_PROMPT = """You are an expert prompt engineer improving a PAIOS skill file.

## Current Skill File
```
{skill_content}
```

## Improvement Directive
{directive}

## Current Scores (composite: {composite}/100)
{scores_summary}

## Test Case Outputs and Evaluator Feedback
{eval_feedback}

## Your Task
Propose a SPECIFIC modification to the skill file that will improve the composite score.

Rules:
- Output the COMPLETE modified skill file (not a diff)
- Make ONE focused change per proposal (not a rewrite)
- Focus on the lowest-scoring dimensions
- Do NOT change: governance section, model assignment, scope boundaries, tool manifest
- DO change: instruction text, output format guidance, examples, decision logic, confidence calibration rules

Respond with the complete modified skill file content, wrapped in <skill> tags:
<skill>
[complete modified skill file here]
</skill>"""


def propose_modification(
    skill_content: str,
    directive: str,
    composite: float,
    dimensions: dict,
    reasoning: dict,
    test_outputs: list[dict],
    client: anthropic.Anthropic,
) -> tuple[str, int, int]:
    """
    Ask Claude to propose a modification to the skill file.

    Returns: (modified_skill_content, tokens_in, tokens_out)
    """
    scores_summary = "\n".join(
        f"  {dim}: {score:.1f}/100 -- {reasoning.get(dim, '')}"
        for dim, score in sorted(dimensions.items(), key=lambda x: x[1])
    )

    eval_feedback = ""
    for i, to in enumerate(test_outputs):
        eval_feedback += f"\n### Test Case {i+1}: {to['test_name']}\n"
        eval_feedback += f"Output excerpt (first 1000 chars):\n{to['output'][:1000]}\n"
        eval_feedback += f"Scores: {json.dumps(to['dimensions'], indent=2)}\n"

    prompt = PROPOSE_PROMPT.format(
        skill_content=skill_content[:12000],  # truncate very long skills
        directive=directive,
        composite=f"{composite:.1f}",
        scores_summary=scores_summary,
        eval_feedback=eval_feedback[:6000],
    )

    response = client.messages.create(
        model=PROPOSER_MODEL,
        max_tokens=PROPOSER_MAX_TOKENS * 4,  # skill files can be large
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text

    # Extract skill content from <skill> tags
    import re
    match = re.search(r'<skill>\s*(.*?)\s*</skill>', text, re.DOTALL)
    if match:
        modified = match.group(1)
    else:
        # Fallback: assume entire response is the skill file
        modified = text

    return modified, response.usage.input_tokens, response.usage.output_tokens


# ---------------------------------------------------------------------------
# Git operations
# ---------------------------------------------------------------------------

def git(cmd: str, cwd: Path | None = None) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + cmd.split(),
        capture_output=True, text=True, cwd=cwd,
    )
    return result.stdout.strip()


def git_commit(skill_path: Path, message: str):
    """Stage and commit changes to a skill file."""
    subprocess.run(["git", "add", str(skill_path)], cwd=PROJECT_ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=PROJECT_ROOT, capture_output=True, check=True,
    )


def git_reset_file(skill_path: Path):
    """Reset a skill file to the last committed state."""
    subprocess.run(
        ["git", "checkout", "HEAD", "--", str(skill_path)],
        cwd=PROJECT_ROOT, capture_output=True,
    )


def git_current_hash() -> str:
    return git("rev-parse --short HEAD", cwd=PROJECT_ROOT)


def setup_branch(skill_name: str):
    """Create and checkout a branch for this improvement run."""
    tag = datetime.now().strftime("%Y%m%d")
    branch = f"autoimprove/{skill_name}-{tag}"

    existing = git(f"branch --list {branch}", cwd=PROJECT_ROOT)
    if existing:
        git(f"checkout {branch}", cwd=PROJECT_ROOT)
    else:
        git(f"checkout -b {branch}", cwd=PROJECT_ROOT)

    return branch


def setup_work_copy(skill_name: str) -> Path:
    """Copy a skill file into the work directory for git-tracked modification."""
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    source = SKILLS_DIR / f"{skill_name}.md"
    dest = WORK_DIR / f"{skill_name}.md"
    shutil.copy2(source, dest)
    return dest


# ---------------------------------------------------------------------------
# Experiment logging
# ---------------------------------------------------------------------------

def log_experiment(
    skill_name: str,
    iteration: int,
    old_score: float,
    new_score: float,
    status: str,  # "keep" | "discard" | "error"
    change_summary: str,
    cost_usd: float,
    commit_hash: str = "",
    dimensions_before: dict | None = None,
    dimensions_after: dict | None = None,
):
    """Append an experiment record to the JSONL log."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "skill": skill_name,
        "iteration": iteration,
        "old_score": round(old_score, 2),
        "new_score": round(new_score, 2),
        "delta": round(new_score - old_score, 2),
        "status": status,
        "change_summary": change_summary,
        "cost_usd": round(cost_usd, 4),
        "commit": commit_hash,
        "dimensions_before": dimensions_before,
        "dimensions_after": dimensions_after,
    }
    with open(EXPERIMENTS_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def load_test_cases(skill_name: str) -> list[TestCase]:
    """Load all test cases for a skill."""
    tc_dir = TEST_CASES_DIR / skill_name
    if not tc_dir.exists():
        raise FileNotFoundError(f"No test cases found at {tc_dir}")
    cases = []
    for f in sorted(tc_dir.glob("*.json")):
        cases.append(TestCase.from_file(f))
    if not cases:
        raise FileNotFoundError(f"No .json test case files in {tc_dir}")
    return cases


def load_directive(skill_name: str) -> str:
    """Load the improvement directive for a skill."""
    path = DIRECTIVES_DIR / f"{skill_name}.md"
    if not path.exists():
        return "Improve overall quality: specificity, structure, confidence calibration, actionability."
    return path.read_text()


def score_skill(
    skill_name: str,
    test_cases: list[TestCase],
    skill_type: str,
    skill_path: Path | None = None,
) -> tuple[float, dict, dict, list[dict], float]:
    """
    Run skill against all test cases and return aggregate score.

    Returns: (composite, avg_dimensions, avg_reasoning, per_case_results, total_cost)
    """
    results = run_skill_on_cases(skill_name, test_cases, skill_path)
    total_cost = sum(r.cost_usd for r in results)

    eval_results = []
    for result, tc in zip(results, test_cases):
        er = evaluate(
            output=result.output,
            schema=tc.schema,
            ground_truth=tc.ground_truth,
            skill_type=skill_type,
        )
        eval_results.append({
            "test_name": tc.name,
            "output": result.output,
            "composite": er.composite,
            "dimensions": er.dimensions,
            "reasoning": er.reasoning,
        })

    # Average across test cases
    composites = [er["composite"] for er in eval_results]
    composite = sum(composites) / len(composites)

    all_dims = [er["dimensions"] for er in eval_results]
    avg_dims = {}
    for dim in all_dims[0]:
        avg_dims[dim] = sum(d[dim] for d in all_dims) / len(all_dims)

    all_reasons = [er["reasoning"] for er in eval_results]
    avg_reasons = {}
    for dim in all_reasons[0]:
        avg_reasons[dim] = "; ".join(r.get(dim, "") for r in all_reasons)

    return composite, avg_dims, avg_reasons, eval_results, total_cost


def run_loop(skill_name: str, max_iterations: int = 50):
    """
    Main improvement loop for a single skill.

    This is the autoresearch pattern adapted for PAIOS:
    - The skill .md file is the only thing modified (like train.py)
    - The evaluator is immutable during the run (like prepare.py)
    - Git commit on improvement, git reset on regression

    The skill file is COPIED into work/ for modification.
    The original in ~/.claude/agents/ is never touched during the loop.
    After the loop, the improved copy can be manually promoted.
    """
    source_path = SKILLS_DIR / f"{skill_name}.md"
    if not source_path.exists():
        print(f"ERROR: Skill file not found: {source_path}")
        sys.exit(1)

    skill_type = SKILL_TYPES.get(skill_name, "research")
    test_cases = load_test_cases(skill_name)
    directive = load_directive(skill_name)
    client = anthropic.Anthropic(api_key=get_api_key())

    # Copy skill into work directory (git-tracked)
    skill_path = setup_work_copy(skill_name)

    print(f"=== autoimprove: {skill_name} ===")
    print(f"Skill type: {skill_type}")
    print(f"Test cases: {len(test_cases)}")
    print(f"Source: {source_path}")
    print(f"Working copy: {skill_path}")
    print()

    # Setup git branch and commit initial copy
    branch = setup_branch(skill_name)
    git_commit(skill_path, f"autoimprove({skill_name}): initial copy for improvement run")
    print(f"Branch: {branch}")

    # Baseline run (using the work copy)
    print("\n--- Baseline ---")
    baseline_score, baseline_dims, baseline_reasons, baseline_results, baseline_cost = (
        score_skill(skill_name, test_cases, skill_type, skill_path)
    )
    total_cost = baseline_cost
    print(f"Baseline composite: {baseline_score:.1f}/100")
    for dim, score in sorted(baseline_dims.items(), key=lambda x: x[1]):
        print(f"  {dim}: {score:.1f}")
    print(f"Cost so far: ${total_cost:.4f}")

    log_experiment(
        skill_name=skill_name,
        iteration=0,
        old_score=0,
        new_score=baseline_score,
        status="baseline",
        change_summary="baseline measurement",
        cost_usd=baseline_cost,
        dimensions_after=baseline_dims,
    )

    current_score = baseline_score
    current_dims = baseline_dims
    current_reasons = baseline_reasons
    current_results = baseline_results
    convergence_count = 0

    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration} ---")

        # Check cost cap
        if total_cost >= COST_CAP_PER_RUN:
            print(f"Cost cap reached (${total_cost:.2f} >= ${COST_CAP_PER_RUN}). Stopping.")
            break

        # Read current skill content
        skill_content = skill_path.read_text()

        # Propose modification
        print("Proposing modification...")
        try:
            modified_content, prop_in, prop_out = propose_modification(
                skill_content=skill_content,
                directive=directive,
                composite=current_score,
                dimensions=current_dims,
                reasoning=current_reasons,
                test_outputs=current_results,
                client=client,
            )
            prop_cost = (
                (prop_in / 1_000_000) * COST_PER_1M_INPUT.get(PROPOSER_MODEL, 3.0)
                + (prop_out / 1_000_000) * COST_PER_1M_OUTPUT.get(PROPOSER_MODEL, 15.0)
            )
            total_cost += prop_cost
        except Exception as e:
            print(f"Proposal failed: {e}")
            log_experiment(
                skill_name=skill_name,
                iteration=iteration,
                old_score=current_score,
                new_score=current_score,
                status="error",
                change_summary=f"proposal failed: {e}",
                cost_usd=0,
            )
            continue

        # Sanity check: modification shouldn't be empty or identical
        if not modified_content.strip():
            print("Empty modification proposed. Skipping.")
            continue
        if modified_content.strip() == skill_content.strip():
            print("Identical content proposed. Skipping.")
            continue

        # Apply modification
        backup = skill_content
        skill_path.write_text(modified_content)

        # Score the modified skill
        print("Scoring modified skill...")
        try:
            new_score, new_dims, new_reasons, new_results, run_cost = (
                score_skill(skill_name, test_cases, skill_type, skill_path)
            )
            total_cost += run_cost
        except Exception as e:
            print(f"Scoring failed: {e}")
            skill_path.write_text(backup)
            log_experiment(
                skill_name=skill_name,
                iteration=iteration,
                old_score=current_score,
                new_score=current_score,
                status="error",
                change_summary=f"scoring failed: {e}",
                cost_usd=run_cost if 'run_cost' in dir() else 0,
            )
            continue

        delta = new_score - current_score
        print(f"Score: {current_score:.1f} -> {new_score:.1f} (delta: {delta:+.1f})")
        for dim in sorted(new_dims):
            old = current_dims.get(dim, 0)
            new = new_dims[dim]
            marker = "+" if new > old else "-" if new < old else "="
            print(f"  {dim}: {old:.1f} -> {new:.1f} [{marker}]")

        if delta > 0:
            # Improvement: commit
            print(f"IMPROVED by {delta:.1f}. Committing.")
            commit_msg = (
                f"autoimprove({skill_name}): {current_score:.1f} -> {new_score:.1f} "
                f"(+{delta:.1f})"
            )
            git_commit(skill_path, commit_msg)
            commit_hash = git_current_hash()

            log_experiment(
                skill_name=skill_name,
                iteration=iteration,
                old_score=current_score,
                new_score=new_score,
                status="keep",
                change_summary=commit_msg,
                cost_usd=prop_cost + run_cost,
                commit_hash=commit_hash,
                dimensions_before=current_dims,
                dimensions_after=new_dims,
            )

            current_score = new_score
            current_dims = new_dims
            current_reasons = new_reasons
            current_results = new_results
            convergence_count = 0
        else:
            # Regression or no change: reset
            print(f"No improvement (delta={delta:.1f}). Resetting.")
            skill_path.write_text(backup)

            log_experiment(
                skill_name=skill_name,
                iteration=iteration,
                old_score=current_score,
                new_score=new_score,
                status="discard",
                change_summary=f"regression: {delta:.1f}",
                cost_usd=prop_cost + run_cost,
                dimensions_before=current_dims,
                dimensions_after=new_dims,
            )

            # Check convergence
            if abs(delta) < CONVERGENCE_THRESHOLD:
                convergence_count += 1
                if convergence_count >= CONVERGENCE_RUNS:
                    print(
                        f"\nConverged: delta < {CONVERGENCE_THRESHOLD} for "
                        f"{CONVERGENCE_RUNS} consecutive runs. Stopping."
                    )
                    break
            else:
                convergence_count = 0

        print(f"Total cost: ${total_cost:.4f}")

    # Summary
    total_delta = current_score - baseline_score
    print(f"\n=== Summary ===")
    print(f"Skill: {skill_name}")
    print(f"Baseline: {baseline_score:.1f} -> Final: {current_score:.1f} (delta: {total_delta:+.1f})")
    print(f"Iterations: {iteration}")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Branch: {branch}")
    print(f"Working copy: {skill_path}")
    if total_delta > 0:
        print(f"\nTo promote the improved skill:")
        print(f"  cp {skill_path} {source_path}")


def main():
    parser = argparse.ArgumentParser(description="autoimprove: autonomous skill improvement")
    parser.add_argument("--skill", required=True, help="Skill name to improve (e.g., scout)")
    parser.add_argument("--max-iterations", type=int, default=50, help="Max improvement iterations")
    args = parser.parse_args()

    run_loop(args.skill, args.max_iterations)


if __name__ == "__main__":
    main()
