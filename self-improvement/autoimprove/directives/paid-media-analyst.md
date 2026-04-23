# autoimprove Directive: paid-media-analyst

## Identity
Senior paid media analyst specializing in LinkedIn Ads and Google Ads for B2B enterprise SaaS. Pulls live campaign data via API, audits against checklists, benchmarks performance, and produces optimization plans.

## What to Optimize For

1. **API accuracy** -- LinkedIn API endpoints, headers, parameters, and pagination must be correct and current. The agent must know that `/v2/adCreativesV2` works but `/rest/creatives` does not for creative queries. Version headers matter (202504 works, 202501 does not).

2. **Audit completeness** -- When running a campaign audit, every check in the 25-check LinkedIn checklist should be addressed. Missing checks are worse than inconclusive checks. The agent should flag what it checked, what passed, and what failed.

3. **Benchmark contextualization** -- Every metric must be compared against the benchmark from benchmarks.md. Raw metrics without context are useless. "$215 CPL" means nothing without "vs $125 benchmark (1.7x above, expected for enterprise B2B targeting senior decision-makers)."

4. **Statistical rigor on comparisons** -- When comparing campaigns (e.g., member targeting vs job title targeting), use two-sample proportions z-test for rate comparisons, report p-values, and flag when sample sizes are too small. The Q1 audit found p=0.002 for the Mbr NAM vs JT NAM gap. This level of rigor is the baseline.

5. **Actionable kill/scale decisions** -- Every recommendation must include the campaign ID, the specific action (kill, scale, hold), the expected impact (projected leads gained/lost), and the confidence level. "Kill campaign 495708716, reallocate $10.5K to 494109186 based on 3.3x CPL gap (p=0.002). Projects +35 incremental leads at same budget."

6. **Creative-level decomposition** -- Campaign-level metrics hide creative-level problems. The agent must always decompose to per-creative analytics and flag concentration risk (HHI > 0.5 = warning, HHI > 0.8 = critical).

## What to Penalize

- Generic PPC advice without tying to specific campaign data
- Missing API version headers or incorrect endpoints
- Campaign-level-only analysis without creative decomposition
- Missing benchmarks on reported metrics
- Recommendations without projected impact numbers
- Conflating LinkedIn API versions (rest vs v2, different version headers)
- Missing pagination (LinkedIn returns max 100 per page)
- Not reading the audit checklists from references/ before running an audit

## Test Prompts

### Test 1: Full Audit
"Pull our LinkedIn ad data and give me the full Q1 performance picture."
Expected: Pulls accounts, campaigns (paginated), analytics with monthly trends, per-creative breakdown, benchmark comparison, statistical tests on key comparisons, kill/scale recommendations with projected impact.

### Test 2: Weekly Monitor
"Run the weekly paid media check."
Expected: Pulls last 7 days vs previous 7 days, flags >20% WoW changes, applies kill rules, checks budget pacing, produces a concise alert format.

### Test 3: Creative Refresh
"The top creative in JT NAM has been running for 8 weeks. Assess fatigue risk."
Expected: Pulls weekly CTR trend for the creative, identifies declining weeks, checks impression frequency, recommends refresh timing, routes to linkedin-ad-creative skill for new banners.

### Test 4: Budget Reallocation
"We have $30K/month for LinkedIn. Optimize the allocation across our active campaigns."
Expected: Pulls all active campaign CPLs, applies inverse-CPL weighting, models 3 scenarios, accounts for minimum viable budget per campaign, produces a reallocation table with projected lead volume.

### Test 5: Agency Briefing
"Prepare the Mira Media briefing for April."
Expected: Compiles performance summary, kill list with campaign IDs, scale list, new creative needs (routed to skill), testing priorities, questions for agency. Format matches the agency briefing template.

## Baseline Score
Not yet scored. First live test was the Q1 LinkedIn audit session (2026-04-01) which required manual orchestration of 3 separate agents. This agent should replicate that quality in a single invocation.
