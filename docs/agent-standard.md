# Agent Standard v1.0

Every agent must meet these 9 non-negotiable requirements before deployment. No exceptions. During audits, every agent is evaluated against these criteria.

---

## The Nine Requirements

### 1. Mission Statement

One sentence that defines why this agent exists. Must answer: "What outcome does this agent produce that wouldn't happen without it?"

If you can't state the mission in one sentence, the agent's scope is too broad.

**Test:** Remove the mission statement and read the rest of the prompt. If the agent could be about anything, the mission is too vague.

### 2. Defined Scope

- **What it handles** -- an explicit list of responsibilities.
- **What it does NOT handle** -- an explicit exclusion list.
- **Handoff rules** -- if something is out of scope, where does it go?

**Test:** Give the agent an out-of-scope request. Does the prompt give it enough information to refuse or redirect cleanly?

### 3. Input/Output Contract

- **Triggers** -- What inputs activate this agent? (user message, scheduled event, data change, another agent's output)
- **Outputs** -- What does this agent produce? (analysis, recommendation, draft, action, decision)
- **Format** -- What structure should outputs follow? (prose, structured doc, JSON, specific template)

**Test:** Can someone who has never seen this agent predict what it will produce from a given input?

### 4. Tool Manifest

- **What tools does this agent have access to?** (web search, file system, APIs, MCP servers, databases)
- **Why does it need each tool?** (no tool access without justification)
- **Tool usage rules** -- When should it use each tool vs. rely on its own knowledge?

**Test:** Remove a tool from the list. Does the agent's capability meaningfully degrade? If not, it didn't need that tool.

### 5. Decision Logic

- **Autonomous actions** -- What can the agent do without asking?
- **Escalation triggers** -- When must it stop and ask the user?
- **Ambiguity protocol** -- What does it do when the input is unclear or conflicting?
- **Confidence thresholds** -- How certain must it be before acting vs. flagging uncertainty?

**Test:** Give the agent an ambiguous input. Does the prompt tell it exactly what to do?

### 6. Failure Protocol

- **What happens when it doesn't know?** (admit it, search, escalate -- not hallucinate)
- **What happens when it gets conflicting information?**
- **What happens when a tool fails or is unavailable?**
- **Graceful degradation** -- Can it still provide value in a reduced capacity?

**Test:** Deliberately break something (remove a tool, give contradictory input). Does the prompt handle it?

### 7. Success Criteria

- **Measurable indicators** that this agent is performing well.
- Must include at least one **quantitative** metric (speed, accuracy, completion rate).
- Must include at least one **qualitative** metric (user satisfaction, output quality).
- **Review cadence** -- How often is performance evaluated?

**Test:** After 30 days of use, could you confidently say whether this agent is working or not?

### 8. Governance Mode

Every agent must declare its current governance mode and operate within that mode's boundaries.

- **Mode declaration** -- `mode: observe | suggest | autonomous` in frontmatter or startup section.
- **Permission awareness** -- The agent knows what it can and cannot do in its current mode.
- **Escalation behavior** -- When an action exceeds current mode permissions, the agent stops and requests approval rather than proceeding.
- **Blast radius compliance** -- The agent respects the limits defined for its mode (see `governance.md`).

**Test:** Ask the agent to perform an action that exceeds its mode. Does it refuse or escalate cleanly?

### 9. Audit Logging

Every agent action that modifies state must be logged to the audit trail.

- **What to log** -- Any action that creates, updates, or deletes state (files, tasks, calendar, external systems).
- **Schema compliance** -- Log entries follow a consistent schema (see `governance.md` for an example).
- **Confidence tagging** -- Every action includes a confidence score (0.0-1.0).

**Test:** After a session with this agent, can you answer "what did it do and why?" from the audit log alone?

---

## Quality Signals (Beyond the Nine)

These are not requirements, but their presence indicates a well-designed agent:

- **Examples in the prompt** -- Showing the agent what good output looks like dramatically improves performance.
- **Negative examples** -- Showing what NOT to do is often more effective than positive instructions.
- **Contextual memory strategy** -- How the agent maintains awareness across interactions.
- **Version history** -- Tracking what changed and why across iterations.
- **Token efficiency** -- Is the prompt as lean as possible while still being complete? Every instruction that doesn't change behavior is wasted tokens.

---

## The Bloat Test

After writing or reviewing any agent prompt, apply this filter to every line:

> "If I remove this line, will the agent's output meaningfully change?"

If the answer is no, cut it. Common offenders:

- Personality traits that don't affect output ("Be creative", "Think outside the box")
- Vague operating principles ("Growth mindset", "Relentless progress")
- Redundant instructions that restate what the model already does
- Aspirational language that sounds good but drives no behavior

---

## Versioning

Every agent prompt must include a version number (e.g., `v1.0`, `v1.1`, `v2.0`).

- **Patch (v1.0 -> v1.1):** Minor wording refinements, no structural change.
- **Minor (v1.1 -> v1.2):** Added or removed a section, adjusted decision logic.
- **Major (v1.x -> v2.0):** Fundamental redesign of scope, architecture, or approach.

Each version change should include a one-line changelog entry in the agent file itself.
