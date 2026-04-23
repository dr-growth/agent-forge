# Audit Trail Specification v1.0

Structured logging for every agent action that modifies state. The answer to "what is this AI thing doing?"

Last updated: 2026-03-26

---

## Log Format

Append-only JSONL file at `governance/audit-log.jsonl`. One JSON object per line.

```json
{
  "timestamp": "2026-03-26T14:30:00Z",
  "agent": "chief-of-staff",
  "mode": "suggest",
  "action_type": "suggest_task_create",
  "target": "asana:task",
  "description": "Proposed creating follow-up task for Marissa re: Q2 ABX campaign review",
  "confidence": 0.85,
  "approval": "pending",
  "outcome": null,
  "context": "Triggered by daily brief scan of overdue delegation items"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 | When the action occurred |
| `agent` | string | Agent name |
| `mode` | string | Agent's governance mode at time of action |
| `action_type` | string | Categorized action (see Action Types) |
| `target` | string | What was acted on (system:resource format) |
| `description` | string | Human-readable description of what happened |
| `confidence` | number | Agent's confidence in the action (0.0-1.0) |
| `approval` | string | pending, approved, rejected, auto (for autonomous mode) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `outcome` | string | success, failure, partial, null (if pending) |
| `context` | string | What triggered this action |
| `files_modified` | array | List of file paths changed |
| `lines_changed` | number | Total lines added/removed |
| `duration_ms` | number | How long the action took |
| `trust_delta` | number | Trust score change resulting from this action |
| `error` | string | Error message if action failed |

---

## Action Types

### Read Actions (logged but don't affect trust score)
- `read_context` -- Read a context file
- `read_external` -- Read from external system (Asana, Notion, Calendar)
- `search` -- Searched for information

### Suggest Actions (Suggest mode)
- `suggest_task_create` -- Proposed creating a task
- `suggest_task_update` -- Proposed modifying a task
- `suggest_calendar_block` -- Proposed a calendar block
- `suggest_delegation` -- Proposed delegating work
- `suggest_message_draft` -- Drafted a message for review
- `suggest_action` -- Generic suggested action

### Write Actions (Autonomous mode)
- `write_task_create` -- Created a task
- `write_task_update` -- Modified a task
- `write_calendar_block` -- Created a calendar block
- `write_state_update` -- Updated internal state file
- `write_context_update` -- Updated a context file
- `write_agent_route` -- Routed work to another agent

### External Actions (highest scrutiny)
- `external_slack` -- Sent or proposed Slack message
- `external_email` -- Sent or proposed email
- `external_asana` -- Modified Asana
- `external_notion` -- Modified Notion
- `external_calendar` -- Modified calendar

---

## Examples by Action Type

### Read (Observe mode)
```json
{
  "timestamp": "2026-03-26T08:00:00Z",
  "agent": "chief-of-staff",
  "mode": "observe",
  "action_type": "read_context",
  "target": "file:~/wrk-os/contexts/work.md",
  "description": "Read work context for daily brief preparation",
  "confidence": 1.0,
  "approval": "auto"
}
```

### Suggest (Suggest mode)
```json
{
  "timestamp": "2026-03-26T08:15:00Z",
  "agent": "chief-of-staff",
  "mode": "suggest",
  "action_type": "suggest_task_create",
  "target": "asana:task",
  "description": "Proposed: Create task 'Follow up with Marissa on ABX Q2 plan' with DUE 2026-03-28",
  "confidence": 0.82,
  "approval": "approved",
  "outcome": "success",
  "trust_delta": 2,
  "context": "Marissa committed to ABX plan in 2026-03-24 team meeting, no follow-up task exists"
}
```

### Write (Autonomous mode)
```json
{
  "timestamp": "2026-03-26T08:30:00Z",
  "agent": "chief-of-staff",
  "mode": "autonomous",
  "action_type": "write_state_update",
  "target": "file:~/os/projects/agent-forge/agents/inner-circle/chief-of-staff/state.md",
  "description": "Updated carry-forward items after daily brief",
  "confidence": 0.95,
  "approval": "auto",
  "outcome": "success",
  "files_modified": ["~/os/projects/agent-forge/agents/inner-circle/chief-of-staff/state.md"],
  "lines_changed": 12
}
```

---

## Retention

- **Active log:** Last 90 days in `audit-log.jsonl`
- **Archive:** Older entries moved to `audit-log-archive/YYYY-MM.jsonl` (manual, quarterly)
- **Metrics:** Monthly summary generated during agent review

---

## Who Writes to the Audit Log

For now, audit entries are written manually during agent interactions -- the orchestrating session (main conversation or agent runner) appends entries when an agent takes notable actions.

Future: Hook-based automatic logging when agent actions are detected.

---

## Privacy

- Audit logs may contain references to people, tasks, and business context
- Treat audit-log.jsonl as confidential (same handling as wrk-os data)
- Never commit to public repositories
- Never share outside David's direct review
