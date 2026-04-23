#!/usr/bin/env python3
"""
Score a skill's output quality using autoimprove's evaluation system.

Usage:
    uv run python score_skill.py --skill editing-copy --skill-path ~/claude-code-skills/skills/editing-copy/SKILL.md
    uv run python score_skill.py --skill editing-copy --skill-path ~/claude-code-skills/skills/editing-copy/SKILL.md --heuristic-only
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.runner import TestCase, run_skill
from src.evaluate import evaluate
from src.config import TEST_CASES_DIR


def load_test_cases(skill_name: str) -> list[TestCase]:
    tc_dir = TEST_CASES_DIR / skill_name
    if not tc_dir.exists():
        print(f"No test cases at {tc_dir}")
        return []
    cases = []
    for f in sorted(tc_dir.glob("*.json")):
        cases.append(TestCase.from_file(f))
    return cases


def score(skill_name: str, skill_path: Path, skill_type: str = "research", heuristic_only: bool = False):
    test_cases = load_test_cases(skill_name)
    if not test_cases:
        return None

    results = []
    total_cost = 0.0

    for tc in test_cases:
        # Run the skill against the test case
        run_result = run_skill(skill_name, tc, skill_path=skill_path)
        total_cost += run_result.cost_usd

        # Evaluate the output
        gt = "" if heuristic_only else tc.ground_truth
        eval_result = evaluate(
            output=run_result.output,
            schema=tc.schema,
            ground_truth=gt,
            skill_type=skill_type,
        )

        results.append({
            "test_case": tc.name,
            "composite": round(eval_result.composite, 1),
            "dimensions": {k: round(v, 1) for k, v in eval_result.dimensions.items()},
            "reasoning": eval_result.reasoning,
            "run_cost": run_result.cost_usd,
        })

    # Average across test cases
    avg_composite = sum(r["composite"] for r in results) / len(results)
    avg_dims = {}
    for dim in results[0]["dimensions"]:
        avg_dims[dim] = round(sum(r["dimensions"][dim] for r in results) / len(results), 1)

    return {
        "skill": skill_name,
        "composite": round(avg_composite, 1),
        "dimensions": avg_dims,
        "per_case": results,
        "total_cost": round(total_cost, 4),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--skill-type", default="research")
    parser.add_argument("--heuristic-only", action="store_true")
    args = parser.parse_args()

    result = score(args.skill, args.skill_path, args.skill_type, args.heuristic_only)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No test cases found", file=sys.stderr)
        sys.exit(1)
