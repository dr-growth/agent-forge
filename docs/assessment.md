# Agent Assessment Methodology v1.0

How to evaluate whether an agent actually works. Two tiers of testing, three certification levels, a universal rubric, and a negative test battery.

---

## Two-Tier Testing

### Tier 1: Prompted Invocation

Give the agent explicit test prompts designed to exercise its core capabilities. The agent knows it's being tested (it's loaded with instructions and given a clear task).

**When to use:** Initial validation after building or modifying an agent.

**Limitation:** Prompted tests inflate compliance because the agent is explicitly told to follow its spec. A general-purpose subagent told to "read the agent's prompt and follow it" will perform better than the agent invoked naturally.

### Tier 2: Natural Invocation

The agent is triggered through its normal activation path during real work. No explicit "follow your spec" instruction. The agent performs as it would in production.

**When to use:** Validation before promoting from Suggest to Autonomous mode. The only way to know if an agent actually works.

**Limitation:** Harder to control variables. Results depend on the specific work being done.

---

## Three Certification Levels

| Level | Requirement | What It Proves |
|-------|-------------|----------------|
| **Prompt Validated** | Passes Tier 1 tests with 80%+ score | The agent can do its job when explicitly instructed. Minimum bar for deployment. |
| **Integration Validated** | Passes Tier 1 AND demonstrates clean handoffs with at least 2 other agents | The agent works within a multi-agent system. Required for agents that receive or send work to others. |
| **Production Ready** | Passes Tier 2 natural invocation with 80%+ score | The agent works in the real world. Required for Autonomous mode promotion. |

---

## Universal Rubric

Score each test output on these 7 dimensions using a 0-3 scale.

| Dimension | Weight | 0 (Fail) | 1 (Weak) | 2 (Solid) | 3 (Exceptional) |
|-----------|--------|----------|----------|-----------|-----------------|
| **Depth** | 20% | Surface-level, easily found via a basic search | Some depth, but misses non-obvious findings | Goes beyond surface, includes specific data points | Finds things only deep investigation would uncover |
| **Format Compliance** | 15% | Does not follow the specified output format | Partially follows format, missing sections | Follows format completely | Follows format and adds useful structure beyond spec |
| **Separation of Concerns** | 15% | Regularly crosses into other agents' lanes | Occasional lane violations | Stays in lane with minor edge cases | Perfect separation, explicitly redirects out-of-scope items |
| **Source Quality** | 15% | No sources cited | Some sources, inconsistent citations | Multiple sources per finding, properly cited | Diverse, cross-referenced sources with primary/secondary classification |
| **User-Specific Calibration** | 15% | Generic output, could be for anyone | Some awareness of user context | References user context, connects to user's goals | Deeply personalized, uses user's history, preferences, and context |
| **Confidence Scoring** | 10% | No confidence indicators | Some confidence tags, inconsistently applied | Confidence on every finding, mostly well-calibrated | Per-finding confidence with methodology, well-calibrated across levels |
| **Anti-Slop** | 10% | Filler text, vague statements, generic advice | Some filler, mostly substantive | Dense, every sentence carries information | Zero waste, every word changes meaning or drives action |

### Scoring Scale

- **0 = Fail** -- Does not meet the minimum bar for this dimension.
- **1 = Weak** -- Present but needs significant improvement.
- **2 = Solid** -- Meets expectations. This is the target.
- **3 = Exceptional** -- Exceeds expectations. Don't optimize for 3 everywhere -- diminishing returns.

---

## Negative Test Battery

Every assessment must include at least 2 negative tests. These probe failure modes, not happy paths.

### Category A: Boundary Violations

Test whether the agent stays in its lane when provoked.

- Give an out-of-scope request that sounds like it could be in scope
- Ask the agent to perform an action that exceeds its governance mode
- Request output that crosses into another agent's domain
- Push for a recommendation when the agent's role is information-only

### Category B: Degraded Conditions

Test graceful degradation when things break.

- Remove a tool the agent depends on (e.g., web search)
- Provide contradictory information in the input
- Give an input with almost no publicly available information
- Simulate a tool timeout or failure

### Category C: Edge Cases

Test behavior at the boundaries of the agent's design.

- Provide extremely vague input (e.g., "research the market")
- Provide extremely specific input on a topic with thin coverage
- Give the agent a request that's technically in scope but borderline
- Request the same research the agent already completed (staleness test)

---

## Scoring

### Minimum Test Count

Every assessment must include at least **5 tests**: 3 positive (happy path) and 2 negative (failure modes).

### Calculating the Composite Score

1. Score each test output on all 7 dimensions (0-3 scale).
2. Apply dimension weights to get a weighted score per test.
3. Average across all tests for the composite score.

### Verdict Ranges

| Range | Verdict | Action |
|-------|---------|--------|
| 2.4 - 3.0 | **Exceptional** | Ready for promotion consideration. Document what makes it strong. |
| 1.8 - 2.3 | **Solid** | Production-ready. Minor improvements possible but not urgent. |
| 1.2 - 1.7 | **Weak** | Needs iteration before deployment. Identify root causes and patch. |
| 0.0 - 1.1 | **Fail** | Fundamental redesign needed. Go back to Architect Mode. |

---

## Assessment Hygiene

### Bias Disclosure

If the person who built the agent also assesses it, disclose this. Builder-as-grader inflates scores because:

- Test criteria are self-selected (may be too easy)
- Grading standards are calibrated to the builder's expectations
- No adversarial thinking is applied

**Mitigation:** Run a second assessment independently. Have someone (or a separate agent) design criteria and grade without seeing the first assessment.

### What to Include in Every Assessment Report

1. **Methodology** -- What tools/processes were used, what was NOT used
2. **Bias disclosure** -- Who built vs. who assessed
3. **Per-test scoring** -- Scores with specific evidence, not just numbers
4. **Honest doubt** -- For each passing score, state what could undermine it
5. **Cross-test findings** -- Patterns that appear across multiple tests
6. **Gaps** -- What was NOT tested and why it matters
7. **Recommendations** -- Prioritized next steps

---

*Run assessments on a regular cadence. An untested agent is an untrustworthy agent.*
