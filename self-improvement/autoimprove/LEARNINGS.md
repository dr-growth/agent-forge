# What We Learned From Studying autoresearch

## The Core Pattern

Karpathy's autoresearch is deceptively simple. There is no loop engine in Python. The loop IS the AI agent following `program.md` instructions. The three files are:

1. **prepare.py** (immutable) -- data loading + `evaluate_bpb()` function. Returns a single scalar metric. Never modified during runs.
2. **train.py** (editable) -- the one file the agent modifies. Contains model architecture, optimizer, training loop. Everything is fair game.
3. **program.md** (human directive) -- tells the agent what to optimize and how to run the loop. The agent executes this instruction set autonomously.

## What We're Taking

| autoresearch Pattern | autoimprove Adaptation |
|---|---|
| Immutable evaluator (`prepare.py`) | `evaluate.py` -- scores skill output, not ML metrics. Immutable during runs. |
| Single editable file (`train.py`) | The skill `.md` file -- the one thing that gets modified per improvement run. |
| Human directive (`program.md`) | `directives/*.md` -- improvement goals per skill. |
| Single scalar metric (`val_bpb`) | Composite quality score (weighted 6-dimension average). |
| Git ratchet (commit on improve, reset on regress) | Same mechanism, on a per-skill branch. |
| `results.tsv` experiment log | `results/experiments.jsonl` -- richer structured logging. |
| "NEVER STOP" autonomous loop | Python `loop.py` orchestrating via Claude API (not interactive agent). |
| Fixed time budget (5 min per run) | No time budget -- cost budget instead ($50 cap per loop). |

## What We're Adapting

**The loop mechanism itself.** Karpathy's loop lives in the agent's conversation context -- the agent reads program.md and iterates. We can't do this because:
- Our "runs" are Claude API calls, not GPU training runs
- We need programmatic control over the propose-test-score-commit cycle
- We want to run unattended (background Python process, not interactive Claude Code session)

So `loop.py` replaces the agent-as-loop with a Python orchestrator that:
1. Reads the skill file
2. Calls `runner.py` to execute the skill against test cases
3. Calls `evaluate.py` to score the output
4. Calls Claude API to propose a modification
5. Applies the modification
6. Re-runs, re-scores
7. Commits or resets via git

**The evaluator.** Karpathy has `val_bpb` -- a clean, deterministic, numeric metric computed from model output. We have prose. Our evaluator is a hybrid:
- Structural dimensions (completeness, structure, confidence calibration): heuristic checks
- Semantic dimensions (accuracy, specificity, actionability): Claude Haiku as judge

The aggregation (weighted average) is deterministic. The Haiku scoring adds mild non-determinism, accepted as the cost of evaluating natural language.

## What Doesn't Apply

- GPU/VRAM constraints (we're API-only)
- Compilation and warmup time
- The specific "simplicity criterion" for code changes (our skills are markdown, not Python)
- Platform support concerns (we're macOS + Claude API)

## Key Insight

The genius of autoresearch is the constraint system: one file to modify, one metric to optimize, immutable evaluation. This prevents the optimization from gaming its own measurement. We preserve these constraints exactly. The rest is just plumbing adapted for skill files instead of ML code.
