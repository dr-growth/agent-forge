# Getting Started: Your First Agent in 30 Minutes

This guide walks you through building, assessing, and improving your first agent using Agent Forge.

## Prerequisites

- Claude Code or any Claude API access
- Python 3.11+ (for autoimprove)
- Git
- `pip install anthropic`

## Step 1: Understand the Standard (5 min)

Read [agent-standard.md](agent-standard.md). Every agent you build must meet these 9 requirements. The standard exists because agents without clear boundaries, failure protocols, and success criteria produce mediocre results and are impossible to improve systematically.

The short version:

| # | Requirement | One-Line Test |
|---|-------------|---------------|
| 1 | Mission Statement | Can you state why this agent exists in one sentence? |
| 2 | Defined Scope | Can the agent refuse an out-of-scope request cleanly? |
| 3 | Input/Output Contract | Can someone predict the output from a given input? |
| 4 | Tool Manifest | Does removing any tool meaningfully degrade capability? |
| 5 | Decision Logic | Does the agent know exactly what to do with ambiguous input? |
| 6 | Failure Protocol | Does it handle broken tools and contradictory info gracefully? |
| 7 | Success Criteria | After 30 days, can you say whether it's working? |
| 8 | Governance Mode | Does it refuse actions that exceed its permissions? |
| 9 | Audit Logging | Can you reconstruct what it did and why from logs alone? |

## Step 2: Copy the Template (2 min)

```bash
cp templates/agent-template.md agents/my-first-agent.md
```

Open it. You'll see placeholders for every section. Don't skip any -- if a section doesn't apply, write "N/A -- [reason]" so it's a conscious decision, not an accidental omission.

## Step 3: Define Your Agent (15 min)

Fill in the template. Start with these three things:

### Mission (1 sentence)
> What outcome does this agent produce that wouldn't happen without it?

Bad: "Helps with research tasks."
Good: "Gathers, verifies, and structures competitive intelligence from public sources into confidence-scored briefing packs."

### Scope (explicit in/out)
List what it handles AND what it doesn't. For everything out of scope, say where it goes instead.

```markdown
### In Scope
- Competitive intelligence gathering
- Company profile research
- Technology landscape analysis

### Out of Scope
- Strategic recommendations -> hand off to strategist agent
- Content creation from research -> hand off to content agent
- Real-time monitoring -> not yet implemented
```

### Decision Logic (if/then, not principles)
Don't write "Be thorough." Write:

```markdown
### Autonomous Actions
- Begin research immediately upon receiving a brief
- Search 3+ independent sources per key finding
- Score every finding with confidence level

### Escalation Triggers
1. Research brief is ambiguous -- ask for clarification
2. Findings contradict each other from credible sources -- present both
3. Required tool (web search) is unavailable -- state limitation
```

Look at [examples/agents/](../examples/agents/) for three fully-built agents you can reference.

## Step 4: Apply the Bloat Test (5 min)

Read every line of your agent and ask:

> "If I remove this line, will the agent's output meaningfully change?"

Cut anything that fails this test. Common things to remove:
- "Be creative" / "Think outside the box" (personality without function)
- "Provide helpful responses" (the model already does this)
- "Growth mindset" / "Relentless progress" (motivational posters)

See [anti-patterns.md](anti-patterns.md) for the full list of traps.

## Step 5: Test It (5 min)

Give your agent 3 different inputs:
1. A normal, well-formed request (should produce good output)
2. An out-of-scope request (should refuse or redirect)
3. An ambiguous request (should follow your ambiguity protocol)

If it fails any of these, your prompt needs work. See [assessment.md](assessment.md) for the full testing methodology.

## Step 6: Set Up Governance (3 min)

Create a trust score file:

```json
{
  "agent": "my-first-agent",
  "cluster": "research",
  "mode": "observe",
  "score": 10,
  "last_updated": "2026-03-30T00:00:00Z",
  "history": [
    {
      "date": "2026-03-30",
      "event": "initial_deployment",
      "delta": 10,
      "reason": "Initial deployment"
    }
  ]
}
```

Your agent starts in Observe mode (read-only, text output only). It earns its way to Suggest and eventually Autonomous through demonstrated competence. See [governance.md](governance.md) for the full framework.

## Step 7: Set Up autoimprove (10 min)

This is where agents start improving themselves.

### Create test cases

```bash
mkdir -p self-improvement/autoimprove/test-cases/my-first-agent
```

Create 2-3 test cases (JSON files):

```json
{
  "name": "basic-research-task",
  "input_prompt": "Research the competitive landscape for [your domain]",
  "ground_truth": "Should include: market overview, 3+ key players with specific details, recent developments, confidence scores on all findings",
  "schema": {
    "required_sections": ["## Summary", "## Key Players", "## Analysis"],
    "required_fields": ["confidence:"],
    "min_word_count": 500
  }
}
```

### Create a directive

```bash
cat > self-improvement/autoimprove/directives/my-first-agent.md << 'EOF'
# Improvement Directive: my-first-agent

## Optimization Goals
- Increase specificity (fewer generic claims, more concrete data)
- Improve confidence calibration (appropriate mix of HIGH/MEDIUM/LOW)
- Ensure all findings have source citations

## Constraints
- Do NOT modify: governance section, scope boundaries, tool manifest
- DO modify: instruction text, output format guidance, examples
EOF
```

### Run the loop

```bash
cd self-improvement/autoimprove
export ANTHROPIC_API_KEY=sk-...
python -m src.loop --skill my-first-agent --max-iterations 5
```

Watch it score, propose changes, validate, and commit improvements. Cost: ~$1 for 5 iterations.

### Promote improvements

```bash
# Review the diff
diff work/my-first-agent.md agents/my-first-agent.md

# If satisfied, promote
cp work/my-first-agent.md agents/my-first-agent.md
```

## What's Next

- Read [proven-patterns.md](proven-patterns.md) for patterns that consistently work
- Read [lifecycle.md](lifecycle.md) for the full agent lifecycle (Architect -> Audit -> Iterate -> Govern -> Research)
- Set up [OpenSpace](../self-improvement/openspace/) for continuous evolution from real usage
- Build more agents and let them coordinate (see the coordinator example)

## Common Mistakes

1. **Skipping the scope section.** Agents without explicit boundaries try to do everything and do nothing well.
2. **Writing principles instead of rules.** "Be thorough" doesn't work. "Search 3+ sources per finding" does.
3. **No failure protocol.** The first time a tool breaks, an agent without a failure protocol will hallucinate.
4. **No success criteria.** If you can't measure it, you can't improve it.
5. **Making the agent too complex.** Start with one job. Add complexity only when the simple version proves insufficient.
