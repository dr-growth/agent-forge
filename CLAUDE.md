# Agent Forge

Framework for building, governing, and continuously improving AI agents. This repo is a knowledge framework + methodology + tooling, not a code SDK.

## Repo Structure

- `docs/` -- Core framework documentation (standards, patterns, governance, lifecycle)
- `methodology/` -- Execution methodologies (algorithm, discover, ISC)
- `templates/` -- Blank templates for agents, assessments, test cases
- `examples/` -- 3 fully-built example agents with assessments and governance files
- `self-improvement/` -- autoimprove engine (Python) + OpenSpace integration docs
- `diagrams/` -- Mermaid diagrams of all system components

## Key Concepts

- **Agent Standard:** 9 non-negotiable requirements every agent must meet
- **Governance Modes:** Observe -> Suggest -> Autonomous (trust is earned, not granted)
- **Self-Improvement Loop:** autoimprove (scheduled optimization) + OpenSpace (continuous evolution)
- **Lifecycle Engine:** 5 modes (Architect, Audit, Iterate, Govern, Research)

## Contributing

- Follow the Agent Standard when proposing new example agents
- Keep docs concise and actionable (no aspirational filler)
- Test all Python changes against example test cases
- Update CHANGELOG.md with every significant change
