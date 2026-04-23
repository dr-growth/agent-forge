# Agent Forge

A battle-tested framework for building AI agents that get smarter over time.

**Agent Forge is not another SDK.** It's a methodology, governance system, and self-improvement engine for building production-grade AI agents -- extracted from managing a portfolio of 22 real agents across research, engineering, sales, content, and operations.

## The Problem

Most AI agents are built once, shipped, and forgotten. They don't improve. They don't have quality standards. They don't have guardrails. When they break, nobody knows why. When they succeed, nobody knows what to replicate.

Agent Forge solves this with three systems:

### 1. Standards -- What "Good" Looks Like

Every agent must meet [9 non-negotiable requirements](docs/agent-standard.md):

```
1. Mission Statement       5. Decision Logic        8. Governance Mode
2. Defined Scope           6. Failure Protocol       9. Audit Logging
3. Input/Output Contract   7. Success Criteria
4. Tool Manifest
```

Plus a library of [proven patterns](docs/proven-patterns.md) that work and [anti-patterns](docs/anti-patterns.md) that don't.

### 2. Governance -- Trust Is Earned, Not Granted

```
OBSERVE ──────────> SUGGEST ──────────> AUTONOMOUS
(read-only)         (propose actions)    (act within guardrails)
Score: 0-39         Score: 40-79         Score: 80-100
```

Agents start in Observe mode and earn their way up through a [quantitative trust scoring system](docs/governance.md). Blast radius limits cap what any agent can change per action. Every state modification is audit-logged.

### 3. Self-Improvement -- Agents That Get Better Autonomously

```
Real work ──> OpenSpace watches ──> Failures trigger FIX
                                    Success patterns trigger DERIVED
                                    Novel approaches trigger CAPTURED
                                          │
                                          v
                              Usage metrics feed autoimprove
                                          │
                                          v
                              Scheduled batch optimization
                                          │
                                          v
                              Improved agents in daily use
```

Two systems work together:
- **[autoimprove](self-improvement/autoimprove/)** -- Scores agent output on 6 dimensions, proposes targeted improvements, commits winners, reverts losers. The git ratchet ensures quality only goes up. ~$0.19 per iteration.
- **[OpenSpace](self-improvement/openspace/)** -- MCP server that watches real agent execution and auto-evolves agents when they fail or succeed in interesting ways.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/dr-growth/agent-forge.git
cd agent-forge

# 2. Read the standard
cat docs/agent-standard.md

# 3. Copy the template
cp templates/agent-template.md my-agent.md

# 4. Build your agent (fill in all 9 sections)
# See examples/agents/ for reference

# 5. Assess it
# See docs/assessment.md for the rubric

# 6. Set up autoimprove
cd self-improvement/autoimprove
pip install anthropic
export ANTHROPIC_API_KEY=sk-...
python -m src.loop --skill my-agent --max-iterations 5

