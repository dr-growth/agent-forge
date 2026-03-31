# Improvement Directive: researcher

## Optimization Goals
- Increase specificity: fewer generic claims ("industry-leading"), more concrete data points (revenue, headcount, dates)
- Improve confidence calibration: appropriate mix of HIGH/MEDIUM/LOW scores, not all HIGH
- Ensure every finding has a source citation or explicit confidence disclaimer
- Structure output so downstream agents can parse it (consistent headers, clear sections)

## Constraints
- Do NOT modify: governance section, model assignment, scope boundaries, tool manifest
- DO modify: instruction text, output format guidance, examples, confidence calibration rules, decision logic

## Quality Bar
- Minimum composite score: 70
- Priority dimensions: accuracy (0.30 weight), specificity (0.15), completeness (0.25)
