"""
Automated multi-dimensional scoring for PAIOS skill output.

The evaluator is IMMUTABLE during improvement loops.
It scores skill output on 6 dimensions and returns a composite score.

Three dimensions use heuristic checks (deterministic):
  - completeness: does output cover expected sections?
  - structure: does output follow expected format?
  - confidence_calibration: are confidence scores properly distributed?

Three dimensions use Claude Haiku as judge (semantic):
  - accuracy: are factual claims specific and verifiable?
  - specificity: are claims concrete vs. generic filler?
  - actionability: does output feed downstream agents?

Usage:
    from src.evaluate import evaluate
    result = evaluate(output_text, schema, ground_truth, skill_type="research")
    print(result["composite"])  # float 0-100
    print(result["dimensions"])  # dict of dimension -> score
"""

import re
import json
from dataclasses import dataclass, field, asdict

import anthropic

from .config import (
    get_api_key,
    JUDGE_MODEL,
    JUDGE_MAX_TOKENS,
    SCORING_WEIGHTS,
    SKILL_TYPES,
)


@dataclass
class EvalResult:
    composite: float
    dimensions: dict[str, float] = field(default_factory=dict)
    reasoning: dict[str, str] = field(default_factory=dict)
    skill_type: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Heuristic dimensions (deterministic)
# ---------------------------------------------------------------------------

def score_completeness(output: str, schema: dict) -> tuple[float, str]:
    """
    Score based on presence of expected sections/fields.

    Schema format:
    {
        "required_sections": ["## Summary", "## Findings", ...],
        "required_fields": ["confidence:", "sources:", ...],
        "min_word_count": 500
    }
    """
    scores = []
    reasons = []

    # Check required sections
    required_sections = schema.get("required_sections", [])
    if required_sections:
        found = sum(1 for s in required_sections if s.lower() in output.lower())
        section_score = (found / len(required_sections)) * 100
        scores.append(section_score)
        reasons.append(f"sections: {found}/{len(required_sections)}")

    # Check required fields/patterns
    required_fields = schema.get("required_fields", [])
    if required_fields:
        found = sum(1 for f in required_fields if f.lower() in output.lower())
        field_score = (found / len(required_fields)) * 100
        scores.append(field_score)
        reasons.append(f"fields: {found}/{len(required_fields)}")

    # Check minimum word count
    min_words = schema.get("min_word_count", 0)
    if min_words > 0:
        word_count = len(output.split())
        word_score = min(100, (word_count / min_words) * 100)
        scores.append(word_score)
        reasons.append(f"words: {word_count}/{min_words}")

    if not scores:
        return 50.0, "no schema to validate against"

    return sum(scores) / len(scores), "; ".join(reasons)


def score_structure(output: str, schema: dict) -> tuple[float, str]:
    """
    Score based on structural formatting quality.

    Checks: markdown headers, bullet points, consistent formatting,
    section ordering matches schema.
    """
    scores = []
    reasons = []

    # Has markdown headers
    headers = re.findall(r'^#{1,4}\s+.+', output, re.MULTILINE)
    if headers:
        header_score = min(100, len(headers) * 15)  # ~7 headers = 100
        scores.append(header_score)
        reasons.append(f"headers: {len(headers)}")
    else:
        scores.append(0)
        reasons.append("no headers")

    # Has bullet points or numbered lists
    bullets = re.findall(r'^\s*[-*]\s+.+', output, re.MULTILINE)
    numbered = re.findall(r'^\s*\d+\.\s+.+', output, re.MULTILINE)
    list_items = len(bullets) + len(numbered)
    if list_items > 0:
        list_score = min(100, list_items * 8)  # ~12 items = 100
        scores.append(list_score)
        reasons.append(f"list items: {list_items}")
    else:
        scores.append(20)
        reasons.append("no lists")

    # Section ordering matches schema
    expected_order = schema.get("required_sections", [])
    if len(expected_order) >= 2:
        positions = []
        for section in expected_order:
            pos = output.lower().find(section.lower())
            positions.append(pos if pos >= 0 else float('inf'))
        # Check if positions are monotonically increasing
        ordered = all(a <= b for a, b in zip(positions, positions[1:]))
        order_score = 100 if ordered else 40
        scores.append(order_score)
        reasons.append(f"order: {'correct' if ordered else 'wrong'}")

    if not scores:
        return 50.0, "no structure checks available"

    return sum(scores) / len(scores), "; ".join(reasons)


def score_confidence_calibration(output: str, _schema: dict) -> tuple[float, str]:
    """
    Score based on proper distribution of confidence levels.

    Good calibration: mix of HIGH/MEDIUM/LOW, not all one level.
    Checks for confidence markers in the output.
    """
    # Find confidence markers
    high_count = len(re.findall(r'\b(?:HIGH|high confidence|0\.[89]\d*|0\.9\d*|1\.0)\b', output))
    med_count = len(re.findall(r'\b(?:MEDIUM|medium confidence|0\.[67]\d*)\b', output))
    low_count = len(re.findall(r'\b(?:LOW|low confidence|0\.[0-5]\d*)\b', output))
    total = high_count + med_count + low_count

    if total == 0:
        return 20.0, "no confidence indicators found"

    # Penalize if all one level
    counts = [high_count, med_count, low_count]
    nonzero = sum(1 for c in counts if c > 0)

    if nonzero == 1:
        return 30.0, f"only one confidence level used ({total} markers)"
    elif nonzero == 2:
        return 70.0, f"two confidence levels ({high_count}H/{med_count}M/{low_count}L)"
    else:
        # Check for reasonable distribution (not 90% HIGH)
        if total > 0 and max(counts) / total > 0.8:
            return 60.0, f"skewed distribution ({high_count}H/{med_count}M/{low_count}L)"
        return 90.0, f"well distributed ({high_count}H/{med_count}M/{low_count}L)"


