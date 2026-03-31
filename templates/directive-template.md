# Improvement Directive: [Agent Name]

**Date:** YYYY-MM-DD
**Agent Version:** v[X.Y]
**Assessment Reference:** [path to assessment that prompted this directive]
**Target Version:** v[X.Y+1]

---

## Optimization Goals

<!-- What specific dimensions or behaviors need to improve? Reference assessment scores. -->

1. [Dimension to improve] -- Current score: [X.X], Target: [Y.Y]
2. [Behavior to change] -- Evidence: [quote from assessment]
3. [Capability to add/refine] -- Rationale: [why]

---

## Constraints

<!-- Hard boundaries on what the improvement process can and cannot change. -->

### Do NOT Modify
- Governance section (mode, trust score, permissions)
- Model assignment
- Scope boundaries (in scope / out of scope lists)
- Tool manifest (adding or removing tools requires separate approval)
- Handoff rules

### DO Modify
- Instruction text within existing sections
- Output format specifications
- Examples (good and bad)
- Decision logic thresholds
- Failure protocol responses
- Communication style guidance

---

## Quality Bar

<!-- Minimum scores the improved agent must achieve on re-assessment. -->

**Minimum composite score:** [X.X] / 3.0

**Priority dimensions:**

| Dimension | Current | Target | Notes |
|-----------|---------|--------|-------|
| [D1-D7] | [score] | [score] | [what needs to change] |
| [D1-D7] | [score] | [score] | [what needs to change] |

---

## Specific Changes

<!-- Concrete, actionable changes to make. Each change should map to an optimization goal. -->

### Change 1: [Short description]

**Goal:** [Which optimization goal this addresses]

**Current behavior:** [What the agent does now, with evidence]

**Desired behavior:** [What the agent should do instead]

**Implementation:** [Specific text to add, remove, or modify in the agent prompt]

### Change 2: [Short description]

**Goal:** [Which optimization goal this addresses]

**Current behavior:** [What the agent does now]

**Desired behavior:** [What the agent should do instead]

**Implementation:** [Specific changes]

---

## Validation Plan

<!-- How to verify the improvements worked. -->

### Re-run Tests

<!-- Which tests from the original assessment to re-run. -->

| Test | Original Score | Expected Improvement | Why |
|------|---------------|---------------------|-----|
| [test name] | [score] | [target] | [what the change fixes] |

### New Tests

<!-- Any new tests needed to validate the specific changes. -->

| Test Name | What It Probes | Pass Criteria |
|-----------|---------------|--------------|
| [name] | [behavior] | [what PASS looks like] |

---

## Rollback Criteria

<!-- When to revert the changes. -->

- Revert if composite score drops below [X.X]
- Revert if any dimension drops more than 0.5 from current score
- Revert if new failure modes appear that did not exist in the original assessment

---

## Sign-off

- [ ] Directive reviewed before implementation
- [ ] Changes implemented in agent file
- [ ] Re-assessment scheduled
- [ ] Version bumped in agent frontmatter
- [ ] Changelog updated in agent file
