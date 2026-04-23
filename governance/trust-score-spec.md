# Trust Score Specification v1.0

Quantitative backing for agent governance modes. Every agent has a score between 0 and 100 that reflects its track record.

Last updated: 2026-03-26

---

## Score Schema

Each agent entry in `trust-scores.json`:

```json
{
  "agent": "chief-of-staff",
  "cluster": "inner-circle",
  "mode": "observe",
  "score": 15,
  "last_updated": "2026-03-26T00:00:00Z",
  "history": [
    {
      "date": "2026-03-26",
      "event": "initial_deployment",
      "delta": 15,
      "reason": "Deployed with Module 1 complete"
    }
  ]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `agent` | string | Agent name (matches filename in ~/.claude/agents/) |
| `cluster` | string | Cluster from agent registry |
| `mode` | string | Current governance mode: observe, suggest, autonomous |
| `score` | number | Current trust score (0-100) |
| `last_updated` | ISO 8601 | When score was last modified |
| `history` | array | Chronological log of score changes |

### History Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date of event (YYYY-MM-DD) |
| `event` | string | Event type (see Event Types below) |
| `delta` | number | Score change (positive or negative) |
| `reason` | string | Human-readable explanation |

---

## Score Calculation

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
| `mode_demotion` | -25 | Demoted (score resets to mode floor, this is the delta from wherever they were) |
| `decay` | varies | Time-based decay (see below) |

### Confidence Decay

Inspired by Ruflo's SONA model. Trust decays without use:

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

---

## Mode Thresholds

| Mode | Score Range | Entry Requirement |
|------|------------|-------------------|
| Observe | 0-39 | Default for all new agents |
| Suggest | 40-79 | Score >= 40 AND cluster promotion criteria met AND human approval |
| Autonomous | 80-100 | Score >= 80 AND cluster promotion criteria met AND human approval |

Score alone is necessary but not sufficient for promotion. Cluster-specific criteria (defined in GOVERNANCE.md) must also be met.

---

## Initial Scores

New agents start at 10 (deployed but unproven). Agents with existing track records get a one-time assessment score based on historical usage.

### Assessment Tiers for Existing Agents

| Tier | Score | Criteria |
|------|-------|----------|
| Unproven | 10 | New or rarely used |
| Tested | 20 | Used 5+ times, generally useful |
| Proven | 35 | Used 15+ times, consistently good output |
| Trusted | 50 | Extensive track record, rarely needs revision |

All existing agents start in Observe mode regardless of initial score. Mode must be explicitly granted.

---

## Score Review

- Weekly: Scan for agents with no activity (flag for David)
- Monthly: Review score trends, identify candidates for promotion
- On demand: David can adjust scores manually with a logged reason

---

## Example Score Evolution

```
chief-of-staff:
  Day 0:  +10 (initial_deployment)     = 10  [Observe]
  Day 3:  +2  (useful_output)           = 12
  Day 5:  +2  (useful_output)           = 14
  Day 7:  +2  (useful_output)           = 16
  Day 7:  +5  (task_success_no_revision) = 21
  Day 7:  +2  (3-streak bonus)          = 23
  Day 10: +5  (task_success_no_revision) = 28
  Day 14: +5  (task_success_no_revision) = 33
  Day 14: +5  (5-streak bonus)          = 38
  Day 15: +2  (useful_output)           = 40  [Eligible for Suggest if criteria met]
  Day 15: +10 (mode_promotion)          = 50  [Promoted to Suggest by David]
```
