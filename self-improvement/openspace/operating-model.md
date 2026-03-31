# Agent Evolution Operating Model

How agents improve themselves through OpenSpace (continuous) and autoimprove (scheduled).

## The Two Systems

### OpenSpace -- The Immune System

**What:** MCP server running alongside Claude Code. Watches agent execution, evolves agents from real usage.

**When it runs:** Always. It's an MCP server that activates during normal Claude Code sessions.

**How it works:**
1. You use an agent during normal work
2. OpenSpace's execution analyzer watches the full task trajectory
3. If an agent fails or underperforms, OpenSpace diagnoses why and triggers a FIX evolution
4. If an agent works well and reveals a pattern, OpenSpace spawns a DERIVED variant or CAPTURES a new agent
5. Over time, the agent library self-heals and self-expands without manual intervention

**Evolution types:**
- **FIX** -- Repair a broken agent in-place. Same directory, updated content. Triggered by failures.
- **DERIVED** -- Specialize or enhance an existing agent. Creates a new agent alongside the parent. Triggered by success patterns.
- **CAPTURED** -- Extract a novel reusable pattern from a successful execution. Brand new agent. Triggered by novel approaches.

### autoimprove -- The Lab

**What:** Controlled experiment runner. Scores agent output, proposes changes, validates improvements, commits or reverts.

**When it runs:** Scheduled. Weekly batch runs, weekend optimization sessions, or on-demand when targeting a specific agent.

**How it works:**
1. Queue agents for optimization
2. autoimprove copies the agent to a git-tracked work directory
3. Runs the agent against test cases via Claude API
4. Scores output on 6 dimensions (heuristic + Claude as judge)
5. Proposes a modification via Claude API
6. Applies modification, re-runs, re-scores
7. If improved: git commit. If regressed: restore backup.
8. Repeats until convergence or cost cap.

**The three-file contract:**
- Immutable evaluator (evaluate.py) -- never changes during a run
- Editable agent (work/{agent}.md) -- the one thing modified per iteration
- Human directive (directives/{agent}.md) -- tells the loop what to optimize for

## When to Use What

| Score Range | Method | Why |
|-------------|--------|-----|
| **< 50** | OpenSpace fix_skill | Needs structural fix. One-shot, surgical, reliable. |
| **50-75** | OpenSpace first, then autoimprove for stragglers | OpenSpace handles the big jump, autoimprove polishes. |
| **75-85** | autoimprove only | Fine-tuning territory. Iterative small gains. |
| **> 85** | Leave alone | Already good. Risk of over-optimization. |
| **Structural redesign** | Manual (Claude Code) | Cross-agent context, major instruction reframes. Validate with autoimprove scoring after. |

## The Feedback Loop

```
Real work sessions
      |
      v
OpenSpace watches execution
      |
      +--> Agent breaks? --> FIX evolution (immediate)
      +--> Better approach found? --> DERIVED evolution
      +--> Novel pattern? --> CAPTURED as new agent
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

OpenSpace generates real-world quality signals (completion rate, applied rate, fallback rate). These signals tell autoimprove which agents to prioritize for scheduled optimization. autoimprove's scoring improvements raise the quality baseline that OpenSpace defends.

## Cost Model

| Activity | Cost | Frequency |
|----------|------|-----------|
| OpenSpace fix (manual) | ~$0.20/fix | On demand |
| OpenSpace real-time evolution | ~$0.20/evolution | Per failure in production |
| autoimprove per iteration | ~$0.19/iteration | Scheduled batches |
| autoimprove per agent (3 iterations) | ~$0.60/agent | Weekly |
| Full portfolio scoring scan | ~$3-5 | Monthly |

Monthly steady-state estimate: $50-100 for continuous OpenSpace + $50-100 for weekly autoimprove batches.

## Prioritization Tiers

### Tier 1: MUST IMPROVE (daily use, high impact)
Agents used every day in operational workflows. Failures here directly impact your work output.

### Tier 2: SHOULD IMPROVE (weekly use, moderate impact)
Agents used regularly for content, research, and building. Quality improvements compound across multiple sessions per week.

### Tier 3: ON-DEMAND (improve when used)
Let OpenSpace handle these reactively. When an agent fails in real use, OpenSpace fixes it. No proactive investment needed.

### Tier 4: SKIP (rarely used, deprecated, or redundant)
Don't spend API budget on these. Archive or remove redundant ones.

## Monthly Cadence

**Week 1:** Re-score all prioritized agents. Identify regressions.
**Week 2:** OpenSpace fix on anything that dropped below threshold.
**Week 3:** autoimprove batch on Tier 1 and 2 agents.
**Week 4:** Review, merge winners, archive non-performers. Update prioritization.
