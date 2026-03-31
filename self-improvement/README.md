# Self-Improvement: Agents That Get Smarter Over Time

This is Agent Forge's killer feature. Two systems work together to continuously improve your agents:

## The Two Systems

### autoimprove -- The Lab

Controlled optimization. Scores agent output on 6 dimensions, proposes targeted improvements, validates them, and commits or reverts. The git ratchet ensures quality only goes up.

**When it runs:** Scheduled. Weekly batch runs, weekend optimization sessions, or on-demand.

**How it works:**
1. Copy agent file to a git-tracked work directory
2. Run agent against test cases via Claude API
3. Score output on 6 dimensions (3 heuristic + 3 semantic)
4. Propose a modification via Claude API
5. Apply modification, re-run, re-score
6. If improved: git commit. If regressed: git reset.
7. Repeat until convergence or cost cap.

**The three-file contract:**
- Immutable evaluator (`evaluate.py`) -- never changes during a run
- Editable agent (`work/{agent}.md`) -- the one thing modified per iteration
- Human directive (`directives/{agent}.md`) -- tells the loop what to optimize for

[Full details in autoimprove/README.md](autoimprove/README.md)

### OpenSpace -- The Immune System

Continuous evolution from real usage. An MCP server that watches agent execution and auto-evolves agents when they fail or succeed in interesting ways.

**When it runs:** Always. Activates during normal work sessions.

**Evolution types:**
- **FIX** -- Repair a broken agent in-place. Triggered by failures.
- **DERIVED** -- Specialize or enhance an existing agent. Triggered by success patterns.
- **CAPTURED** -- Extract a novel reusable pattern. Triggered by novel approaches.

[Full details in openspace/README.md](openspace/README.md)

## When to Use What

| Score Range | Method | Why |
|-------------|--------|-----|
| **< 50** | OpenSpace fix (structural fix, one-shot) | Needs major repair |
| **50-75** | OpenSpace first, then autoimprove | Big jump + polish |
| **75-85** | autoimprove only (fine-tuning) | Iterative small gains |
| **> 85** | Leave alone | Risk of over-optimization |
| **Structural redesign** | Manual + validate with autoimprove | Cross-agent context needed |

## The Feedback Loop

```
Real work sessions
      |
      v
OpenSpace watches execution
      |
      +--> Agent breaks? --> FIX evolution (immediate)
      +--> Better approach found? --> DERIVED evolution
      +--> Novel pattern? --> CAPTURED as new skill
      +--> Usage metrics accumulate
              |
              v
      autoimprove uses metrics to prioritize
              |
              v
      Scheduled batch optimization
              |
              v
      Improved agents feed back into daily use
```

## Cost Model

| Activity | Cost | Frequency |
|----------|------|-----------|
| OpenSpace fix (manual) | ~$0.20/fix | On demand |
| OpenSpace real-time evolution | ~$0.20/evolution | Per failure |
| autoimprove per iteration | ~$0.19/iteration | Scheduled batches |
| autoimprove per agent (3 iterations) | ~$0.60/agent | Weekly |
| Full portfolio scoring scan | ~$3-5 | Monthly |

## Getting Started

1. Set up autoimprove first -- it's standalone Python, no MCP needed
2. Create test cases for your agents
3. Run a baseline score
4. Let the loop improve them
5. Add OpenSpace when you want continuous evolution

See [autoimprove/README.md](autoimprove/README.md) for setup instructions.
