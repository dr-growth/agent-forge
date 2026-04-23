"""
Three-signal evaluator for autoimprove v2.

Signals:
  1. Behavioral — deterministic assertions run by src.sandbox.assertions
  2. Rubric     — Opus 4.7 grading the SKILL file itself against Anthropic's
                   building-skills doc (external, procedural, harder to game)
  3. Prose      — existing v1 Haiku prose-quality score (reused from evaluate.py)

The v2 evaluator applies a GATE on behavioral_pass_rate: runs below the
threshold are rejected before the composite is even computed.
"""

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

import anthropic

from .config import (
    get_api_key,
    V2_RUBRIC_JUDGE_MODEL,
    V2_RUBRIC_JUDGE_MAX_TOKENS,
    V2_BEHAVIORAL_GATE_THRESHOLD,
    V2_COMPOSITE_WEIGHTS,
    V2_RUBRIC_SOURCE,
)
from .evaluate import evaluate as evaluate_v1
from .sandbox.assertions import run_behavioral_checks


@dataclass
class EvalV2Result:
    gate_passed: bool
    behavioral_pass_rate: float
    rubric_score: float
    prose_score: float
    composite: float
    dimensions: dict = field(default_factory=dict)
    reasoning: dict = field(default_factory=dict)
    behavioral_detail: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Rubric scoring (Opus as judge against building-skills doc)
# ---------------------------------------------------------------------------

RUBRIC_PROMPT = """You are auditing a Claude Code SKILL.md file against the
authoritative authoring guide below. Apply the guide's criteria procedurally.
Do not grade on prose aesthetics or personal taste. Grade on conformance.

## Authoring guide (authoritative)
{rubric_source}

## Skill file being audited
```
{skill_content}
```

## Dimensions (score each 0-10)

1. DESCRIPTION_QUALITY — does the `description` field clearly state what the
   skill does AND when to use it, include trigger keywords, use third person,
   stay under 1024 chars?
2. NAME_FORMAT — is `name` gerund form (verb+ing), lowercase, hyphens, ≤64
   chars? (If the skill is an explicit exception noted in the file, score 10.)
3. FRONTMATTER_HYGIENE — no disallowed fields (allowed-tools, model, color,
   tools). Frontmatter is clean.
4. BODY_LENGTH — body ≤500 lines; if longer, uses progressive disclosure via
   linked reference files.
5. PROGRESSIVE_DISCLOSURE — for complex skills, reference files are used
   appropriately and linked from SKILL.md.
6. IMPERATIVE_VOICE — instructions use imperative form ("Create", "Read",
   "Ask"), not descriptive prose about what the skill does.
7. CONCISENESS — no redundant explanations of things Claude already knows;
   no filler. Every section earns its token cost.
8. WHEN_TO_USE_IN_DESCRIPTION — trigger/use-case info lives in the
   description field, not duplicated in the body (since body is not loaded
   until after the skill is triggered).

Respond with ONLY a JSON object:
{{
  "DESCRIPTION_QUALITY":       {{"score": <0-10>, "reasoning": "<one sentence>"}},
  "NAME_FORMAT":               {{"score": <0-10>, "reasoning": "<one sentence>"}},
  "FRONTMATTER_HYGIENE":       {{"score": <0-10>, "reasoning": "<one sentence>"}},
  "BODY_LENGTH":               {{"score": <0-10>, "reasoning": "<one sentence>"}},
  "PROGRESSIVE_DISCLOSURE":    {{"score": <0-10>, "reasoning": "<one sentence>"}},
  "IMPERATIVE_VOICE":          {{"score": <0-10>, "reasoning": "<one sentence>"}},
  "CONCISENESS":               {{"score": <0-10>, "reasoning": "<one sentence>"}},
  "WHEN_TO_USE_IN_DESCRIPTION":{{"score": <0-10>, "reasoning": "<one sentence>"}}
}}"""


