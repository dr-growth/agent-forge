# Proven Patterns Library v1.0

Patterns that consistently produce better agent output. Every entry is grounded in either repeated empirical success across agent portfolios or published research. This is a living document -- add patterns as you validate them.

---

## Prompting Patterns

### P-001: Lead with Role, Then Scope, Then Rules

**What:** Structure agent prompts in this order: (1) who you are, (2) what you do and don't do, (3) how you do it.

**Why:** Models attend more strongly to early context. Putting identity and scope first anchors all downstream behavior.

**Source:** Empirical -- consistent across portfolios. Supported by Anthropic prompt engineering guidance.

### P-002: Negative Examples Outperform Positive-Only

**What:** Including examples of what NOT to do (and why) produces sharper adherence to desired behavior than positive examples alone.

**Why:** Negative examples define boundaries. Models often drift toward generic "good" behavior without them.

**Source:** Empirical -- observed in agent iteration cycles across multiple domains.

### P-003: Decision Logic as If/Then, Not Principles

**What:** Convert abstract operating principles into concrete if/then rules. Instead of "Be pragmatic," write "If the user presents an idea that requires more than 3 tools to implement, flag complexity and suggest a simpler alternative first."

**Why:** Abstract principles don't reliably change model behavior. Conditional logic does.

**Source:** Empirical -- Bloat Test results across multiple audits.

### P-004: One Agent, One Job

**What:** Each agent should have a single, clearly defined function. If an agent is doing two distinct jobs, split it.

**Why:** Multi-purpose agents produce mediocre results across all functions. Single-purpose agents excel at their one thing.

**Source:** Observed during orchestration refactors (14 agents -> 3 focused agents improved output quality).

### P-005: Explicit Uncertainty Handling

**What:** Always include explicit instructions for what the agent should do when it's unsure -- ask, flag, or degrade gracefully. Never leave this implicit.

**Why:** Without explicit uncertainty handling, models default to confident-sounding hallucination.

**Source:** Universal observation. Supported by multiple research papers on LLM calibration.

### P-006: Forced-Answer Final Iteration

**What:** When an agent runs in an iterative loop (retry cycles, multi-step reasoning, tool-calling chains), instruct the orchestrator to remove all tool access on the final permitted iteration, forcing the model to synthesize what it has and produce a text answer.

**Why:** Without an explicit escape valve, agents can enter infinite loops where they keep calling tools that keep failing. Stripping tools on the last iteration guarantees a deterministic exit with a synthesized response rather than a hang or timeout.

**Source:** Dify open-source platform. Implemented in their Agent Node execution engine as a production safety mechanism across Fortune 500 deployments.

---

## Structural Patterns

### S-001: Tool Justification Requirement

**What:** Every tool in the manifest must have a one-line justification. If you can't justify it, remove it.

**Why:** Unnecessary tool access increases error surface and token cost. Models sometimes use tools when they shouldn't if the tools are available.

**Source:** Empirical -- observed over-reliance on web search when it was listed but not justified.

### S-002: Version + Changelog in Every Prompt

**What:** Include a version number and changelog directly in the agent file. Not in a separate doc -- in the prompt itself.

**Why:** When iterating quickly, you lose track of what changed and when. In-prompt versioning creates accountability.

**Source:** Process learning from portfolio management.

### S-003: Escalation Triggers as a Numbered List

**What:** List the specific conditions under which the agent must stop and ask the user, as a numbered list near the top of the prompt.

**Why:** Buried escalation logic gets ignored. A prominent numbered list gets followed.

**Source:** Empirical -- iteration mode findings.

---

## Process Patterns

### PR-001: Audit Before Iterate

**What:** Never jump straight to fixing an agent based on a single complaint. Run a full audit first.

**Why:** The reported problem is often a symptom of a deeper structural issue. Patching symptoms creates prompt bloat.

**Source:** Lifecycle engine experience -- repeated across multiple agent improvement cycles.

### PR-002: One Change Per Iteration Cycle

**What:** When iterating, make one structural change at a time. Test it. Then make the next.

**Why:** Multiple simultaneous changes make it impossible to attribute improvement or regression.

**Source:** Standard experimental methodology, applied to prompt engineering.

---

*Add new patterns as you validate them. Each pattern must include a source before being added.*
