# Example Agents

Three production-ready example agents that demonstrate the full Agent Standard (all 9 requirements). These are designed to work as a system, not just as standalone templates.

## The Three Agents

### 1. Researcher (`agents/researcher.md`)

Deep research engine. Takes research briefs, gathers information from multiple sources, cross-references findings, and delivers confidence-scored intelligence packages.

Key features:
- Confidence scoring on every finding (HIGH / MEDIUM / LOW)
- Source citation requirements (3+ independent sources for key claims)
- Explicit "what I searched and couldn't find" reporting
- Hard boundary: reports findings only, never makes recommendations

### 2. Strategist (`agents/strategist.md`)

Strategic thinking partner. Pressure-tests decisions, identifies non-obvious risks, and connects actions to stated goals.

Key features:
- Strategy context memory (maintains awareness across sessions via a context file)
- Goal-connected analysis (every recommendation ties back to user's stated objectives)
- Active challenging (surfaces flawed assumptions instead of validating them)
- Hard boundary: analyzes and recommends, never executes

### 3. Coordinator (`agents/coordinator.md`)

Operational backbone. Routes work, produces daily briefings, tracks progress, and ensures nothing falls through the cracks.

Key features:
- Routing table mapping request types to specialist agents
- Handoff templates (research, strategy, generic) so receiving agents get full context
- Accountability enforcement (flags stalled projects, overdue items)
- Hard boundary: routes and tracks, never decides or executes

## How They Work Together

```
User Request
    |
    v
Coordinator (triage + route)
    |
    +--> "Research X" --> Researcher --> findings
    |                                      |
    +--> "Should I X?" --> Strategist <----+
    |                         |
    |                    analysis + recommendation
    |                         |
    +<--- action items -------+
    |
    v
Track progress, flag blockers, brief user
```

The flow:

1. **Coordinator** receives incoming work and routes it based on the routing table
2. **Researcher** gathers and structures information when data is needed
3. **Strategist** analyzes options and pressure-tests decisions using research findings
4. **Coordinator** tracks resulting action items and ensures follow-through

Each agent has a hard boundary that prevents scope creep:
- Researcher never recommends. Strategist never researches. Coordinator never decides.
- When an agent hits the edge of its scope, it produces a handoff package for the right agent.

## How to Customize

### Quick Start

1. Copy the agent file you want to use
2. Update the mission statement for your specific context
3. Adjust the scope sections to match your needs
4. Add your own examples (the most impactful change you can make)
5. Set the governance mode (`observe` for new agents -- always)

### Adapting the System

**Adding a new specialist:** Create a new agent file, then add a routing rule in the Coordinator's routing table.

**Changing the Strategist's goals:** Update the Strategy Context file structure to reflect your goal framework. The agent's value is directly proportional to how well it knows what you're working toward.

**Scaling the Researcher:** Add domain-specific source preferences. For technical research, prioritize documentation and benchmarks. For market research, prioritize analyst reports and financial filings.

**Customizing the Coordinator's brief:** Adjust the daily brief template sections. Some users want calendar-first. Others want blockers-first. Match your workflow.

### What to Avoid

- Don't merge agents. The single-responsibility boundary is what makes each one sharp.
- Don't skip negative examples. They define boundaries more effectively than positive examples.
- Don't remove the Failure Protocol. Every agent will encounter edge cases -- the protocol is how it handles them gracefully instead of hallucinating.
- Don't start agents in Suggest or Autonomous mode. Trust is earned through the governance framework, not granted at deployment.

## Supporting Files

- `governance/trust-scores.json` -- Example trust scores showing agents at different maturity stages
- `governance/audit-log.jsonl` -- Example audit log entries for different action types
- `assessments/researcher-assessment.md` -- Example assessment output from the audit process
