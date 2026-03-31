# Algorithm: 7-Phase Execution Cycle

A rigorous execution framework for any non-trivial task. Each phase has specific activities and exit criteria. Phases are sequential -- do not skip phases or start the next before the current one is complete.

```mermaid
flowchart TD
    subgraph phase1["Phase 1: OBSERVE"]
        direction TB
        O1["Reverse-engineer the problem"]
        O2["Read all relevant context"]
        O3["Define ISC criteria<br/>(Independent, Specific, Completable)"]
        O4["Identify unknowns"]
    end

    subgraph phase2["Phase 2: THINK"]
        direction TB
        T1["Run a premortem<br/>What could go wrong?"]
        T2["Identify assumptions"]
        T3["Assess risks and dependencies"]
        T4["Challenge the approach"]
    end

    subgraph phase3["Phase 3: PLAN"]
        direction TB
        P1["Sequence the work"]
        P2["Map dependencies"]
        P3["Define verification criteria<br/>per deliverable"]
        P4["Identify the smallest<br/>working version"]
    end

    subgraph phase4["Phase 4: BUILD"]
        direction TB
        B1["Scaffold the structure"]
        B2["Set up the skeleton<br/>before adding detail"]
        B3["Create test harness<br/>if applicable"]
    end

    subgraph phase5["Phase 5: EXECUTE"]
        direction TB
        E1["Implement against the plan"]
        E2["One change at a time"]
        E3["Verify each step<br/>before proceeding"]
        E4["Log deviations from plan"]
    end

    subgraph phase6["Phase 6: VERIFY"]
        direction TB
        V1["Check every ISC criterion"]
        V2["Evidence per criterion<br/>(not blanket assertions)"]
        V3["Run the Bloat Test"]
        V4["Test edge cases"]
    end

    subgraph phase7["Phase 7: LEARN"]
        direction TB
        L1["What worked?"]
        L2["What broke?"]
        L3["What was harder than expected?"]
        L4["Update patterns library"]
    end

    phase1 -->|"Exit: ISC criteria defined,<br/>context loaded,<br/>unknowns mapped"| phase2
    phase2 -->|"Exit: Risks identified,<br/>assumptions stated,<br/>approach validated"| phase3
    phase3 -->|"Exit: Sequence defined,<br/>dependencies mapped,<br/>verification criteria set"| phase4
    phase4 -->|"Exit: Structure scaffolded,<br/>ready for implementation"| phase5
    phase5 -->|"Exit: Implementation complete,<br/>all steps verified"| phase6
    phase6 -->|"Exit: All criteria pass<br/>with evidence"| phase7
    phase7 -->|"Exit: Learnings captured,<br/>patterns updated"| Done["DONE"]

    phase6 -->|"Criteria fail"| phase5
    phase5 -->|"Plan was wrong"| phase3

    classDef observe fill:#e3f2fd,stroke:#1565C0
    classDef think fill:#fce4ec,stroke:#AD1457
    classDef plan fill:#f3e5f5,stroke:#6A1B9A
    classDef build fill:#fff3e0,stroke:#E65100
    classDef execute fill:#e8f5e9,stroke:#2E7D32
    classDef verify fill:#e0f2f1,stroke:#00695C
    classDef learn fill:#fff8e1,stroke:#F9A825
    classDef done fill:#e8eaf6,stroke:#283593

    class O1,O2,O3,O4 observe
    class T1,T2,T3,T4 think
    class P1,P2,P3,P4 plan
    class B1,B2,B3 build
    class E1,E2,E3,E4 execute
    class V1,V2,V3,V4 verify
    class L1,L2,L3,L4 learn
    class Done done
```

## Phase Details

| Phase | Purpose | Key Question | Exit Criteria |
|-------|---------|-------------|---------------|
| **OBSERVE** | Understand the problem fully before acting | "Do I know what done looks like?" | ISC criteria defined, context loaded, unknowns listed |
| **THINK** | Stress-test the approach before committing | "What could go wrong?" | Risks identified, assumptions explicit, approach validated |
| **PLAN** | Sequence work for efficient execution | "What order minimizes rework?" | Steps sequenced, dependencies mapped, verification defined |
| **BUILD** | Create structure before filling in detail | "Is the skeleton sound?" | Scaffolding in place, ready for implementation |
| **EXECUTE** | Implement one step at a time | "Did this step work before I move on?" | All steps implemented and individually verified |
| **VERIFY** | Confirm the work meets the original criteria | "Can I prove each criterion is met?" | Every ISC criterion passes with specific evidence |
| **LEARN** | Extract lessons for future work | "What would I do differently?" | Learnings logged, patterns updated |

## Common Failure Modes

| Failure | Which Phase Was Skipped | Fix |
|---------|------------------------|-----|
| Built the wrong thing | OBSERVE | Define ISC before starting |
| Didn't anticipate obvious risk | THINK | Run the premortem |
| Constant rework | PLAN | Sequence dependencies properly |
| "It works on my machine" | VERIFY | Evidence per criterion, not assertions |
| Same mistake twice | LEARN | Capture the pattern |
