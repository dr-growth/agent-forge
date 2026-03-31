# Discovery Pipeline

A structured process for analyzing external content (repos, articles, podcasts, tools) to extract techniques, patterns, and ideas worth integrating into your agent system.

Use the Discovery Pipeline when you encounter something external and want to understand what is valuable, what is noise, and what should be integrated.

## Core Mindset

**Growth-first, never dismissive.** Even when your system has a more sophisticated version of something, ask: "What angle or approach here could make ours better?" Never rush to "we already have this." The goal is continuous improvement.

## Effort Tiers

Not every discovery deserves the same depth. Set the tier before starting.

| Tier | Source Type | Depth | Time |
|------|-----------|-------|------|
| **Quick Scan** | Tweet, short post, single technique | Extract + classify, skip formal brief | 5 min |
| **Standard** | Article, podcast, blog post | Full pipeline, inline output | 15-30 min |
| **Deep Dive** | Full repo, framework, multi-part series | Full pipeline + discovery brief artifact | 1-2 hours |
| **Strategic** | Architecture paradigm, major tool, system-level shift | Full pipeline + strategic evaluation | Half day |

Default to **Standard**. Escalate if the source keeps yielding signal.

---

## The Pipeline

### Phase 0: OBSERVE

Before extracting anything, reverse-engineer the source.

1. **What is this?** Type, author, date, context (why was it created?)
2. **What's explicitly offered?** Techniques, tools, patterns, code
3. **What's implicitly offered?** Philosophy, mental models, architecture thinking
4. **What's NOT relevant?** Parts that do not connect to your system or goals
5. **What's the author's level and context?** Beginner tutorial vs. battle-tested practitioner matters

**Output:**
```
OBSERVE: [Source Title]
Type: [repo/article/podcast/tool] | Author: [who] | Tier: [quick/standard/deep/strategic]
Explicitly offered: [list]
Implicitly offered: [list]
Not relevant: [list]
Author context: [one line]
```

---

### Phase 1: Deep Extract

Go deep. This is not a summary exercise.

**For URLs/Articles/Podcasts:**
- Fetch full content (use web fetch tools, transcripts, related coverage)
- Extract EVERY actionable technique, pattern, philosophy, architecture decision, and workflow
- Capture specific code examples, config patterns, and implementation details
- Note the author's reasoning, not just their conclusions

**For Repos:**
- Read the README fully
- Read configuration files, agent definitions, skill definitions, hook configs
- Read key source files that implement the core patterns
- Understand the architecture decisions and why they were made
- Look at how they handle: context loading, agent orchestration, tool integration, quality gates
- Check issues and discussions for roadmap signals

**For Tools/Products:**
- Understand the core value proposition
- Map the feature set against your current capabilities
- Identify unique approaches or novel solutions

**Output format:**
```markdown
## Deep Extract: [Source Title]

### Source
- Type: [repo/article/podcast/tool]
- URL: [link]
- Author: [who]
- Date: [when]

### Techniques and Patterns
Number every finding. No limit. Extract everything.

1. **[Technique Name]**: [Description]
   - Implementation: [How they do it]
   - Key insight: [Why it matters]

2. ...continue for ALL findings
```

---

### Phase 2: Gap Analysis

Compare every extracted finding against your current system state. **Read the relevant files to verify, not from memory.**

**For each finding, classify:**

| Classification | Meaning |
|---------------|---------|
| NEW | You do not have anything like this |
| UPGRADE | You have something similar but this approach is better or adds a dimension |
| LEARN | You have a more sophisticated version but there is a specific angle worth absorbing |
| VALIDATE | Confirms your approach is solid (still note what specifically validates it) |
| NOT APPLICABLE | Does not fit your architecture or goals (explain why) |

**VERIFY rule:** When classifying as UPGRADE, show evidence. Read the current file. Show what exists. Show what is better. No blanket assertions.

