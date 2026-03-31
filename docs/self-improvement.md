# Agent Self-Improvement Systems v1.0

Two complementary systems for making agents and skills better over time: one scheduled (The Lab), one continuous (The Immune System). Together, they create a feedback loop where agents improve from both controlled experiments and real-world usage.

---

## System 1: The Lab (Scheduled Optimization)

A controlled experiment runner. Scores agent/skill output, proposes targeted changes, validates improvements, commits winners, rolls back regressions. The git ratchet ensures quality only goes up.

### How It Works

1. Copy the agent/skill file to a git-tracked working directory.
2. Run the agent against test cases via API (using a mid-tier model like Sonnet).
3. Score output on 6 dimensions (mix of heuristic checks and LLM-as-judge).
4. Propose a targeted modification via API.
5. Apply modification, re-run, re-score.
6. If improved: git commit. If regressed: restore backup.
7. Repeat until convergence or cost cap.

### The Three-File Contract

This contract prevents runaway self-modification:

- **Immutable evaluator** -- The scoring logic never changes during a run. This is the anchor. If the evaluator could change, the system could game its own metrics.
- **Editable skill/agent** -- The one thing modified per iteration. Only the prompt text changes.
- **Human directive** -- A file that tells the loop what to optimize for. "Improve specificity of output" or "Reduce hallucination rate on competitor data." The human steers; the system executes.

### 6-Dimension Scoring

| Dimension | Method | Weight (default) |
|-----------|--------|-----------------|
| Completeness | Heuristic (section/field presence) | 0.25 |
| Accuracy | LLM judge | 0.30 |
| Structure | Heuristic (headers, lists, ordering) | 0.05 |
| Confidence Calibration | Heuristic (H/M/L distribution) | 0.10 |
| Actionability | LLM judge | 0.15 |
| Specificity | LLM judge | 0.15 |

Weights are configurable per agent type (research, execution, infrastructure). Adjust based on what matters most for each agent's output.

### The Git Ratchet Pattern

Every improvement is committed. Every regression is reverted. The git history becomes a one-way quality ratchet:

- `git diff` shows exactly what changed between versions
- `git log` shows the scoring trajectory
- `git revert` is always available as a safety net
- The best version is always the latest commit

This eliminates the fear of experimentation. You can try anything because the worst case is a revert.

### Adding a New Agent/Skill

1. Create test cases (JSON files with name, input prompt, expected output/ground truth)
2. Create a directive file (what to optimize for)
3. Configure scoring weights for the agent's type
4. Run the loop

---

## System 2: The Immune System (Continuous Evolution)

An always-on system that watches agent/skill execution during real work and evolves them based on actual performance. While The Lab runs experiments in isolation, The Immune System learns from production.

### How It Works

1. You use an agent/skill during normal work.
2. The system watches the full task trajectory (inputs, tool calls, outputs).
3. Based on results, it triggers one of three evolution types.
4. Over time, the agent library self-heals and self-expands without manual intervention.

### Three Evolution Types

**FIX** -- Repair a broken agent/skill in-place.
- Same file, updated content.
- Triggered by: execution failures, tool errors, consistently poor output.
- Example: A research agent that crashes when web search returns no results gets a graceful degradation path added.

**DERIVED** -- Specialize or enhance an existing agent/skill.
- Creates a new agent alongside the parent.
- Triggered by: success patterns that suggest a specialized variant would perform better.
- Example: A general "content writer" agent spawns a "LinkedIn post writer" variant after repeated LinkedIn-specific usage.

**CAPTURED** -- Extract a novel reusable pattern from a successful execution.
- Brand new agent/skill, no parent.
- Triggered by: novel approaches that solved a problem in an unexpected way.
- Example: During a debugging session, a novel error-diagnosis workflow emerges and gets captured as a reusable skill.

### Evolution Triggers

1. **Post-Execution Analysis** -- After every execution, analyze the trajectory and suggest evolutions.
2. **Tool Degradation** -- When a tool's success rate drops, dependent agents get batch-evolved to handle the degradation.
3. **Metric Monitor** -- Periodic scan of applied rate, completion rate, and fallback rate identifies agents trending downward.

---

## When to Use What

| Score Range | Method | Why |
|-------------|--------|-----|
| **Below 50** | Immune System (FIX) | Needs structural repair. One-shot, surgical, reliable. |
| **50-75** | Immune System first, then Lab | The big jump comes from structural fixes. Lab polishes after. |
| **75-85** | Lab only | Fine-tuning territory. Iterative small gains. |
| **Above 85** | Leave alone | Already good. Risk of over-optimization. |
| **Structural redesign** | Manual (human) | Cross-agent context, major instruction reframes. Validate with Lab scoring after. |

---

## The Feedback Loop

```
Real work sessions
      |
      v
Immune System watches execution
      |
      +--> Agent breaks?        --> FIX evolution (immediate)
      +--> Better approach?     --> DERIVED evolution
      +--> Novel pattern?       --> CAPTURED as new agent/skill
      +--> Usage metrics accumulate
              |
              v
      Lab uses metrics to prioritize
              |
              v
      Scheduled batch optimization
              |
              v
      Improved agents feed back into daily use
```

The Immune System generates real-world quality signals (completion rate, success rate, fallback rate). These signals tell The Lab which agents to prioritize for batch optimization. The Lab's scoring improvements raise the quality baseline that the Immune System defends.

---

## Cost Model

| Activity | Cost | Frequency |
|----------|------|-----------|
| Immune System fix (manual) | ~$0.20/fix | On demand |
| Immune System real-time evolution | ~$0.20/evolution | Per failure in production |
| Lab per iteration | ~$0.19/iteration | Scheduled batches |
| Lab per agent (3 iterations) | ~$0.60/agent | Weekly |
| Full portfolio scoring scan | ~$3-5 | Monthly |

Monthly steady-state estimate: $50-100 for continuous Immune System + $50-100 for weekly Lab batches. Scale depends on portfolio size.

---

## Monthly Cadence

**Week 1:** Re-score all prioritized agents. Identify regressions from the previous month.

**Week 2:** Run Immune System FIX on anything that dropped below threshold.

**Week 3:** Run Lab batch optimization on high-priority agents.

**Week 4:** Review results, merge winners, archive non-performers. Update prioritization tiers.

### Prioritization Tiers

| Tier | Agents | Optimization Budget |
|------|--------|-------------------|
| **Tier 1: Must Improve** | Daily-use, high-impact agents | Full Lab + Immune System attention |
| **Tier 2: Should Improve** | Weekly-use, moderate-impact agents | Lab batches when budget allows |
| **Tier 3: On-Demand** | Infrequent use | Let Immune System handle reactively |
| **Tier 4: Skip** | Rarely used, deprecated, or redundant | Don't spend API budget. Archive or remove. |

---

## Getting Started

1. **Score your agents first.** Before optimizing anything, establish a baseline score for every agent. You can't improve what you can't measure.
2. **Set up test cases.** Each agent needs at least 3 test cases with input prompts and expected outputs. More is better, but 3 is the minimum.
3. **Write directives.** For each agent you want to optimize, write a one-paragraph directive explaining what "better" means for this specific agent.
4. **Run the Lab on your weakest agent.** Start with the lowest-scoring agent and work up. The biggest gains come from fixing the worst performers.
5. **Deploy the Immune System.** Once your agents are above baseline, let the Immune System maintain quality while you focus on new agents.

---

*These systems are complementary, not competitive. The Immune System keeps agents healthy in production. The Lab pushes them to the next level in controlled conditions. Together, they create agents that get better the more you use them.*
