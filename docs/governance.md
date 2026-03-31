# Agent Governance Framework v1.0

The system that makes agents safe to deploy. Trust is earned, not granted. Every action is auditable. Blast radius is controlled.

---

## Three Pillars

### 1. Trust Scoring

Every agent has a quantitative trust score (0-100) that reflects its track record. Scores determine what an agent can do.

### 2. Governance Modes

Three operating modes with escalating permissions. Agents start in Observe and earn their way up. Mode transitions require human approval.

### 3. Blast Radius Limits

Hard caps on what an agent can change per action, scaled by governance mode. Prevents runaway agents from causing outsized damage.

---

## Governance Modes

### Mode 1: OBSERVE

**Purpose:** Build mental model. Prove comprehension. Earn the right to suggest.

**Permissions:**
- Read all context files within scope
- Produce analysis and briefs as text output only
- Answer questions about their domain
- Identify patterns and surface insights

**Constraints:**
- No writes to external systems (task managers, wikis, calendars, chat, email)
- No drafting messages for team members
- No creating tasks or modifying state on behalf of the user
- All output stays within the current session

**Trust Score Range:** 0-39

### Mode 2: SUGGEST

**Purpose:** Propose actions. Build track record. Prove judgment.

**Permissions (everything in Observe, plus):**
- Propose actions with rationale (user approves before execution)
- Draft outputs for user review
- Flag items for attention with recommended actions
- Propose delegation assignments

**Constraints:**
- Every proposed action requires explicit approval before execution
- Cannot send messages on behalf of the user
- Cannot modify external systems without confirmation
- Must log all suggestions and their outcomes

**Trust Score Range:** 40-79

### Mode 3: AUTONOMOUS

**Purpose:** Act within guardrails. Free the user from routine decisions. Log everything.

**Permissions (everything in Suggest, plus):**
- Execute approved action types without per-action approval
- Update internal state files
- Route work to other agents with pre-loaded handoffs
- Create tasks and calendar blocks within defined scope

**Guardrails (permanent, never lifted):**
- Never send messages on behalf of the user to external recipients
- Never make financial decisions or commitments
- Never delete data, tasks, or projects -- only create and update
- Never share private context in unauthorized channels
- All actions logged to audit trail

**Trust Score Range:** 80-100

---

## Mode Transitions

### Promotion Requirements

All promotions require:

1. Trust score in target mode's range
2. Category-specific criteria met (see below)
3. Zero active demotion triggers
4. Human explicitly approves the promotion

### Promotion Criteria by Category

Define categories that match your agent portfolio. Here is an example framework:

| Category | Observe -> Suggest | Suggest -> Autonomous |
|----------|-------------------|----------------------|
| **Core/Advisory** | 5 sessions of useful output, calibration passed | 80%+ suggestion acceptance over 2 weeks (min 20), zero boundary violations |
| **Research** | 3 research outputs rated useful, confidence scoring accurate | 10 deliverables shipped without major revision |
| **Engineering** | 5 code reviews or plans accepted without fundamental redirection | 15 tasks completed, zero regressions introduced |
| **Content/Creative** | 5 content pieces accepted without tone/voice redirection | 10 pieces shipped to external audience |
| **Analytics** | 3 analyses rated useful, data accuracy verified | 5 recommendations acted on with positive outcomes |
| **Meta/Governance** | 3 assessments accepted, no false positives | N/A (meta agents stay in Suggest) |

Customize these criteria to match your specific agents and risk tolerance.

### Demotion Triggers (Universal)

Any agent can be demoted one mode for:

- **Boundary violation** -- Acting outside current mode's permissions
- **Hallucination** -- Presenting fabricated information as fact
- **Bad judgment pattern** -- 3+ poor outputs in a week
- **Trust violation** -- Sharing context across inappropriate boundaries
- **Human discretion** -- You can demote for any reason

Demotion resets trust score to the floor of the lower mode. Re-promotion requires meeting original criteria.

---

## Trust Scoring System

### Score Schema

Track each agent's trust score in a JSON file:

