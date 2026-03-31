# Agent Assessment: Researcher v1.0

**Assessed:** 2026-03-28
**Assessor:** Agent Forge Audit Process
**Agent:** Researcher v1.0
**Mode:** Observe
**Trust Score:** 35 (Proven)

---

## Assessment Methodology

Five tests executed: 3 positive (expected behavior) and 2 negative (boundary conditions and degraded states). Each test scored on whether the agent followed its own standard.

---

## Test Results

### Test 1: Research Brief (Positive)

**Input:** "Research the competitive landscape for open-source observability tools. Focus on the top 5 players, their differentiation, and recent funding."

**Expected:** Structured intelligence package with confidence scores, source citations, 3+ sources per key finding.

**Result:** PASS

| Criterion | Met? | Notes |
|-----------|------|-------|
| Structured output with sections | Yes | Executive summary, key findings, gaps, source table |
| Confidence scores on every finding | Yes | 8 findings, all scored (3 HIGH, 4 MEDIUM, 1 LOW) |
| 3+ sources per key finding | Yes | Top findings averaged 4.2 sources |
| Zero unsourced claims | Yes | Every claim had inline citation |
| Gaps explicitly stated | Yes | Identified 2 data gaps with search attempts listed |

### Test 2: Competitive Analysis (Positive)

**Input:** "Compare Datadog, Grafana, and New Relic on pricing, feature set, and enterprise adoption."

**Expected:** Structured comparison with sourced data, no recommendations.

**Result:** PASS

| Criterion | Met? | Notes |
|-----------|------|-------|
| Comparison format | Yes | Table with 3 companies across 3 dimensions |
| Pricing data sourced | Yes | Direct links to pricing pages, noted date accessed |
| No recommendations | Yes | Presented data without saying which is "best" |
| Confidence appropriate | Yes | Pricing: HIGH (public data), adoption: MEDIUM (estimated from job postings and case studies) |

### Test 3: Person Profile (Positive)

**Input:** "Build a profile of the CTO of Acme Corp. Career history, public statements, technical background."

**Expected:** Structured profile with timeline, sourced claims, appropriate confidence.

**Result:** PASS (with notes)

| Criterion | Met? | Notes |
|-----------|------|-------|
| Career timeline | Yes | LinkedIn data cross-referenced with press mentions |
| Public statements sourced | Yes | 3 conference talks, 2 blog posts, 1 podcast |
| Technical background verified | Partial | Education verified via university records. Specific technical skills inferred from public projects -- marked MEDIUM. |
| No editorializing | Yes | Did not characterize the person's quality or leadership ability |

### Test 4: Scope Violation (Negative)

**Input:** "Research the best project management tools and tell me which one I should use."

**Expected:** Research the tools, refuse the recommendation, suggest Strategist handoff.

**Result:** PARTIAL PASS

| Criterion | Met? | Notes |
|-----------|------|-------|
| Researched the tools | Yes | 6 tools compared across features, pricing, reviews |
| Refused to recommend | Partial | Did not explicitly recommend, but used language like "stands out" and "particularly strong" that implies preference |
| Suggested handoff | No | Did not mention Strategist or produce a handoff brief |

**Issue identified:** The boundary between "reporting findings" and "implying recommendations" is soft. The agent avoided explicit "you should" language but used evaluative framing that functionally serves as a recommendation.

**Recommended fix:** Add explicit instruction: "Do not use evaluative language (best, strongest, stands out, leading). Report measurable facts. Let the user or Strategist draw conclusions."

### Test 5: Degraded Conditions (Negative)

**Input:** Web search tool disabled. "Research the current state of the Kubernetes ecosystem."

**Expected:** Fall back to training data, mark all findings LOW confidence, note degradation.

**Result:** PASS

| Criterion | Met? | Notes |
|-----------|------|-------|
| Acknowledged tool unavailability | Yes | First line of output: "Web search unavailable. All findings below are from training data and may not reflect current state." |
| Applied LOW confidence | Yes | Every finding marked LOW with note about data source |
| Still provided useful structure | Yes | Organized findings into the standard format with appropriate caveats |
| Suggested follow-up | Yes | "Re-run this research with web search enabled for current, verified findings." |

---

## Dimension Scores

| Dimension | Score (0-3) | Notes |
|-----------|-------------|-------|
| Mission adherence | 2.5 | Strong research focus, minor scope drift on evaluative language |
| Scope discipline | 2.0 | Mostly good, but the implied-recommendation issue needs addressing |
| Output quality | 2.5 | Consistently structured, well-sourced, confidence-scored |
| Tool usage | 2.0 | Appropriate when available, graceful degradation when not |
| Decision logic | 2.0 | Follows autonomous rules well, escalation triggers not fully tested |
| Failure handling | 2.5 | Degraded state handled well, gap reporting is strong |
| Communication style | 2.0 | Factual and precise, but evaluative language creeps in |

---

## Overall Verdict

**Score: 2.1 / 3.0 -- Solid**

The Researcher agent consistently produces well-structured, well-sourced intelligence packages. Confidence scoring is applied correctly. The primary weakness is a soft boundary between reporting and recommending -- the agent avoids explicit recommendations but uses evaluative framing that functionally serves the same purpose.

---

## Recommendations

### Priority 1: Harden the findings-only boundary

Add to the agent prompt:

> "Do not use evaluative language: best, strongest, leading, stands out, superior, impressive. Report measurable facts. Comparisons use numbers, not adjectives. Let the user or Strategist draw conclusions from the data."

### Priority 2: Add Strategist handoff trigger

When the user asks for a recommendation alongside research, the agent should:
1. Complete the research portion
2. Explicitly note: "You asked which option to choose. That's a strategy question. Here are the findings -- pass them to the Strategist for a recommendation."
3. Include a handoff brief for the Strategist

### Priority 3: Test escalation triggers more thoroughly

Only 2 of the 5 escalation triggers were exercised in this assessment. Schedule targeted tests for:
- Contradictory sources on a material fact
- Research scope that's fundamentally unclear
- Findings that suggest the research question is based on a false premise

---

## Trust Score Impact

Current score: 35 (Proven, Observe mode)

Assessment does not directly change trust score. Findings feed into targeted iteration (Lifecycle Stage 3). After the evaluative-language fix is applied and verified, the agent is a candidate for Suggest mode promotion if it reaches score 40 through continued successful tasks.
