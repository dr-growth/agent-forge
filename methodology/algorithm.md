# The Algorithm: 7-Phase Execution Cycle

A structured execution framework for rigorous, high-quality work. Wraps every non-trivial task in a cycle: understand deeply, plan precisely, build carefully, verify thoroughly, learn from the experience.

Use The Algorithm when you want maximum quality and traceability. For lighter-weight planning without the full cycle, use a simpler planning process.

## When to Use

- Multi-step implementation work
- Anything that will take more than 30 minutes
- Work where failure modes matter (production changes, external-facing content, system architecture)
- When you need maximum confidence in the outcome

## When NOT to Use

- Quick lookups or single-file edits
- Conversational exploration or brainstorming
- Tasks already in progress with their own plan

---

## Phase 1: OBSERVE

**Goal:** Deeply understand what's being asked before touching anything.

### Actions

1. **Reverse engineer the request:**
   - What was explicitly asked for? (granular, one item per line)
   - What's implicitly wanted but unsaid?
   - What was explicitly NOT wanted?
   - What's obviously NOT wanted but unsaid?
   - How fast does it need to be done?

2. **Set effort level:**

| Tier | Time Budget | ISC Floor | When |
|------|------------|-----------|------|
| **Standard** | <2 hours | 8 | Normal task |
| **Extended** | <8 hours | 16 | Multi-file, cross-cutting |
| **Advanced** | <2 days | 24 | Substantial system changes |
| **Deep** | <1 week | 40 | Complex multi-system design |
| **Comprehensive** | <2 weeks | 64 | Full architecture overhaul |

3. **Define ISC (Ideal State Criteria):**
   - Write atomic, binary-testable criteria (8-12 words each, end states not actions)
   - Apply the Splitting Test: if a criterion can be split into two independent criteria, it must be
   - Include anti-criteria (ISC-A) for failure modes
   - **ISC Count Gate:** Cannot proceed until criteria count meets effort tier floor

See [isc.md](./isc.md) for the full ISC methodology.

### Output Format

```
OBSERVE

REVERSE ENGINEERING:
- Explicitly wanted: [list]
- Implicitly wanted: [list]
- Explicitly NOT wanted: [list]
- Implicitly NOT wanted: [list]

EFFORT LEVEL: [tier] | [8-word reasoning]

ISC: [N] criteria defined
[Show criteria list]
```

---

## Phase 2: THINK

**Goal:** Pressure-test the plan before building anything.

### Actions

1. Identify the 2-5 riskiest assumptions
2. Run a premortem: 2-5 ways the current approach could fail
3. Check prerequisites: what do we need that we might not have?
4. Refine ISC based on risks discovered (split compound criteria, add missing failure modes)

### Output Format

```
THINK

RISKIEST ASSUMPTIONS:
- [assumption 1]
- [assumption 2]

PREMORTEM:
- [failure mode 1]
- [failure mode 2]

PREREQUISITES:
- [what we need and whether we have it]

ISC REFINED: [any criteria added/split]
```

---

## Phase 3: PLAN

**Goal:** Map the execution path.

### Actions

1. Sequence the work into phases
2. Map ISC criteria to phases (every criterion must be covered)
3. Identify parallel vs sequential phases
4. Validate prerequisites are met

### Output Format

```
PLAN

EXECUTION SEQUENCE:
Phase A: [name] -- ISC-1, ISC-2, ISC-3
Phase B: [name] -- ISC-4, ISC-5 (parallel with A)
Phase C: [name] -- ISC-6, ISC-7 (depends on A)

FILES TO MODIFY:
[file list with changes]
```

---

## Phase 4: BUILD

**Goal:** Prepare everything needed before execution.

### Actions

1. Set up scaffolding (directories, templates, configs)
2. Resolve any remaining unknowns
3. Make non-obvious technical decisions and document them
4. If the task is straightforward, BUILD and EXECUTE can be combined

This phase separates preparation from execution. Skipping it is acceptable for simple tasks, but for complex work, the separation prevents false starts.

---

## Phase 5: EXECUTE

**Goal:** Do the actual work.

### Actions

1. Implement the plan phase by phase
2. Check off ISC criteria immediately as they are satisfied (do not batch)
3. Track progress as criteria are completed
4. Log any mid-execution decisions
5. If the approach needs to change significantly, pause and re-enter THINK

### Rules

- One change at a time when debugging
- Read files before modifying them
- If blocked, do not brute force. Reconsider the approach.

---

## Phase 6: VERIFY

**Goal:** Confirm every criterion is actually met with evidence.

### Actions

1. For each ISC criterion, provide specific evidence (not blanket assertions)
2. For anti-criteria, prove absence (search for the thing that should not exist)
3. If any criteria FAIL, loop back to EXECUTE for that specific criterion

### Gate

All ISC must PASS before proceeding to LEARN. No exceptions.

### Evidence Standards

Acceptable evidence:
- Direct observation: "File X contains Y at line Z"
- Test output: "Running `npm test` produces 0 failures"
- Absence proof: "Grep for [pattern] returns 0 results"

Not acceptable:
- "It works" (no evidence)
- "Looks correct" (no specificity)
- "Should be fine" (speculation)

---

## Phase 7: LEARN

**Goal:** Extract value from the experience.

### Actions

1. Reflect on the execution:
   - What should have been done differently?
   - What would a smarter approach have looked like?
   - What patterns emerged that could become reusable?
2. Document insights worth preserving
3. If a new rule or pattern is warranted, capture it

### Output Format

```
LEARN

REFLECTIONS:
- [What worked well]
- [What should change next time]
- [Patterns worth extracting]

RESULT: [M]/[N] criteria passed.
```

---

## Phase Transitions

Track where you are at every transition. The ISC list is the system of record for progress.

If context gets bloated during long runs (Extended+ effort), compress intermediate reasoning at phase boundaries. Preserve: ISC status, key results, decisions. Discard: raw tool output, verbose reasoning.

## Effort Tier Reference

| Tier | Time | ISC Floor | Phases Required |
|------|------|-----------|-----------------|
| Standard | <2hr | 8 | All 7, THINK can be brief |
| Extended | <8hr | 16 | All 7, full depth |
| Advanced | <2 days | 24 | All 7, document decisions |
| Deep | <1 week | 40 | All 7, checkpoint at phase boundaries |
| Comprehensive | <2 weeks | 64 | All 7, formal deliverables per phase |

## Attribution

Adapted from the PAI Algorithm (Daniel Miessler). 7-phase structure preserved. ISC methodology, Splitting Test, effort tiers, and premortem patterns sourced from PAI.
