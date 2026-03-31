# autoimprove -- Autonomous Agent Improvement Engine

Adapted from Karpathy's autoresearch pattern. Proposes changes to agent files, evaluates output quality, commits improvements, rolls back regressions. The git ratchet ensures quality only goes up.

## Quick Start

```bash
# 1. Install dependencies
cd agent-forge/self-improvement/autoimprove
pip install anthropic

# 2. Set your API key
export ANTHROPIC_API_KEY=sk-...

# 3. Create test cases for your agent
mkdir -p test-cases/my-agent
# See templates/test-case-template.json for format

# 4. Run the improvement loop
python -m src.loop --skill my-agent --max-iterations 5
```

## How It Works

```
                    +-----------+
                    | Read agent|
                    | .md file  |
                    +-----+-----+
                          |
                    +-----v-----+
                    | Run against|
                    | test cases |
                    +-----+-----+
                          |
                    +-----v-----+
                    | Score on 6 |
                    | dimensions |
                    +-----+-----+
                          |
                    +-----v-----+
                    | Propose    |
                    | modification|
                    +-----+-----+
                          |
                    +-----v-----+
                    | Apply &    |
                    | re-score   |
                    +-----+-----+
                          |
                   +------+------+
                   |             |
              Improved?    Regressed?
                   |             |
              git commit    git reset
                   |             |
                   +------+------+
                          |
                     Next iteration
```

## The Three-File Contract

This is the core design principle. During any improvement run, exactly three things matter:

1. **Immutable evaluator** (`src/evaluate.py`) -- The scoring engine. Never changes during a run. This is the fixed reference point that prevents circular optimization.

2. **Editable agent** (`work/{agent}.md`) -- The agent file being improved. This is the ONLY thing the loop modifies. A copy of the original, tracked in git.

3. **Human directive** (`directives/{agent}.md`) -- Your instructions to the loop. What to optimize for, what constraints to respect. The human stays in control of the direction.

## Scoring Dimensions

| Dimension | Method | Default Weight (Research) |
|-----------|--------|--------------------------|
| Completeness | Heuristic (section/field presence) | 0.25 |
| Accuracy | Claude as judge | 0.30 |
| Structure | Heuristic (headers, lists, ordering) | 0.05 |
| Confidence Calibration | Heuristic (H/M/L distribution) | 0.10 |
| Actionability | Claude as judge | 0.15 |
| Specificity | Claude as judge | 0.15 |

Weights are configurable per agent type in `src/config.py`:
- **Research agents:** Heavy on accuracy and completeness
- **Execution agents:** Heavy on actionability and structure
- **Infrastructure agents:** Heavy on completeness and structure

## Cost

- Per iteration: ~$0.19
- Cost cap: $5 per run (configurable)
- ~25 iterations per $5 cap

## Adding a New Agent

1. Create test cases in `test-cases/{agent-name}/` (JSON files)
2. Create a directive in `directives/{agent-name}.md`
3. Add agent to `SKILL_TYPES` in `src/config.py`
4. Run: `python -m src.loop --skill {agent-name}`

## Test Case Format

```json
{
  "name": "basic-research-task",
  "input_prompt": "Research the competitive landscape for cloud data warehousing",
  "ground_truth": "Should include: market size data, key players (Snowflake, Databricks, BigQuery), recent funding rounds, competitive positioning",
  "schema": {
    "required_sections": ["## Summary", "## Key Players", "## Analysis"],
    "required_fields": ["confidence:", "sources:"],
    "min_word_count": 500
  }
}
```

## Promoting Improvements

After a successful run, the improved agent is at `work/{agent}.md`. To promote:

```bash
# Review the diff first
diff work/my-agent.md ~/.claude/agents/my-agent.md

# If satisfied, promote
cp work/my-agent.md ~/.claude/agents/my-agent.md
```

The loop modifies instruction text, output format guidance, and examples. It does NOT touch governance, model assignment, or scope boundaries.

## Key Files

| File | Purpose |
|------|---------|
| `src/loop.py` | Main improvement loop |
| `src/runner.py` | Execute agent against test cases via Claude API |
| `src/evaluate.py` | 6-dimension scoring engine |
| `src/config.py` | Weights, models, thresholds, cost caps |
| `test-cases/{agent}/` | Test inputs + ground truth per agent |
| `directives/{agent}.md` | Improvement goals per agent |
| `results/experiments.jsonl` | Full experiment log |
| `work/{agent}.md` | Working copy being improved |
