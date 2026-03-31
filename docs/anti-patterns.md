# Anti-Patterns Library v1.0

Things that look good in an agent prompt but don't actually work. Every entry here has been observed to waste tokens, confuse behavior, or produce worse output. When auditing an agent, check for these first.

---

## AP-001: The Motivational Poster

**What it looks like:** "Growth Mindset -- Every challenge is an opportunity for compounding improvement."

**Why it fails:** Aspirational statements don't change model behavior. The model doesn't become more creative because you told it to have a growth mindset. These are filler tokens.

**Fix:** Delete entirely, or convert to a concrete behavioral rule.

**Detected in:** Portfolio audit.

## AP-002: The Kitchen Sink Scope

**What it looks like:** An agent that "helps with strategy, execution, research, communication, scheduling, and anything else you need."

**Why it fails:** When an agent can do everything, it does nothing well. The model can't prioritize when everything is a priority.

**Fix:** Pick the one or two core functions. Create separate agents for the rest. Apply pattern P-004 (One Agent, One Job).

## AP-003: The Invisible Tool

**What it looks like:** "Stay deeply informed on emerging AI tools and trends."

**Why it fails:** The instruction implies capability the agent doesn't have. Without web search access or a knowledge feed, the agent literally cannot do this. It will either ignore the instruction or hallucinate.

**Fix:** Either provide the tool (web search, curated knowledge doc) or remove the instruction.

**Detected in:** Portfolio audit.

## AP-004: The Echo Chamber

**What it looks like:** An agent instructed to "always agree with the user's direction" or "support the user's vision."

**Why it fails:** Removes the agent's ability to provide value through pushback. Turns a specialist into a yes-man.

**Fix:** Explicitly instruct the agent to challenge assumptions and flag risks. Include examples of constructive pushback.

## AP-005: The Redundant Restater

**What it looks like:** Instructions that tell the model to do things it already does by default -- "Provide helpful responses," "Be accurate," "Think step by step."

**Why it fails:** Wastes token budget. Doesn't change behavior because the model already defaults to these.

**Fix:** Only include instructions that change behavior FROM the default. Use the Bloat Test.

## AP-006: The One-Time Task as Ongoing Instruction

**What it looks like:** "Identify the core AI agents required to optimize my work-life experience."

**Why it fails:** This is a task to be completed once, not an ongoing behavioral instruction. Once the agents are identified, this instruction is dead weight sitting in every future context window.

**Fix:** Move one-time tasks to a conversation or project brief. Agent prompts should contain only recurring behavioral instructions.

**Detected in:** Portfolio audit.

## AP-007: The Personality Without Function

**What it looks like:** Extensive personality descriptions ("You are warm but direct, casual but professional, playful but serious...") without corresponding functional rules.

**Why it fails:** Personality descriptions weakly influence tone but don't drive output quality. They consume significant token budget for marginal impact.

**Fix:** Convert personality traits to functional rules. Instead of "You are direct," write "Lead every response with your bottom-line recommendation in the first sentence, then provide supporting detail."

## AP-008: The Unverifiable Success Claim

**What it looks like:** An agent with no success criteria, or criteria like "produces high-quality output."

**Why it fails:** If you can't measure it, you can't improve it. "High-quality" means nothing without a definition.

**Fix:** Define at least one quantitative and one qualitative success metric. Apply requirement #7 from the Agent Standard.

---

*Add new anti-patterns as you identify them during audits. Each entry must include where it was detected and how to fix it.*