# ---------------------------------------------------------------------------
# Semantic dimensions (Haiku as judge)
# ---------------------------------------------------------------------------

JUDGE_PROMPT = """You are an expert evaluator scoring AI agent output quality.

Score the following output on the dimension: {dimension}

## Dimension Definition
{dimension_def}

## Scoring Scale
0-100 where:
- 0-20: Completely fails on this dimension
- 21-40: Major gaps, mostly generic or wrong
- 41-60: Acceptable but mediocre, some gaps
- 61-80: Good, specific, mostly meets expectations
- 81-100: Excellent, thorough, exceeds expectations

## Ground Truth (what a good answer would include)
{ground_truth}

## Output to Score
{output}

Respond with ONLY a JSON object:
{{"score": <int 0-100>, "reasoning": "<one sentence>"}}"""

DIMENSION_DEFS = {
    "accuracy": (
        "Are factual claims specific and verifiable? Does the output cite real sources, "
        "reference real companies/people/data, and avoid making things up? Penalize "
        "hallucinated facts, vague unsourced claims, and confident statements about "
        "things that don't match the ground truth."
    ),
    "specificity": (
        "Are claims concrete and detailed rather than generic filler? Does the output "
        "contain specific numbers, names, dates, and facts rather than vague platitudes "
        "like 'industry-leading' or 'comprehensive solution'? Penalize hand-wavy language, "
        "corporate buzzwords, and statements that could apply to any company."
    ),
    "actionability": (
        "Does the output provide information that downstream agents or humans can act on? "
        "Does it contain structured findings, clear signals, specific recommendations, "
        "or data points that inform decisions? Penalize outputs that are informative "
        "but don't lead anywhere actionable."
    ),
}


def score_semantic_dimension(
    output: str,
    dimension: str,
    ground_truth: str,
    client: anthropic.Anthropic,
) -> tuple[float, str]:
    """Score a single semantic dimension using Haiku as judge."""
    prompt = JUDGE_PROMPT.format(
        dimension=dimension,
        dimension_def=DIMENSION_DEFS[dimension],
        ground_truth=ground_truth,
        output=output[:8000],  # truncate to control cost
    )

    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=JUDGE_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    # Parse JSON from response
    try:
        # Handle markdown code blocks
        if "```" in text:
            text = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL).group(1)
        data = json.loads(text)
        score = float(data["score"])
        reasoning = data.get("reasoning", "")
        return min(100, max(0, score)), reasoning
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError):
        return 50.0, f"judge parse error: {text[:100]}"


# ---------------------------------------------------------------------------
# Main evaluator
# ---------------------------------------------------------------------------

def evaluate(
    output: str,
    schema: dict,
    ground_truth: str = "",
    skill_type: str = "research",
) -> EvalResult:
    """
    Score skill output on 6 dimensions and return composite score.

    Args:
        output: The full text output from the skill execution
        schema: Expected output structure (sections, fields, word count)
        ground_truth: What a good answer would include (for semantic scoring)
        skill_type: One of "research", "execution", "infrastructure"

    Returns:
        EvalResult with composite score (0-100) and per-dimension breakdown
    """
    weights = SCORING_WEIGHTS.get(skill_type, SCORING_WEIGHTS["research"])
    dimensions = {}
    reasoning = {}

    # Heuristic dimensions
    dimensions["completeness"], reasoning["completeness"] = score_completeness(output, schema)
    dimensions["structure"], reasoning["structure"] = score_structure(output, schema)
    dimensions["confidence_calibration"], reasoning["confidence_calibration"] = (
        score_confidence_calibration(output, schema)
    )

    # Semantic dimensions (only if ground truth provided and weight > 0)
    semantic_dims = ["accuracy", "specificity", "actionability"]
    needs_judge = any(weights.get(d, 0) > 0 for d in semantic_dims)

    if needs_judge and ground_truth:
        client = anthropic.Anthropic(api_key=get_api_key())
        for dim in semantic_dims:
            if weights.get(dim, 0) > 0:
                dimensions[dim], reasoning[dim] = score_semantic_dimension(
                    output, dim, ground_truth, client
                )
            else:
                dimensions[dim] = 0.0
                reasoning[dim] = "weight=0, skipped"
    else:
        for dim in semantic_dims:
            dimensions[dim] = 50.0
            reasoning[dim] = "no ground truth provided, default score"

    # Compute weighted composite
    composite = sum(
        dimensions.get(dim, 0) * weight
        for dim, weight in weights.items()
    )

    return EvalResult(
        composite=round(composite, 2),
        dimensions={k: round(v, 2) for k, v in dimensions.items()},
        reasoning=reasoning,
        skill_type=skill_type,
    )
