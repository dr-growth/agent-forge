# OpenSpace -- Continuous Agent Evolution

An MCP server that watches agent execution and auto-evolves agents from real usage. While autoimprove is the lab (scheduled experiments), OpenSpace is the immune system (continuous defense and adaptation).

## How It Works

1. You use an agent during normal work
2. OpenSpace's execution analyzer watches the full task trajectory
3. If an agent fails or underperforms, OpenSpace diagnoses why and triggers a FIX evolution
4. If an agent works well and reveals a pattern, OpenSpace spawns a DERIVED variant or CAPTURES a new agent
5. Over time, the agent portfolio self-heals and self-expands without manual intervention

## Evolution Types

### FIX
Repair a broken agent in-place. Same file, updated content. Triggered by failures.

**Example:** Your researcher agent keeps producing outputs without confidence scores. OpenSpace detects the pattern, diagnoses that the confidence calibration instructions are buried too deep in the prompt, and moves them to a more prominent position.

### DERIVED
Specialize or enhance an existing agent. Creates a new agent alongside the parent. Triggered by success patterns.

**Example:** Your general researcher agent consistently gets used for competitive intelligence. OpenSpace creates a specialized `competitive-researcher` that inherits the base research protocol but adds competitor-specific sections and data sources.

### CAPTURED
Extract a novel reusable pattern from a successful execution. Brand new agent. Triggered by novel approaches.

**Example:** During a complex project, you improvise a multi-step verification workflow that works well. OpenSpace captures this as a standalone `verifier` agent.

## Setup

OpenSpace is an MCP server. Add it to your Claude Code configuration:

```json
{
  "mcpServers": {
    "openspace": {
      "command": "node",
      "args": ["path/to/openspace/dist/index.js"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-...",
        "OPENSPACE_MODEL": "anthropic/claude-sonnet-4-6",
        "SKILLS_DIR": "~/.claude/agents/"
      }
    }
  }
}
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `search_skills` | Find agents by capability or keyword |
| `execute_task` | Run an agent with real-time observation |
| `fix_skill` | Manually trigger a FIX evolution on an agent |
| `upload_skill` | Add a new agent to the portfolio |

## Integration with autoimprove

OpenSpace generates real-world quality signals:
- **Completion rate** -- Did the agent finish the task?
- **Applied rate** -- Did the user actually use the output?
- **Fallback rate** -- Did the user abandon the agent mid-task?

These signals feed into autoimprove's prioritization. autoimprove's scoring improvements raise the quality baseline that OpenSpace then defends.

## Cost

- ~$0.20 per fix evolution
- ~$0.20 per real-time evolution event
- Monthly steady-state: $50-100 for continuous evolution

## More Information

OpenSpace is a separate open-source project. This directory documents how it integrates with Agent Forge's self-improvement loop.

For the full OpenSpace documentation and source code, see the [OpenSpace repository](https://github.com/openspace-ai/openspace).
