# Agent Lifecycle Engine v1.0

Every agent moves through a defined lifecycle. This document defines the process for each stage. Operate in one mode at a time and follow the corresponding playbook.

---

## Stage 1: Architect Mode

**When:** A new agent needs to be created from scratch.

### Step 1 -- Discovery (Do NOT skip this)

Before writing a single line of prompt, gather:

- **What problem does this agent solve?** Get specific. "Helps with sales" is not a problem statement. "Generates personalized outreach emails using account research and signal data" is.
- **Who is the user?** Just you? Your team? External users?
- **What tools will it need?** Map the integrations required.
- **What does success look like?** Get at least one measurable outcome.
- **What existing agents might overlap?** Check your registry to avoid redundancy.

### Step 2 -- Design

- Fill out the Agent Template completely (see `templates/` for a starter).
- Validate against all 9 requirements in the Agent Standard.
- Flag any requirement that can't be met yet and document why.

### Step 3 -- Review

- Walk through the completed design.
- Apply the Bloat Test to every section.
- Stress-test: What happens with edge cases, ambiguous input, tool failure?

### Step 4 -- Ship V1

- Finalize the prompt with a `v1.0` version tag.
- Add the agent to your registry.
- Document the initial design rationale in the agent's file.

**Exit criteria:** Agent meets all 9 requirements of the Agent Standard and is registered.

---

## Stage 2: Audit Mode

**When:** An existing agent is brought in for review (first-time or periodic).

### Step 1 -- Standard Check

Run the agent prompt against all 9 requirements of the Agent Standard. For each:

- **Pass** -- Requirement is clearly met.
- **Partial** -- Present but weak, vague, or incomplete.
- **Fail** -- Missing entirely.

### Step 2 -- Bloat Analysis

Apply the Bloat Test. Identify:

- Lines that don't change behavior (cut candidates)
- Instructions that restate default model behavior (cut candidates)
- Personality/principle statements with no functional impact (cut or convert to functional instructions)

### Step 3 -- Gap Analysis

Identify what's missing beyond the standard:

- Are there examples (positive and negative)?
- Is there a memory strategy?
- Are edge cases handled?
- Is the prompt token-efficient?

### Step 4 -- Diagnosis Report

Produce a structured assessment:

- **Overall grade** (A through F)
- **What's working** -- Keep these elements.
- **What's bloated** -- Cut or rewrite these.
- **What's missing** -- Add these.
- **Recommended next steps** -- Prioritized list of improvements.

**Exit criteria:** Diagnosis report delivered, improvement plan agreed upon.

---

## Stage 3: Iterate Mode

**When:** An agent has been audited and you return with feedback from real usage.

### Step 1 -- Feedback Intake

Collect specific examples:

- Where did the agent fall short? (Get the actual input and output if possible.)
- Where did it exceed expectations?
- Any new use cases discovered that should be added to scope?
- Any scope items that turned out to be unnecessary?

### Step 2 -- Root Cause Analysis

For each failure or shortcoming, diagnose WHY:

- **Prompt gap** -- The instruction was missing or vague.
- **Scope creep** -- The agent tried to do something outside its design.
- **Tool limitation** -- The agent needed a capability it doesn't have.
- **Model limitation** -- The task exceeds what the model can reliably do.

### Step 3 -- Targeted Patch

Make the minimum effective change. Don't rewrite the whole prompt because one section underperformed. Patch surgically:

- Add missing instructions.
- Sharpen vague ones.
- Add examples of the failure case and desired behavior.
- Adjust decision logic or escalation triggers.

### Step 4 -- Version Bump

- Update the version number.
- Add a changelog entry.
- Update the registry with new version and date.

**Exit criteria:** Patch applied, version bumped, registry updated.

---

## Stage 4: Govern Mode

**When:** Periodic portfolio-level review (recommended: monthly).

### Step 1 -- Registry Review

Pull up the full agent registry. For each agent, check:

- Last review date -- Is it overdue?
- Version -- Has it been iterated on, or is it still v1.0?
- Usage -- Are you actually using it? (If not, why?)

### Step 2 -- Overlap and Redundancy Check

As your agent count grows, overlap is inevitable. Identify:

- Agents with overlapping scope -- Candidates for merging.
- Agents unused for 30+ days -- Candidates for sunsetting.
- Agents that have grown beyond their original mission -- Candidates for splitting.

### Step 3 -- Architecture Health Check

Zoom out and assess the overall system:

- Are agents well-organized by domain?
- Are there gaps -- areas of your work with no agent coverage?
- Is the total number of agents manageable, or is there sprawl?

### Step 4 -- Governance Report

Produce a portfolio-level summary:

- Agents reviewed, overall health.
- Recommended merges, sunsets, or new agents.
- Priority actions for the next cycle.

**Exit criteria:** Governance report delivered, action items agreed upon.

---

## Stage 5: Research Mode

**When:** Monthly research audit to validate architecture decisions against latest findings.

### Step 1 -- Source Collection

Gather the latest research on prompt engineering, agent architectures, and tool-use patterns from:

- Model provider documentation (Anthropic, OpenAI, Google)
- Academic papers on agent design
- Open-source agent framework releases
- Community best practices and post-mortems

### Step 2 -- Pattern Extraction

For each source, identify:

- Techniques that validate your current patterns (confidence boost)
- Techniques that contradict your current patterns (investigate)
- New techniques not yet captured in your proven patterns library

### Step 3 -- Validation

Test new techniques against your existing agents:

- Pick one agent as a guinea pig.
- Apply the technique.
- Measure output quality before and after.
- If improved, document in your proven patterns library with source.

### Step 4 -- Update Standards

If research reveals a fundamental gap in your standards:

- Propose the change with evidence.
- Apply it to one agent first (pilot).
- Roll out to the portfolio if validated.

**Exit criteria:** Research audit complete, patterns library updated, standards reviewed.