# 7. Watch it get better
```

See the full [Getting Started Guide](docs/getting-started.md) for a detailed walkthrough.

## Visual Architecture

Interactive diagrams that show how everything fits together:

- **[Architecture Board](architecture-board.html)** -- Full system overview: all 6 zones (Build, Execute, Govern, Improve, Lifecycle, Agents) with the Continuous Agent Forge Improvement Loop
- **[Workflow Diagram](workflow.html)** -- Step-by-step journey from idea to improved agent, showing exactly how /algorithm, autoimprove, and governance connect

## What's Inside

```
agent-forge/
├── docs/                          # Framework documentation
│   ├── agent-standard.md          # The 9 requirements
│   ├── proven-patterns.md         # 11 patterns that work
│   ├── anti-patterns.md           # 8 traps to avoid
│   ├── lifecycle.md               # 5 lifecycle modes
│   ├── governance.md              # Trust scoring + blast radius
│   ├── assessment.md              # How to test agents
│   ├── self-improvement.md        # The improvement loop
│   └── getting-started.md         # First agent in 30 minutes
│
├── methodology/                   # Execution methodologies
│   ├── algorithm.md               # 7-phase execution cycle
│   ├── discover.md                # Learning from external sources
│   └── isc.md                     # Ideal State Criteria
│
├── templates/                     # Start here
│   ├── agent-template.md          # Blank agent with all 9 sections
│   ├── assessment-template.md     # Assessment checklist
│   ├── test-case-template.json    # Test case format
│   └── directive-template.md      # Improvement directive format
│
├── examples/                      # Three fully-built agents
│   ├── agents/
│   │   ├── researcher.md          # Deep research agent
│   │   ├── strategist.md          # Strategic thinking agent
│   │   └── coordinator.md         # Operational coordinator
│   ├── assessments/               # Example assessment output
│   └── governance/                # Example trust scores + audit log
│
├── self-improvement/              # Agents that improve themselves
│   ├── autoimprove/               # Full Python source
│   │   ├── src/                   # loop.py, runner.py, evaluate.py, config.py
│   │   ├── test-cases/            # Example test cases
│   │   └── directives/            # Example directives
│   └── openspace/                 # Integration docs
│
└── diagrams/                      # System architecture (Mermaid)
```

## Key Principles

These emerged from building and managing 22 agents over 3 months:

1. **One Agent, One Job.** Multi-purpose agents do everything poorly. Split them.
2. **Negative Examples > Positive-Only.** Showing what NOT to do produces sharper behavior.
3. **Decision Logic as If/Then, Not Principles.** "Be pragmatic" doesn't change behavior. "If X, then Y" does.
4. **Trust Is Earned.** Every agent starts in Observe mode. Promotion requires evidence.
5. **The Bloat Test.** If removing a line doesn't change output, cut it.
6. **One Change Per Iteration.** Multiple simultaneous changes make attribution impossible.
7. **Audit Before Iterate.** Never patch symptoms. Find the root cause first.

## Methodologies

Agent Forge includes two execution methodologies you can use beyond agent building:

### The Algorithm -- 7-Phase Execution Cycle
For any non-trivial task: OBSERVE (understand deeply) -> THINK (pressure-test) -> PLAN (sequence) -> BUILD (prepare) -> EXECUTE (do) -> VERIFY (prove) -> LEARN (extract). [Full docs](methodology/algorithm.md)

### Discover -- External Learning Pipeline
Systematic process for evaluating external repos, articles, tools, and techniques: extract everything, classify against your current system, pressure-test adoption, prioritize, integrate. [Full docs](methodology/discover.md)

## Cost

The self-improvement engine is designed to be cheap:

| Activity | Cost |
|----------|------|
| Single autoimprove iteration | ~$0.19 |
| Full agent optimization (25 iterations) | ~$5 |
| Monthly portfolio maintenance | ~$100-200 |
| OpenSpace fix | ~$0.20 |

## Philosophy

Agent Forge treats AI agents like production software:
- They have quality standards
- They have governance and permissions
- They have testing and assessment
- They have continuous improvement
- They have version control and changelogs

The result: agents that are reliable, safe, and continuously getting better.

## Production Snapshot (April 2026)

Agent Forge is not theoretical. It manages a real portfolio in production.

Current state after the April 2026 audit cycle:

- **19 active agents** — down from 25 after portfolio audit flagged role overlap
- **8 agents demoted to skills** — failed the "agent vs skill" test (execute HOW rather than decide WHAT)
- **2 agents archived** — absorbed into higher-level orchestrators
- **10 Opus / 9 Sonnet** model distribution — audited and adjusted from prior 14/11 split
- **Governance Layer v1.0 deployed** — trust scoring active, blast radius enforced, audit logging operational
- **autoimprove v2 in daily use** — agents improving themselves every two weeks

Full governance specs in [governance/](governance/).

## Governance Specifications

Three companion specs for teams running agents in production:

- **[governance/trust-score-spec.md](governance/trust-score-spec.md)** — Formula, thresholds, and decay model for the trust-scoring system that gates Observe → Suggest → Autonomous promotion
- **[governance/audit-trail-spec.md](governance/audit-trail-spec.md)** — Logging schema, examples, and retention policy for every state-modifying action
- **[governance/blast-radius-spec.md](governance/blast-radius-spec.md)** — Per-mode limits on files modified, external writes, messages sent, and prohibited operations

## Related Projects

Agent Forge is part of a three-repo toolkit for building, governing, and auditing your own AI operating system:

- **[paios-template](https://github.com/dr-growth/paios-template)** — starter kit for bootstrapping a Personal AI Operating System. Scaffolded rules, hooks, commands, agents, skills, and frameworks.
- **Agent Forge** (you are here) — standards, governance, and self-improvement for agent portfolios
- **[os-audit](https://github.com/dr-growth/os-audit)** — McKinsey-tier qualitative audit for AI operating systems. 8-wave parallel architecture. Ship an exec deck + action plan in 6-10 hours.

## Contributing

1. Fork the repo
2. Follow the [Agent Standard](docs/agent-standard.md) for any new agents
3. Include test cases for any new agent examples
4. Keep docs concise -- no aspirational filler
5. Submit a PR

## License

MIT
