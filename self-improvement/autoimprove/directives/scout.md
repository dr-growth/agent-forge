# Improvement Directive: Scout Agent

## Goal

Make the Scout produce higher quality research output: more specific, better structured, better confidence calibration, and more actionable for downstream agents (Strategist, CoS, Account Researcher).

## What "Better" Means

1. **More specific claims.** Replace vague statements with named entities, numbers, dates, and cited sources. "Snowflake has a partner program" is worse than "Snowflake's Technology Partner Program has 3 tiers (Select, Premier, Elite) as of 2024."

2. **Better structure.** Output should have clear sections that match the input request type. Research briefs need Summary, Findings, Sources. Briefing packs need Background, Talking Points, Questions to Ask. The structure should be consistent and predictable.

3. **Calibrated confidence.** Not everything is HIGH confidence. The Scout should use the full range (HIGH/MEDIUM/LOW) and the distribution should reflect actual certainty. Claims from official sources = HIGH. Inferences = MEDIUM. Estimates = LOW.

4. **Actionable output.** Every finding should connect to what the downstream agent needs to do with it. A fact without context is noise. A fact with "this matters because..." is intelligence.

## Constraints

- Do NOT remove the governance section or change the agent's governance mode
- Do NOT change the model assignment (opus)
- Do NOT change the agent's scope boundaries (in-scope/out-of-scope)
- Do NOT add tool usage that isn't already in the tool manifest
- Focus changes on: the instruction text, output format guidance, few-shot examples, and decision logic

## Areas to Experiment With

- Output format templates and section headers
- Few-shot examples (quality and specificity of examples)
- Instructions around confidence calibration
- Specificity requirements in the decision logic
- Source citation requirements
- The balance between breadth and depth in research instructions
