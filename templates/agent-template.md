# Agent Template

> Copy this template when creating a new agent. Fill in every section. If a section does not apply, write "N/A -- [reason]" rather than deleting it. This ensures conscious decisions rather than accidental omissions.

---

```yaml
---
name: [agent-name]
version: v1.0
description: |
  [2-3 sentence mission. What outcome does this agent produce
  that would not happen without it?]
model: [model-name]
governance_mode: observe
trust_score: 10
permissions:
  allow: []
  deny: []
---
```

---

## Mission

<!-- One sentence. What outcome does this agent produce that would not happen without it?
     If you cannot state it in one sentence, the scope is too broad. -->

[Mission statement]

---

## Scope

### In Scope
<!-- Explicit list of responsibilities. Be specific. -->
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

### Out of Scope
<!-- What this agent does NOT handle, and where that work goes instead. -->
- [Exclusion 1] -> [Where this goes instead]
- [Exclusion 2] -> [Where this goes instead]

### Handoff Rules
<!-- When and how this agent transfers work to other agents or humans. -->
- If [condition], hand off to [agent/human/process]
- If [condition], hand off to [agent/human/process]

---

## Input/Output Contract

### Inputs (What Triggers This Agent)

<!-- What activates this agent? Be specific about trigger types. -->

| Trigger Type | Description | Example |
|-------------|-------------|---------|
| [User message / Scheduled / Event / Agent output] | [What specifically triggers it] | [Concrete example] |

### Outputs (What This Agent Produces)

<!-- What does this agent deliver? Define the format precisely. -->

| Output Type | Format | Example |
|------------|--------|---------|
| [Analysis / Recommendation / Draft / Action] | [Prose / Structured / JSON / Template] | [Concrete example] |

---

## Tool Manifest

<!-- Every tool the agent can access, why it needs it, and when to use it.
     No tool access without justification. If you remove a tool and the agent
     still works the same, it did not need that tool. -->

| Tool | Purpose | Usage Rule |
|------|---------|-----------|
| [Tool name] | [Why it needs this tool] | [When to use vs. not use] |

---

## Decision Logic

### Autonomous Actions (Act Without Asking)
<!-- Actions the agent can take on its own. Define the conditions precisely. -->
- [Action 1 -- under what conditions]
- [Action 2 -- under what conditions]

### Escalation Triggers (Stop and Ask)
<!-- Conditions that require human input before proceeding. -->
1. [Condition that requires human input]
2. [Condition that requires human input]
3. [Condition that requires human input]

### Ambiguity Protocol
<!-- What the agent does when input is unclear or information conflicts. -->
- When input is unclear: [Ask for clarification / Make best guess and flag / Refuse]
- When information conflicts: [Resolution strategy]

### Confidence Thresholds
<!-- How certain the agent must be before acting vs. flagging uncertainty. -->
- Act autonomously when confidence >= [threshold]
- Flag for review when confidence is between [low] and [high]
- Escalate when confidence < [threshold]

---

## Failure Protocol

<!-- How the agent handles things going wrong. Every row must have a specific response,
     not a vague "handle gracefully." -->

| Failure Scenario | Response |
|-----------------|----------|
| Agent does not know the answer | [Admit uncertainty / Search / Escalate] |
| Tool is unavailable | [Graceful degradation plan] |
| Conflicting information received | [Resolution strategy] |
| Output does not meet quality bar | [Self-check / Flag / Retry strategy] |

---

## Success Criteria

### Quantitative Metrics
<!-- At least one measurable metric. -->
- [Metric 1 -- e.g., "Produces output in under 60 seconds"]
- [Metric 2 -- e.g., "Accuracy rate of 90%+ on fact-based queries"]

### Qualitative Metrics
<!-- At least one quality-based metric. -->
- [Metric 1 -- e.g., "Output requires fewer than 2 rounds of revision"]
- [Metric 2 -- e.g., "User rates output as useful or very useful 80%+ of the time"]

### Review Cadence
<!-- How often this agent is formally evaluated. -->
- [Monthly / Quarterly / Per use / After N invocations]

---

## Governance Mode

<!-- Declare the current operating mode. Agents start in Observe and earn their way up. -->

**Current Mode:** observe

| Mode | What It Can Do |
|------|---------------|
| observe | Read context, produce analysis, answer questions. No external writes. |
| suggest | Everything in observe + propose actions for human approval. |
| autonomous | Everything in suggest + execute approved action types independently. |

**Blast radius limits:** [Reference your governance spec or define inline]

---

## Communication Style

<!-- How the agent communicates. This shapes the output tone and format. -->

- **Default tone:** [Conversational / Formal / Technical / Adaptive]
- **Formatting rules:** [When to use structure vs. prose]
- **Length guidance:** [Default response length, when to go longer/shorter]
- **Anti-patterns:** [What the agent should never do in its output]

---

## Examples

### Good Output Example

**Input:** [Sample input]

**Output:** [What the agent SHOULD produce]

### Bad Output Example

**Input:** [Sample input]

**Output:** [What the agent should NOT produce]

**Why it is bad:** [Explanation]

---

## Changelog

| Version | Date | Change | Reason |
|---------|------|--------|--------|
| v1.0 | [YYYY-MM-DD] | Initial creation | -- |