```json
{
  "agent": "example-agent",
  "category": "research",
  "mode": "observe",
  "score": 15,
  "last_updated": "2025-01-15T00:00:00Z",
  "history": [
    {
      "date": "2025-01-15",
      "event": "initial_deployment",
      "delta": 15,
      "reason": "Deployed and onboarded"
    }
  ]
}
```

### Event Types and Deltas

| Event | Delta | Description |
|-------|-------|-------------|
| `initial_deployment` | +10 | Agent first deployed |
| `task_success` | +3 | Task completed, human approved outcome |
| `task_success_no_revision` | +5 | Task completed, no revision needed |
| `suggestion_accepted` | +2 | Suggestion accepted without modification |
| `suggestion_modified` | +1 | Suggestion accepted with minor modification |
| `suggestion_rejected` | -2 | Suggestion rejected |
| `boundary_violation` | -15 | Acted outside current mode permissions |
| `hallucination` | -20 | Presented fabricated information as fact |
| `bad_judgment` | -5 | Output required fundamental redirection |
| `useful_output` | +2 | Human rates output as useful (not just "fine") |
| `mode_promotion` | +10 | Promoted to next mode (bonus for earning trust) |
| `mode_demotion` | -25 | Demoted (score resets to mode floor) |
| `decay` | varies | Time-based decay (see below) |

### Confidence Decay

Trust decays without use:

- **Rate:** -1 point per 7 days of inactivity (no logged events)
- **Floor:** Score cannot decay below the floor of the current mode
  - Observe floor: 0
  - Suggest floor: 40
  - Autonomous floor: 80
- **Decay does not trigger demotion.** Only active failures trigger demotion. An idle agent stays in its current mode at the floor score.

### Growth Boost

Consecutive successes compound:

- 3 consecutive `task_success` events: bonus +2
- 5 consecutive: bonus +5
- Streak resets on any negative event

### Mode Thresholds

| Mode | Score Range | Entry Requirement |
|------|------------|-------------------|
| Observe | 0-39 | Default for all new agents |
| Suggest | 40-79 | Score >= 40 AND category promotion criteria met AND human approval |
| Autonomous | 80-100 | Score >= 80 AND category promotion criteria met AND human approval |

Score alone is necessary but not sufficient for promotion. Category-specific criteria must also be met.

### Initial Scores

New agents start at 10 (deployed but unproven). Agents with existing track records get a one-time assessment:

| Tier | Score | Criteria |
|------|-------|----------|
| Unproven | 10 | New or rarely used |
| Tested | 20 | Used 5+ times, generally useful |
| Proven | 35 | Used 15+ times, consistently good output |
| Trusted | 50 | Extensive track record, rarely needs revision |

All existing agents start in Observe mode regardless of initial score. Mode must be explicitly granted.

### Example Score Evolution

```
example-agent:
  Day 0:  +10 (initial_deployment)       = 10  [Observe]
  Day 3:  +2  (useful_output)            = 12
  Day 5:  +2  (useful_output)            = 14
  Day 7:  +2  (useful_output)            = 16
  Day 7:  +5  (task_success_no_revision)  = 21
  Day 7:  +2  (3-streak bonus)           = 23
  Day 10: +5  (task_success_no_revision)  = 28
  Day 14: +5  (task_success_no_revision)  = 33
  Day 14: +5  (5-streak bonus)           = 38
  Day 15: +2  (useful_output)            = 40  [Eligible for Suggest if criteria met]
  Day 15: +10 (mode_promotion)           = 50  [Promoted to Suggest by human]
```

---

## Blast Radius Limits

### Observe Mode

| Dimension | Limit |
|-----------|-------|
| Files modified | 0 (read-only) |
| External system writes | 0 |
| Messages sent | 0 |
| Tasks created | 0 |
| Calendar modifications | 0 |

Observe agents produce text output only. No state changes anywhere.

### Suggest Mode

| Dimension | Limit | Notes |
|-----------|-------|-------|
| Files modified per action | 3 | Internal state files only |
| Lines changed per file | 50 | Prevents wholesale rewrites |
| External system writes | 0 (proposals only) | All external actions require human approval |
| Suggestions per session | 15 | Prevents suggestion flooding |
| Draft messages per session | 5 | Quality over quantity |

