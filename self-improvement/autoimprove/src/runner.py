"""
Agent execution harness.

Loads an agent .md file as a system prompt, executes it against
a test case via Claude API, and captures the full output + metadata.

The runner is READ-ONLY with respect to the agent file. It never modifies it.

Usage:
    from src.runner import run_skill
    result = run_skill("researcher", test_case)
    print(result.output)
    print(result.tokens_in, result.tokens_out)
"""

import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

import anthropic

from .config import (
    get_api_key,
    RUNNER_MODEL,
    RUNNER_MAX_TOKENS,
    AGENTS_DIR,
    COST_PER_1M_INPUT,
    COST_PER_1M_OUTPUT,
)


@dataclass
class TestCase:
    """A test case for agent execution."""
    name: str
    input_prompt: str
    ground_truth: str  # What a good answer includes (for evaluator)
    schema: dict = field(default_factory=dict)  # Expected output structure

    @classmethod
    def from_file(cls, path: Path) -> "TestCase":
        """Load a test case from a JSON file."""
        import json
        data = json.loads(path.read_text())
        return cls(**data)


@dataclass
class RunResult:
    """Result of a single agent execution."""
    output: str
    tokens_in: int
    tokens_out: int
    latency_seconds: float
    cost_usd: float
    model: str
    skill_name: str
    test_case_name: str

    def to_dict(self) -> dict:
        return asdict(self)


def load_skill(skill_name: str, skill_path: Path | None = None) -> str:
    """Load an agent .md file as a string."""
    if skill_path:
        path = skill_path
    else:
        path = AGENTS_DIR / f"{skill_name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Agent file not found: {path}")
    return path.read_text()


def run_skill(
    skill_name: str,
    test_case: TestCase,
    skill_path: Path | None = None,
) -> RunResult:
    """
    Execute an agent against a test case via Claude API.

    The agent .md content becomes the system prompt.
    The test case input becomes the user message.

    If skill_path is provided, reads from that path instead of the default.
    """
    skill_content = load_skill(skill_name, skill_path)
    client = anthropic.Anthropic(api_key=get_api_key())

    t0 = time.time()
    response = client.messages.create(
        model=RUNNER_MODEL,
        max_tokens=RUNNER_MAX_TOKENS,
        system=skill_content,
        messages=[{"role": "user", "content": test_case.input_prompt}],
    )
    latency = time.time() - t0

    output = response.content[0].text
    tokens_in = response.usage.input_tokens
    tokens_out = response.usage.output_tokens

    cost = (
        (tokens_in / 1_000_000) * COST_PER_1M_INPUT.get(RUNNER_MODEL, 3.0)
        + (tokens_out / 1_000_000) * COST_PER_1M_OUTPUT.get(RUNNER_MODEL, 15.0)
    )

    return RunResult(
        output=output,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        latency_seconds=round(latency, 2),
        cost_usd=round(cost, 4),
        model=RUNNER_MODEL,
        skill_name=skill_name,
        test_case_name=test_case.name,
    )


def run_skill_on_cases(
    skill_name: str,
    test_cases: list[TestCase],
    skill_path: Path | None = None,
) -> list[RunResult]:
    """Run an agent against multiple test cases."""
    return [run_skill(skill_name, tc, skill_path) for tc in test_cases]