**Output format:**
```markdown
## Gap Analysis

### NEW Findings
| # | Finding | What It Enables | Where It Fits |
|---|---------|----------------|---------------|

### UPGRADE Findings
| # | Finding | Current State | What's Better | Where to Apply |
|---|---------|--------------|---------------|---------------|

### LEARN Findings
| # | Finding | Our Version | Angle Worth Absorbing |
|---|---------|-------------|----------------------|

### VALIDATE Findings
| # | Finding | What It Confirms |
|---|---------|-----------------|
```

---

### Phase 3: THINK

Before prioritizing, pressure-test the integration.

For each NEW or UPGRADE finding:
1. **Adoption cost:** What breaks or changes if you add this?
2. **Complexity tax:** Does this add maintenance burden disproportionate to value?
3. **Dependency check:** Does this require something you do not have?
4. **Conflict check:** Does this contradict an existing pattern or rule?

Kill anything where the adoption cost exceeds the value. Be honest about it.

---

### Phase 4: Prioritize

Rank surviving NEW, UPGRADE, and LEARN findings by impact and urgency.

| Priority | Criteria | Timeline |
|----------|----------|----------|
| P0 - Build Now | Fills a critical gap or unblocks significant capability | This session or next |
| P1 - Build Soon | Clear upgrade to existing workflow | Within the week |
| P2 - Queue | Valuable but not urgent, or depends on other work | Add to backlog |
| P3 - Someday | Interesting direction, revisit when relevant | Log for reference |

**For each prioritized item, specify:**
- What artifact to create or modify (skill, agent, rule, hook, config)
- Where it lives in the system
- Dependencies (does it need something else first?)
- Estimated complexity (trivial / moderate / significant)

### Rep 1 Ship Plan (for P0 and P1 items)

For every P0 or P1 item, include a concrete "Rep 1" ship plan -- the smallest shippable version that delivers value.

```markdown
#### Rep 1: [Item Name]
- **Goal:** [One sentence -- what exists after Rep 1 that doesn't exist now]
- **Scope:** [Exactly what to build/modify -- no more]
- **Not in Rep 1:** [What to explicitly defer]
- **Ship criteria:** [2-3 binary tests that confirm Rep 1 is done]
- **Time estimate:** [Hours, not days]
```

**Philosophy:** Ship small, ship fast. The purpose of Rep 1 is to create something real, not something perfect. If Rep 1 takes more than a day, the scope is too large -- cut it down.

Rep 2-5 can be sketched in one line each. Do not over-plan future reps -- they will be informed by what you learn shipping Rep 1.

---

### Phase 5: Integration Plan

For P0 and P1 items, produce a concrete integration plan:

```markdown
## Integration Plan

### P0: [Item Name]
- **Action:** [Create skill / Modify agent / Add hook / Update rule]
- **Location:** [Exact file path]
- **Dependencies:** [What needs to exist first]
- **Implementation:** [Specific steps]

### P1: [Item Name]
...
```

---

### Phase 6: LEARN

After the discovery session:
1. **Source quality:** Was this source high-signal or mostly noise? Log it.
2. **Pattern detection:** Are you seeing the same gaps across multiple discoveries? That is a systemic weakness.
3. **Philosophy shifts:** Did this change how you think about something, not just what you do?
4. **Feed forward:** What should future discovery sessions look for based on what you learned?

---

## Discovery Brief (Deep Dive+ tiers)

For Deep Dive and Strategic tiers, persist findings as a discovery brief:

```markdown
---
source: [title]
url: [link]
author: [who]
date_discovered: [YYYY-MM-DD]
tier: [quick/standard/deep/strategic]
findings_count: [N]
integrated: [list of P0/P1 items that were built]
queued: [list of P2/P3 items for future]
---

[Full pipeline output: OBSERVE + Extract + Gap Analysis + THINK + Prioritize + Integration Plan]
```

---

## Session Close

Every discovery session must end with:
1. P0 items either built or added to your task backlog
2. P1-P3 items logged for future sessions
3. Discovery brief saved (Deep Dive+ tiers)
4. Source quality noted for future reference
