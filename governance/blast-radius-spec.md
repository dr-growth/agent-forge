# Blast Radius Specification v1.0

Hard limits on what agents can change per action, scaled by governance mode. Prevents runaway agents from causing outsized damage.

Last updated: 2026-03-26

---

## Limits by Mode

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
| External system writes per hour | 5 | Rate limit on Asana/Notion/Calendar |

---

## Prohibited Operations (All Modes)

These operations are never permitted regardless of trust score or mode:

1. **Delete** -- No deleting files, tasks, projects, calendar events, or data
2. **Send external messages** -- No Slack DMs, emails, or any communication on behalf of the user
3. **Financial actions** -- No purchases, approvals, or financial commitments
4. **Permission changes** -- No modifying access controls, sharing settings, or permissions
5. **Credential access** -- No reading, storing, or transmitting secrets, tokens, or passwords
6. **Cross-boundary sharing** -- No sharing pai-os content in work contexts or vice versa
7. **Force operations** -- No git force push, database drops, or destructive overwrite
8. **Recursive self-modification** -- No agent modifying its own governance rules or trust score

---

## Rate Limits for External Actions

When agents reach Autonomous mode and gain external system access:

| System | Rate Limit | Cooldown |
|--------|-----------|----------|
| Asana (task create/update) | 5 per hour | 12 min between writes |
| Notion (page create/update) | 3 per hour | 20 min between writes |
| Calendar (event create/update) | 3 per hour | 20 min between writes |
| Slack (when available) | 0 (never autonomous) | N/A |
| Email (when available) | 0 (never autonomous) | N/A |

Slack and email remain human-approved-only regardless of mode. Communication on behalf of the user is the highest-trust action and is gated permanently.

---

## Escalation Protocol

When an agent hits a limit:

1. **Stop the current action.** Do not attempt to work around the limit.
2. **Log the limit hit** in the audit trail with action_type `limit_reached`.
3. **Inform the user.** State what was attempted, what limit was hit, and ask for guidance.
4. **Do not retry** without explicit human approval.

---

## Cluster-Specific Overrides

Some clusters have tighter or looser limits based on their domain:

| Cluster | Override | Reason |
|---------|----------|--------|
| engineering | Lines changed per file: 200 (Autonomous) | Code changes are naturally larger |
| sales-pipeline | External writes: 0 at all modes | Research agents should never write to prospect-facing systems |
| health | All external writes: 0 | Health recommendations stay advisory |
| meta-governance | Mode cap: Suggest only | Governance agents don't get autonomous mode |

---

## Enforcement

This spec is enforced through two mechanisms:

1. **Steering Rule** (`~/.claude/rules/SYSTEM/blast-radius.md`): Loaded into every session. Advisory but prominent.
2. **Agent Instructions**: Each agent's prompt includes its mode and corresponding limits. The agent is instructed to self-enforce.

Future: Hook-based enforcement that validates actions against limits before execution.

---

## Reviewing Limits

Limits are reviewed quarterly or when:
- An agent consistently hits limits during normal operation (limits too tight)
- An agent causes damage within limits (limits too loose)
- A new external system integration is added
- David's comfort level with autonomous agents changes

All limit changes logged in `~/os/knowledge/changelog.md`.
