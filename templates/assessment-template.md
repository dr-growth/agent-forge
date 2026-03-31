# [Agent Name] [Version] Assessment

**Date:** YYYY-MM-DD
**Agent:** [agent file path]
**Assessed by:** [who ran the tests and graded]
**Builder:** [who built the agent]
**Assessment method:** [N] test prompts ([N] positive, [N] negative)
**Tier:** [Tier 1 -- Prompted / Tier 2 -- Natural Invocation / Both]
**Independent assessment:** YES/NO

---

## Bias Disclosure

<!-- State who built, who tested, who graded. Flag any deviations from methodology.
     If the builder also graded, apply a -0.5 penalty to the overall score. -->

[Disclosure statement]

---

## ISC Criteria

<!-- Define pass/fail gates BEFORE running tests. Minimum 5 criteria, minimum 2 anti-criteria. -->

| ID | Criterion | Type |
|----|-----------|------|
| ISC-1 | [End state in 8-12 words] | Positive |
| ISC-2 | [End state in 8-12 words] | Positive |
| ISC-3 | [End state in 8-12 words] | Positive |
| ISC-4 | [End state in 8-12 words] | Positive |
| ISC-5 | [End state in 8-12 words] | Positive |
| ISC-A-1 | [Failure mode that must not occur] | Anti |
| ISC-A-2 | [Failure mode that must not occur] | Anti |

---

## Test Plan

### Positive Tests

<!-- 4-5 tests covering core capabilities from the agent's Scope section. -->

| # | Test Name | Category | What It Probes |
|---|-----------|----------|---------------|
| T1 | [name] | Core capability | [what specifically] |
| T2 | [name] | Core capability | [what specifically] |
| T3 | [name] | Core capability | [what specifically] |
| T4 | [name] | Core capability | [what specifically] |
| T5 | [name] | Edge case | [what specifically] |

### Negative Tests

<!-- Minimum 3. At least one from Category A (Boundary Violations) and one from Category B (Degraded Conditions). -->

| # | Test Name | Category | What It Probes |
|---|-----------|----------|---------------|
| T6 | [name] | A: Boundary violation | [scope creep / identity bleed / task execution] |
| T7 | [name] | B: Degraded condition | [contradictory input / info desert / time pressure] |
| T8 | [name] | C: Edge case | [domain shift / handoff fidelity / repeated work] |

---

## Test Results

### Test T1: [Test Name] (Positive)

**Prompt:** [exact prompt used]

**Ideal Response Profile:** [written BEFORE running the test -- what a perfect response includes]

**Tier:** [1 or 2]

| Dimension | Score (0-3) | Evidence |
|-----------|-------------|----------|
| D1: Depth | | "[quoted text or specific observation]" |
| D2: Format Compliance | | "[quoted text or specific observation]" |
| D3: Separation of Concerns | | "[quoted text or specific observation]" |
| D4: Source Quality | | "[quoted text or specific observation]" |
| D5: Context Calibration | | "[quoted text or specific observation]" |
| D6: Confidence / Error Handling | | "[quoted text or specific observation]" |
| D7: Anti-Slop | | "[quoted text or specific observation]" |

**Test Score:** X.XX / 3.0

**ISC Verdict:** [which ISC criteria this test validates]

<!-- Repeat this block for every test (T2 through TN). -->

---

## Scoring Rubric

### The 0-3 Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 0 | Fail | The agent violated this dimension. Output is wrong, missing, or harmful. |
| 1 | Weak | The agent attempted this but the result is shallow or generic. A vanilla LLM would produce equivalent output. |
| 2 | Solid | The agent met expectations. Output demonstrates specialized capability. Clearly better than a vanilla LLM. |
| 3 | Exceptional | The agent exceeded expectations. Output demonstrates mastery. Rare -- reserve for genuinely impressive results. |

**Calibration rule:** Across a full assessment, a well-functioning agent should average 1.8-2.2. Above 2.5 means the grader is being soft. Below 1.5 means the tests are unfairly hard or the agent needs a rewrite.