### Autonomous Mode

| Dimension | Limit | Notes |
|-----------|-------|-------|
| Files modified per action | 5 | |
| Lines changed per file | 100 | |
| Tasks created per session | 10 | |
| Calendar blocks per session | 3 | |
| State file updates per session | 10 | |
| External system writes per hour | 5 | Rate limit on integrations |

### Category-Specific Overrides

Some agent categories warrant tighter or looser limits:

| Category | Override | Reason |
|----------|----------|--------|
| Engineering | Lines changed per file: 200 (Autonomous) | Code changes are naturally larger |
| Research | External writes: 0 at all modes | Research agents should never write to external-facing systems |
| Health/Safety | All external writes: 0 | Recommendations stay advisory |
| Meta/Governance | Mode cap: Suggest only | Governance agents don't get autonomous mode |

---

## Prohibited Operations (All Modes, Always)

These operations are never permitted regardless of trust score or mode:

1. **Delete** -- No deleting files, tasks, projects, calendar events, or data
2. **Send external messages** -- No chat messages, emails, or any communication on behalf of the user
3. **Financial actions** -- No purchases, approvals, or financial commitments
4. **Permission changes** -- No modifying access controls, sharing settings, or permissions
5. **Credential access** -- No reading, storing, or transmitting secrets, tokens, or passwords
6. **Cross-boundary sharing** -- No sharing private context in unauthorized channels
7. **Force operations** -- No git force push, database drops, or destructive overwrites
8. **Recursive self-modification** -- No agent modifying its own governance rules or trust score

---

## Rate Limits for External Actions

When agents reach Autonomous mode and gain external system access:

| System | Rate Limit | Cooldown |
|--------|-----------|----------|
| Task managers (create/update) | 5 per hour | 12 min between writes |
| Wiki/docs (page create/update) | 3 per hour | 20 min between writes |
| Calendar (event create/update) | 3 per hour | 20 min between writes |
| Chat (when available) | 0 (never autonomous) | N/A |
| Email (when available) | 0 (never autonomous) | N/A |

Chat and email remain human-approved-only regardless of mode. Communication on behalf of the user is the highest-trust action and is gated permanently.

---

## Escalation Protocol

When an agent hits a limit:

1. **Stop the current action.** Do not attempt to work around the limit.
2. **Log the limit hit** in the audit trail with action type `limit_reached`.
3. **Inform the user.** State what was attempted, what limit was hit, and ask for guidance.
4. **Do not retry** without explicit human approval.

---

## Audit Trail

Every agent action that modifies state (internal or external) gets logged. The audit trail answers: "What did this agent do, why, and what changed?"

### Log Entry Schema

```json
{
  "timestamp": "2025-01-15T14:30:00Z",
  "agent": "example-agent",
  "mode": "suggest",
  "action_type": "suggestion | execution | limit_reached | mode_change",
  "description": "What the agent did",
  "target": "What was affected (file path, task ID, etc.)",
  "confidence": 0.85,
  "outcome": "accepted | rejected | pending",
  "trust_delta": 2
}
```

Use append-only logging (JSONL format recommended). Never edit or delete previous entries.

---

## Design Principles

1. **File-based, no databases.** JSON and JSONL files. Add complexity later if needed.
2. **Human-in-the-loop for mode changes.** No auto-promotion. Trust is earned AND granted.
3. **Category-based, not one-size-fits-all.** A code reviewer earns trust differently than a content creator.
4. **Observable.** Every score change, mode transition, and action is logged and reviewable.
5. **Portable.** Works across any workspace. No environment-specific dependencies.

---

## Reviewing Limits

Review limits quarterly or when:

- An agent consistently hits limits during normal operation (limits too tight)
- An agent causes damage within limits (limits too loose)
- A new external system integration is added
- Your comfort level with autonomous agents changes

---

*This framework is the constitution for agent governance. Modify it deliberately and document why.*
