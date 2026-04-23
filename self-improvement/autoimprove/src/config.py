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
SKILLS_DIR = Path.home() / ".claude" / "agents"
TEST_CASES_DIR = PROJECT_ROOT / "test-cases"
DIRECTIVES_DIR = PROJECT_ROOT / "directives"
RESULTS_DIR = PROJECT_ROOT / "results"
EXPERIMENTS_LOG = RESULTS_DIR / "experiments.jsonl"

# ---------------------------------------------------------------------------
# API Configuration
# ---------------------------------------------------------------------------

def get_api_key() -> str:
    """Retrieve ANTHROPIC_API_KEY from env, .env file, or macOS keychain."""
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

    # 3. macOS keychain
    try:
        key = subprocess.run(
            ["security", "find-generic-password", "-s", "anthropic", "-w"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if key:
            return key
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    raise RuntimeError(
        "ANTHROPIC_API_KEY not found. Set it via:\n"
        "  1. export ANTHROPIC_API_KEY=sk-...\n"
        "  2. echo 'ANTHROPIC_API_KEY=sk-...' > ~/pai-os/projects/autoimprove/.env\n"
    )


# Model for running skills (the thing being tested)
RUNNER_MODEL = "claude-sonnet-4-20250514"

# Model for proposing improvements to skill files
PROPOSER_MODEL = "claude-sonnet-4-20250514"

# Model for semantic scoring dimensions (quality over cost -- the judge IS the ceiling)
JUDGE_MODEL = "claude-sonnet-4-20250514"

# Max tokens for skill execution
RUNNER_MAX_TOKENS = 4096

# Max tokens for improvement proposals
PROPOSER_MAX_TOKENS = 2048

# Max tokens for judge evaluations
JUDGE_MAX_TOKENS = 1024

# ---------------------------------------------------------------------------
# Scoring Weights by Skill Type
# ---------------------------------------------------------------------------

# Each skill type has different weight distributions across the 6 dimensions.
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

# Skill -> type mapping (add entries as you onboard skills)
SKILL_TYPES = {
    "scout": "research",
    "chief-of-staff": "execution",
    "build-in-public": "execution",
    "account-researcher": "research",
    "competitor-scan": "research",
    "signal-crafter": "execution",
    "eval-harness": "infrastructure",
    "iterative-retrieval": "infrastructure",
    "scaffolding-projects": "infrastructure",
    "linkedin-posting": "execution",
    "close-chat": "infrastructure",
}

# ---------------------------------------------------------------------------
# v2 Configuration — three-signal evaluator with behavioral gate
# ---------------------------------------------------------------------------

# Rubric judge: Opus (procedural criteria, harder to game, external standard)
V2_RUBRIC_JUDGE_MODEL = "claude-opus-4-7"
V2_RUBRIC_JUDGE_MAX_TOKENS = 2048

# Behavioral gate: fraction of assertions that must pass for a run to count.
# Below threshold → iteration is rejected regardless of other signals.
V2_BEHAVIORAL_GATE_THRESHOLD = 0.80

# Composite score weighting (used ONLY when the behavioral gate passes)
V2_COMPOSITE_WEIGHTS = {
    "rubric": 0.60,   # Opus grading against Anthropic's building-skills doc
    "prose": 0.40,    # v1 Haiku prose score, retained for continuity
}

# Cost cap for v2 runs (Opus is pricier than v1 stack)
V2_COST_CAP_PER_RUN = 10.0

# Path to the authoritative skill-authoring rubric source
V2_RUBRIC_SOURCE = Path.home() / ".claude" / "skills" / "building-skills" / "SKILL.md"

# ---------------------------------------------------------------------------
# Loop Configuration
# ---------------------------------------------------------------------------

# Stop loop when score improvement is below this for N consecutive runs
CONVERGENCE_THRESHOLD = 0.5
CONVERGENCE_RUNS = 3

# Hard cost cap per loop run (USD)
# Set low for initial testing. Increase once evaluator is calibrated.
COST_CAP_PER_RUN = 5.0

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
