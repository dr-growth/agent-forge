#!/usr/bin/env python3
"""
Run autoimprove loop on a skill from any path (not just ~/.claude/agents/).

Usage:
    uv run python run_autoimprove_skill.py --skill optimizing-pages --skill-path ~/claude-code-skills/skills/optimizing-pages/SKILL.md --max-iterations 3
"""
import argparse
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.loop import (
    load_test_cases, load_directive, score_skill, propose_modification,
    log_experiment, WORK_DIR, PROJECT_ROOT
)
from src.config import get_api_key, SKILL_TYPES
import anthropic


def run_loop_on_skill(skill_name: str, skill_source: Path, max_iterations: int = 3):
    """Run improvement loop on any skill file."""

    skill_type = SKILL_TYPES.get(skill_name, "execution")
    test_cases = load_test_cases(skill_name)
    directive = load_directive(skill_name)
    client = anthropic.Anthropic(api_key=get_api_key())

    # Copy to work dir
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    skill_path = WORK_DIR / f"{skill_name}.md"
    shutil.copy2(skill_source, skill_path)

    print(f"=== autoimprove: {skill_name} ===")
    print(f"Source: {skill_source}")
    print(f"Working copy: {skill_path}")
    print(f"Test cases: {len(test_cases)}")
    print(f"Max iterations: {max_iterations}")

    # Baseline
    print("\n--- Baseline ---")
    current_score, current_dims, current_reasons, current_results, total_cost = (
        score_skill(skill_name, test_cases, skill_type, skill_path)
    )
    baseline_score = current_score
    print(f"Baseline: {current_score:.1f}/100")
    for dim, score in sorted(current_dims.items(), key=lambda x: x[1]):
        print(f"  {dim}: {score:.1f}")

    best_score = current_score
    best_content = skill_path.read_text()

    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration}/{max_iterations} ---")

        skill_content = skill_path.read_text()

        # Propose
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
        except Exception as e:
            print(f"Proposal failed: {e}")
            continue

        if not modified_content.strip() or modified_content.strip() == skill_content.strip():
            print("No meaningful change proposed. Skipping.")
            continue

        # Apply and re-score
        backup = skill_content
        skill_path.write_text(modified_content)

        print("Scoring modified version...")
        new_score, new_dims, new_reasons, new_results, score_cost = (
            score_skill(skill_name, test_cases, skill_type, skill_path)
        )
        total_cost += score_cost
        delta = new_score - current_score

        if delta > 0:
            print(f"  IMPROVED: {current_score:.1f} -> {new_score:.1f} (+{delta:.1f})")
            current_score = new_score
            current_dims = new_dims
            current_reasons = new_reasons
            current_results = new_results
            if new_score > best_score:
                best_score = new_score
                best_content = modified_content
        else:
            print(f"  REGRESSED: {current_score:.1f} -> {new_score:.1f} ({delta:.1f}) -- rolling back")
            skill_path.write_text(backup)

    # Write best version back
    skill_path.write_text(best_content)

    print(f"\n{'='*60}")
    print(f"RESULT: {skill_name}")
    print(f"  Baseline: {baseline_score:.1f}")
    print(f"  Final:    {best_score:.1f}")
    print(f"  Delta:    {best_score - baseline_score:+.1f}")
    print(f"  Cost:     ${total_cost:.4f}")
    print(f"  Best version at: {skill_path}")

    return {
        "skill": skill_name,
        "baseline": round(baseline_score, 1),
        "final": round(best_score, 1),
        "delta": round(best_score - baseline_score, 1),
        "cost": round(total_cost, 4),
        "output_path": str(skill_path),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--max-iterations", type=int, default=3)
    args = parser.parse_args()

    result = run_loop_on_skill(args.skill, args.skill_path, args.max_iterations)
    print(json.dumps(result, indent=2))
