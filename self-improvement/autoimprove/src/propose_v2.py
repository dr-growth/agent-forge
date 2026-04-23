"""
v2 proposal generation.

Unlike v1, the propose prompt is fed the BEHAVIORAL GATE signal so the
proposer can target specific failing assertions instead of guessing at
"what would make prose better."

Gate-failing assertions are the highest-priority feedback because they
represent falsifiable behavior the skill either does or doesn't exhibit.
Rubric dims and prose dims are secondary -- rubric tells us about skill
file quality against Anthropic's authoring guide, prose is fuzzy.
"""

import json
import re

import anthropic

from .config import (
    PROPOSER_MODEL,
    PROPOSER_MAX_TOKENS,
    COST_PER_1M_INPUT,
    COST_PER_1M_OUTPUT,
)


PROPOSE_V2_PROMPT = """You are improving a Claude Code SKILL.md file. You have
access to three signals from the v2 evaluator:

  1. BEHAVIORAL — deterministic assertions on the skill's output (highest priority)
  2. RUBRIC     — Opus grading the SKILL file against Anthropic's authoring guide
  3. PROSE      — Haiku grading output prose quality (noisy, lowest priority)

## Current SKILL.md
```
{skill_content}
```

## Improvement Directive
{directive}

## Current Signals
behavioral_pass_rate: {behavioral:.2f} (gate threshold: 0.80)
rubric_score: {rubric:.1f}/100
prose_score: {prose:.1f}/100
composite: {composite:.1f}/100
gate_passed: {gate_passed}

## Failing Behavioral Assertions (ADDRESS THESE FIRST)
{behavioral_failures}

## Rubric Weaknesses (lowest-scoring dimensions)
{rubric_weaknesses}

## Your Task
Propose ONE focused modification to the SKILL.md that addresses the
highest-priority signal:

- If gate_passed is False: the behavioral failures are the ONLY thing that
  matters. Fix the skill so those assertions pass. Do not touch anything else.
- If gate_passed is True: target the lowest-scoring rubric dimension.
  Prose drift alone is not worth a change.

Rules:
- Output the COMPLETE modified SKILL.md (not a diff)
- Make ONE focused change per proposal, not a rewrite
- Do NOT change the YAML frontmatter fields (name, description) unless the
  rubric explicitly flagged them as the weakness to fix
- Do NOT add new sections; prefer tightening existing ones
- Prefer surgical edits (a sentence, a rule, a reordering) over large additions
- Preserve the skill's structure and voice

Respond with the complete modified SKILL.md content wrapped in <skill> tags:
<skill>
[complete modified SKILL.md here]
</skill>

Then in a <change> tag, one-sentence summary of what you changed and why:
<change>
[one-sentence change summary]
</change>"""


def format_behavioral_failures(per_case_results: list[dict]) -> str:
    """Surface failing assertions per test case as actionable proposer input."""
    lines = []
    for case in per_case_results:
        fails = [c for c in case['eval']['behavioral_detail']['results']
                 if not c['passed']]
        if not fails:
            continue
        lines.append(f"\n### [{case['case']}] (pass rate {case['eval']['behavioral_pass_rate']:.2f})")
        for f in fails:
            lines.append(f"  FAIL {f['name']}: {f['detail']}")
        excerpt = case.get('output_excerpt', '')[:500]
        if excerpt:
            lines.append(f"  Output head: {excerpt!r}")
    if not lines:
        return "(no failing behavioral assertions — gate is already passing)"
    return "\n".join(lines)


def format_rubric_weaknesses(per_case_results: list[dict]) -> str:
    """List the lowest-scoring rubric dimensions across cases."""
    dim_scores: dict[str, list[float]] = {}
    for case in per_case_results:
        rubric_per_dim = case['eval']['dimensions'].get('rubric_per_dim', {})
        for dim, score in rubric_per_dim.items():
            dim_scores.setdefault(dim, []).append(float(score))
    if not dim_scores:
        return "(no rubric dims available)"
    avg = {dim: sum(scores) / len(scores) for dim, scores in dim_scores.items()}
    sorted_dims = sorted(avg.items(), key=lambda x: x[1])
    lines = []
    for dim, score in sorted_dims[:4]:  # 4 weakest
        lines.append(f"  {dim}: {score:.1f}/10")
    return "\n".join(lines)


def propose_modification_v2(
    skill_content: str,
    directive: str,
    aggregated: dict,
    client: anthropic.Anthropic,
) -> tuple[str, str, int, int]:
    """
    Ask Claude to propose a v2 skill modification.

    Returns: (modified_skill_content, change_summary, tokens_in, tokens_out)
    """
    per_case = aggregated['per_case']
    behavioral_failures = format_behavioral_failures(per_case)
    rubric_weaknesses = format_rubric_weaknesses(per_case)

    prompt = PROPOSE_V2_PROMPT.format(
        skill_content=skill_content[:14000],
        directive=directive,
        behavioral=aggregated['avg_behavioral_pass_rate'],
        rubric=aggregated['avg_rubric_score'],
        prose=aggregated['avg_prose_score'],
        composite=aggregated['avg_composite'],
        gate_passed=aggregated['gate_passed_all_cases'],
        behavioral_failures=behavioral_failures[:6000],
        rubric_weaknesses=rubric_weaknesses,
    )

    response = client.messages.create(
        model=PROPOSER_MODEL,
        max_tokens=PROPOSER_MAX_TOKENS * 4,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text

    skill_match = re.search(r'<skill>\s*(.*?)\s*</skill>', text, re.DOTALL)
    change_match = re.search(r'<change>\s*(.*?)\s*</change>', text, re.DOTALL)

    modified = skill_match.group(1) if skill_match else text
    summary = change_match.group(1).strip() if change_match else "(no change summary provided)"

    return modified, summary, response.usage.input_tokens, response.usage.output_tokens


def estimate_propose_cost(tokens_in: int, tokens_out: int) -> float:
    return (
        (tokens_in / 1_000_000) * COST_PER_1M_INPUT.get(PROPOSER_MODEL, 3.0)
        + (tokens_out / 1_000_000) * COST_PER_1M_OUTPUT.get(PROPOSER_MODEL, 15.0)
    )
