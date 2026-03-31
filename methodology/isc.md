# Ideal State Criteria (ISC)

ISC is a methodology for defining "done" in a way that is atomic, binary-testable, and immune to scope drift. Every non-trivial task should have ISC defined before execution begins.

## What ISC Is

An ISC criterion is a statement that describes an end state, not an action. It passes or fails. There is no "partially done."

Each criterion should be:
- **Atomic:** One thing, not two things joined by "and"
- **Binary-testable:** A human can look at the result and answer YES or NO
- **8-12 words:** Short enough to hold in working memory
- **An end state, not an action:** Describes what IS true when done, not what you DO

## Writing Good ISC

### The Rules

1. Start with the noun, not the verb. "Database schema includes user table" not "Create user table in database."
2. One assertion per criterion. If you use "and," you probably need two criteria.
3. Make it verifiable by someone who was not in the room. No implicit context.
4. Include the specificity needed to test. "Homepage loads in under 2 seconds" not "Homepage is fast."

### Good Examples

| Criterion | Why It Works |
|-----------|-------------|
| ISC-1: All API endpoints return JSON error responses | Atomic, testable, end state |
| ISC-2: Test suite passes with zero failures | Binary, no ambiguity |
| ISC-3: README includes setup instructions for new developers | Verifiable by inspection |
| ISC-4: No hardcoded credentials in source files | Testable via grep |
| ISC-5: Docker container starts without manual intervention | Binary, reproducible |

### Bad Examples

| Criterion | Problem | Fix |
|-----------|---------|-----|
| "Implement user authentication" | Action, not end state | "Users can log in with email and password" |
| "Code is clean and well-organized" | Subjective, not testable | "All functions are under 50 lines" or "No function has more than 3 parameters" |
| "The system handles errors properly" | Vague, compound | Split into specific error scenarios: "API returns 404 for missing resources" + "API returns 400 for invalid input" |
| "Database is set up and migrations run and seeds are loaded" | Three criteria joined by "and" | Split into three: "Database schema matches migration files" + "Seed data present in users table" + "Migration tool reports no pending migrations" |
| "Performance is acceptable" | No definition of acceptable | "P95 response time under 200ms for list endpoints" |

---

## The Splitting Test

After writing every ISC criterion, apply this test:

> Can this criterion be split into two independent criteria that could pass or fail independently?

If YES, split it. Keep splitting until every criterion is irreducibly atomic.

### Splitting Examples

**Before:** "API validates input and returns appropriate error messages"

**Split into:**
- ISC-1: API rejects requests with missing required fields
- ISC-2: API error responses include field name and reason

These can pass/fail independently. The API might validate but return unhelpful errors, or return good errors but miss some validation. Two different failure modes, two different criteria.

**Before:** "User profile page shows all user data and handles missing fields gracefully"

**Split into:**
- ISC-1: Profile page displays name, email, and avatar when all fields are present
- ISC-2: Profile page shows placeholder text for any missing field
- ISC-3: Profile page does not crash when user record has null fields

---

## Anti-Criteria (ISC-A)

Anti-criteria define what must NOT be true. They catch failure modes that positive criteria miss.

Anti-criteria use the ISC-A prefix and describe states that indicate failure.

### Examples

| Anti-Criterion | What It Catches |
|---------------|----------------|
| ISC-A-1: No console errors on page load | Runtime errors that do not break rendering |
| ISC-A-2: No API calls without authentication headers | Security regression |
| ISC-A-3: No inline styles in component files | Style methodology violation |
| ISC-A-4: No TODO comments in shipped code | Incomplete work |
| ISC-A-5: No functions longer than 100 lines | Complexity creep |

### When to Use Anti-Criteria

- When you have seen a specific failure mode before and want to prevent recurrence
- When the positive criteria do not cover important constraints
- When "absence of X" is easier to test than "presence of Y"
- When you want to enforce standards that are not features

---

## ISC Count Gate

The number of criteria should match the complexity of the work. Too few criteria means you have not thought through the task. Too many means you are over-specifying.

| Effort Tier | ISC Floor | Typical Range |
|-------------|-----------|---------------|
| Standard (<2hr) | 8 | 8-12 |
| Extended (<8hr) | 16 | 16-24 |
| Advanced (<2 days) | 24 | 24-36 |
| Deep (<1 week) | 40 | 40-56 |
| Comprehensive (<2 weeks) | 64 | 64-80 |

**Gate rule:** Do not begin execution until the criteria count meets the floor for the effort tier. If you cannot write enough criteria, you do not understand the task well enough.

**Ceiling guidance:** If you are writing more than 80 criteria for any task, the task should be decomposed into subtasks, each with their own ISC.

---

## Using ISC During Execution

1. **Define ISC before Phase 1 (OBSERVE) completes.** They are the contract for what "done" means.
2. **Check off criteria immediately as they are satisfied.** Do not batch. The ISC list is the real-time progress tracker.
3. **If a criterion turns out to be wrong, update it.** ISC is a living document during execution. Log why it changed.
4. **During VERIFY, provide evidence per criterion.** Every criterion gets a PASS with evidence or a FAIL with explanation. No blanket assertions.

---

## ISC vs. User Stories vs. Acceptance Criteria

| Concept | Scope | Format | Testability |
|---------|-------|--------|-------------|
| User Story | Feature-level | "As a [user], I want [feature], so that [benefit]" | Indirectly testable |
| Acceptance Criteria | Feature-level | "Given [context], when [action], then [result]" | Testable but often compound |
| ISC | Task-level | "[End state in 8-12 words]" | Directly testable, atomic |

ISC operates at a lower level than user stories. A single user story might generate 5-15 ISC criteria. ISC replaces "did we do the thing?" with "is the thing done?"