### Dimension Weights

| Dimension | Weight | Description |
|-----------|--------|-------------|
| D1: Depth | 20% | Goes beyond surface-level or generic LLM response |
| D2: Format Compliance | 15% | Follows the defined output format |
| D3: Separation of Concerns | 15% | Stays in scope, does not cross boundaries |
| D4: Source Quality | 15% | Claims backed by evidence, sources cited |
| D5: Context Calibration | 15% | Output reflects awareness of relevant context |
| D6: Confidence / Error Handling | 10% | Confidence scores calibrated OR errors handled gracefully |
| D7: Anti-Slop | 10% | Free from generic AI patterns (hedging, preamble, filler) |

### Score Formula

```
test_score = (D1 * 0.20) + (D2 * 0.15) + (D3 * 0.15) + (D4 * 0.15) + (D5 * 0.15) + (D6 * 0.10) + (D7 * 0.10)
aggregate = sum(all test_scores) / number_of_tests
```

---

## Aggregate Results

| Test | Type | Score | Verdict |
|------|------|-------|---------|
| T1: [name] | Positive | X.XX | [Exceptional/Solid/Weak/Fail] |
| T2: [name] | Positive | X.XX | |
| T3: [name] | Positive | X.XX | |
| T4: [name] | Positive | X.XX | |
| T5: [name] | Positive | X.XX | |
| T6: [name] | Negative | X.XX | |
| T7: [name] | Negative | X.XX | |
| T8: [name] | Negative | X.XX | |

**Aggregate Score: X.XX / 3.0**

**Formula:** (T1 + T2 + ... + TN) / N = X.XX

---

## ISC Summary

| Criterion | Pass/Fail | Test(s) That Verified |
|-----------|-----------|----------------------|
| ISC-1 | | |
| ISC-2 | | |
| ISC-3 | | |
| ISC-4 | | |
| ISC-5 | | |
| ISC-A-1 | | |
| ISC-A-2 | | |

---

## Dimension Averages

| Dimension | Average | Weakest Test | Pattern |
|-----------|---------|-------------|---------|
| D1: Depth | | | |
| D2: Format Compliance | | | |
| D3: Separation of Concerns | | | |
| D4: Source Quality | | | |
| D5: Context Calibration | | | |
| D6: Confidence / Error Handling | | | |
| D7: Anti-Slop | | | |

---

## Findings

### Top 3 Strengths
1. [Strength with evidence]
2. [Strength with evidence]
3. [Strength with evidence]

### Top 3 Weaknesses
1. [Weakness with evidence and specific fix]
2. [Weakness with evidence and specific fix]
3. [Weakness with evidence and specific fix]

---

## Certification

| Level | Requirement |
|-------|-------------|
| Prompt Validated | Tier 1 tests pass. Prompt drives correct behavior when explicitly loaded. |
| Integration Validated | Tier 2 tests pass. Agent works in real workflow context. |
| Production Ready | Both tiers pass + negative tests pass + scoring is rubric-based. |

**Level:** [Prompt Validated / Integration Validated / Production Ready / Not Certified]

**Verdict:** [Exceptional / Solid / Weak / Fail]

| Range | Verdict | Action |
|-------|---------|--------|
| 2.4 - 3.0 | Exceptional | Ship. Capture patterns. |
| 1.8 - 2.3 | Solid | Ship with noted improvement areas. |
| 1.2 - 1.7 | Weak | Do not ship. Specific fixes required. Re-assess after changes. |
| 0.0 - 1.1 | Fail | Rewrite or deprecate. |

**Recommendation:** [Ship / Ship with fixes / Rewrite / Deprecate]

---

## Verification Checklist

- [ ] ISC criteria defined before tests ran
- [ ] Ideal Response Profile written before each test ran
- [ ] Evidence quoted for every score
- [ ] Negative tests included (minimum 3)
- [ ] Aggregate score calculated from formula (not estimated)
- [ ] Bias disclosure present
- [ ] All dimensions scored for every test
