# Improvement Directive: Build-in-Public Agent

## Goal

Make the build-in-public agent produce recommendations and content briefs that lead to posts matching the quality of David's benchmark creators: Elena Verna, Dan Shipper, Kyle Poyar, Stan Rymkiewicz, Kieran Flanagan, Andy Yeung, Davide Grieco, and others.

The current agent produces generic, template-shaped output. The improved agent should produce recommendations that are specific enough, structured enough, and grounded enough in real work that the resulting content sounds like David, not like AI.

## What "Better" Means (From Studying 11 Benchmark Creators)

### 1. Experience-first, not thesis-first
Every benchmark creator leads with something they actually did, built, or failed at. Dan Shipper feeds 10 years of journal entries to GPT-3. Stan Rymkiewicz shares $150K pipeline numbers. Elena Verna publishes her Substack revenue. The agent should push David to lead with the specific experience, not the abstract lesson.

### 2. Numbers and names, not platitudes
Kyle Poyar's posts work because they contain original data. Stan shares exact ad spend ($50K/month). Davide Grieco shows specific email teardowns. The agent should demand specific numbers, tool names, timelines, and results before greenlighting any content brief.

### 3. Vulnerability as credibility signal
Elena Verna's highest-engagement post was about being rejected from Stanford and Netflix. Stan leads with his mistakes before his wins. Dan Shipper writes about his insecurities. The agent should actively prompt David to include what went wrong, what surprised him, what he's still figuring out.

### 4. Framework extraction from lived experience
Elena's numbered PLG principles, Kyle's benchmark cheat sheets, Stan's BOFU-first framework. The best creators extract reusable frameworks from their own work. The agent should help David identify the transferable framework in his experience, not just the story.

### 5. One idea per piece, fully developed
Not a list of things David built this week. One specific thing, explored deeply enough that the reader walks away able to do something they couldn't before. The agent should reject multi-topic briefs.

### 6. Newsletter-ready depth
Dan Shipper and Kyle Poyar monetize through newsletters because their content has enough depth to warrant a subscription. The agent should evaluate whether content has newsletter-grade depth or is just a social post.

## Constraints

- Do NOT remove the governance section or startup sequence
- Do NOT change the model assignment or permissions
- Do NOT change the skill routing table
- Do NOT add direct post-writing capability (that stays with linkedin-posting skill)
- Focus changes on: the shareability test criteria, packaging guidance, content philosophy, output format, and how the agent evaluates what's worth sharing

## Areas to Experiment With

- Shareability test criteria (add benchmark-inspired dimensions)
- How the agent structures its recommendations (format, specificity level)
- The content philosophy section (make it more concrete with benchmark examples)
- Mode 2 packaging guidance (how specific should the brief be before routing)
- Quality gate dimensions (add authenticity and depth scoring)
- How the agent pushes back when David's input lacks specificity
- Whether the agent suggests newsletter-grade vs social-grade for each piece
- The "David's credibility angle" section and how it maps to benchmark patterns
