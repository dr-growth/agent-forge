"""
Configuration for autoimprove.

Scoring weights, model settings, thresholds, paths.
"""

import os
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_DIR = Path(os.environ.get("AGENTS_DIR", str(Path.home() / ".claude" / "agents")))
TEST_CASES_DIR = PROJECT_ROOT / "test-cases"
DIRECTIVES_DIR = PROJECT_ROOT / "directives"
RESULTS_DIR = PROJECT_ROOT / "results"
EXPERIMENTS_LOG = RESULTS_DIR / "experiments.jsonl"

# ---------------------------------------------------------------------------
# API Configuration
# ---------------------------------------------------------------------------

def get_api_key() -> str:
    """Retrieve ANTHROPIC_API_KEY from env or .env file."""
    # 1. Environment variable
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key

    # 2. .env file in project root
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key

    raise RuntimeError(
        "ANTHROPIC_API_KEY not found. Set it via:\n"
        "  1. export ANTHROPIC_API_KEY=sk-...\n"
        "  2. echo 'ANTHROPIC_API_KEY=sk-...' > .env\n"
    )


# Model for running agents (the thing being tested)
RUNNER_MODEL = os.environ.get("RUNNER_MODEL", "claude-sonnet-4-20250514")

# Model for proposing improvements to agent files
PROPOSER_MODEL = os.environ.get("PROPOSER_MODEL", "claude-sonnet-4-20250514")

# Model for semantic scoring dimensions
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-sonnet-4-20250514")

# Max tokens for agent execution
RUNNER_MAX_TOKENS = int(os.environ.get("RUNNER_MAX_TOKENS", "4096"))

# Max tokens for improvement proposals
PROPOSER_MAX_TOKENS = int(os.environ.get("PROPOSER_MAX_TOKENS", "2048"))

# Max tokens for judge evaluations
JUDGE_MAX_TOKENS = int(os.environ.get("JUDGE_MAX_TOKENS", "1024"))

# ---------------------------------------------------------------------------
# Scoring Weights by Agent Type
# ---------------------------------------------------------------------------

# Each agent type has different weight distributions across the 6 dimensions.
# Weights must sum to 1.0.

SCORING_WEIGHTS = {
    "research": {
        "completeness": 0.25,
        "accuracy": 0.30,
        "structure": 0.05,
        "confidence_calibration": 0.10,
        "actionability": 0.15,
        "specificity": 0.15,
    },
    "execution": {
        "completeness": 0.15,
        "accuracy": 0.10,
        "structure": 0.20,
        "confidence_calibration": 0.05,
        "actionability": 0.30,
        "specificity": 0.20,
    },
    "infrastructure": {
        "completeness": 0.30,
        "accuracy": 0.20,
        "structure": 0.35,
        "confidence_calibration": 0.00,
        "actionability": 0.15,
        "specificity": 0.00,
    },
}

# Agent -> type mapping (add entries as you onboard agents)
SKILL_TYPES: dict[str, str] = {
    # Example entries:
    # "researcher": "research",
    # "coordinator": "execution",
    # "strategist": "research",
}

# ---------------------------------------------------------------------------
# Loop Configuration
# ---------------------------------------------------------------------------

# Stop loop when score improvement is below this for N consecutive runs
CONVERGENCE_THRESHOLD = float(os.environ.get("CONVERGENCE_THRESHOLD", "0.5"))
CONVERGENCE_RUNS = int(os.environ.get("CONVERGENCE_RUNS", "3"))

# Hard cost cap per loop run (USD)
COST_CAP_PER_RUN = float(os.environ.get("COST_CAP_PER_RUN", "5.0"))

# Approximate cost tracking (USD per 1M tokens)
COST_PER_1M_INPUT = {
    RUNNER_MODEL: 3.00,
    PROPOSER_MODEL: 3.00,
    JUDGE_MODEL: 3.00,
}
COST_PER_1M_OUTPUT = {
    RUNNER_MODEL: 15.00,
    PROPOSER_MODEL: 15.00,
    JUDGE_MODEL: 15.00,
}