def score_rubric(skill_content: str,
                  client: anthropic.Anthropic | None = None
                  ) -> tuple[float, dict, dict]:
    """
    Grade a SKILL.md file against Anthropic's building-skills rubric using
    Opus 4.7. Returns (normalized_score_0_100, per_dim_scores, per_dim_reasoning).
    """
    if not V2_RUBRIC_SOURCE.exists():
        return 50.0, {}, {"error": f"rubric source missing: {V2_RUBRIC_SOURCE}"}

    rubric_text = V2_RUBRIC_SOURCE.read_text()
    # Cap rubric to control token cost; the first ~500 lines cover the core
    rubric_text = "\n".join(rubric_text.splitlines()[:500])

    client = client or anthropic.Anthropic(api_key=get_api_key())
    prompt = RUBRIC_PROMPT.format(
        rubric_source=rubric_text,
        skill_content=skill_content[:16000],
    )

    response = client.messages.create(
        model=V2_RUBRIC_JUDGE_MODEL,
        max_tokens=V2_RUBRIC_JUDGE_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    try:
        if "```" in text:
            m = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
            if m:
                text = m.group(1)
        data = json.loads(text)
    except (json.JSONDecodeError, AttributeError):
        return 50.0, {}, {"parse_error": text[:200]}

    scores = {}
    reasoning = {}
    for dim, payload in data.items():
        if isinstance(payload, dict) and "score" in payload:
            scores[dim] = float(payload["score"])
            reasoning[dim] = payload.get("reasoning", "")

    if not scores:
        return 50.0, {}, {"empty_scores": text[:200]}

    # Normalize sum of 0-10 scores across 8 dimensions → 0-100
    normalized = (sum(scores.values()) / (len(scores) * 10)) * 100
    return round(normalized, 2), scores, reasoning


# ---------------------------------------------------------------------------
# Main v2 evaluator
# ---------------------------------------------------------------------------

def evaluate_v2(
    output: str,
    test_case: dict,
    skill_content: str,
    sandbox_root: Path | None = None,
    skill_type: str = "execution",
) -> EvalV2Result:
    """
    Apply the three-signal evaluation.

    Args:
      output: the text produced by the skill on this test case
      test_case: the full v2 test case dict (has `behavioral_checks`, `ground_truth`, etc.)
      skill_content: the raw contents of the SKILL.md file being evaluated
      sandbox_root: tempdir where file-system effects can be observed
      skill_type: for the v1 prose scorer's weight selection

    Returns:
      EvalV2Result with gate_passed flag and all three signals.
    """
    # Signal 1: Behavioral
    behavioral = run_behavioral_checks(
        output,
        test_case.get("behavioral_checks", {}),
        sandbox_root=sandbox_root,
    )
    gate_passed = behavioral["pass_rate"] >= V2_BEHAVIORAL_GATE_THRESHOLD

    # Signal 2: Rubric (Opus grading SKILL.md itself)
    rubric_score, rubric_dims, rubric_reasoning = score_rubric(skill_content)

    # Signal 3: Prose (existing v1 evaluator)
    v1_result = evaluate_v1(
        output=output,
        schema=test_case.get("schema", {}),
        ground_truth=test_case.get("ground_truth", ""),
        skill_type=skill_type,
    )
    prose_score = v1_result.composite

    # Composite (only meaningful if gate passes; still computed for logging)
    composite = (
        V2_COMPOSITE_WEIGHTS["rubric"] * rubric_score
        + V2_COMPOSITE_WEIGHTS["prose"] * prose_score
    )

    return EvalV2Result(
        gate_passed=gate_passed,
        behavioral_pass_rate=round(behavioral["pass_rate"], 3),
        rubric_score=rubric_score,
        prose_score=prose_score,
        composite=round(composite, 2),
        dimensions={
            "rubric_per_dim": rubric_dims,
            "prose_per_dim": v1_result.dimensions,
        },
        reasoning={
            "rubric": rubric_reasoning,
            "prose": v1_result.reasoning,
        },
        behavioral_detail=behavioral,
    )
