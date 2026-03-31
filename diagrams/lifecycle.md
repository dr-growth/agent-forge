# Lifecycle Engine

The 5 stages every agent moves through. Stages are not strictly sequential -- agents cycle between Audit, Iterate, and Govern throughout their lifetime.

```mermaid
stateDiagram-v2
    [*] --> Architect

    state "1. ARCHITECT" as Architect {
        direction LR
        Discovery --> Design
        Design --> Review
        Review --> ShipV1["Ship v1.0"]
    }

    state "2. AUDIT" as Audit {
        direction LR
        StandardCheck["Standard Check<br/>9 requirements"] --> BloatAnalysis["Bloat Analysis<br/>Cut what doesn't<br/>change behavior"]
        BloatAnalysis --> GapAnalysis["Gap Analysis<br/>Missing examples?<br/>Edge cases?"]
        GapAnalysis --> DiagnosisReport["Diagnosis Report<br/>Grade A-F"]
    }

    state "3. ITERATE" as Iterate {
        direction LR
        FeedbackIntake["Feedback Intake<br/>Real usage examples"] --> RootCause["Root Cause<br/>Prompt gap?<br/>Scope creep?<br/>Tool limit?"]
        RootCause --> TargetedPatch["Targeted Patch<br/>Minimum effective<br/>change"]
        TargetedPatch --> VersionBump["Version Bump<br/>+ changelog"]
    }

    state "4. GOVERN" as Govern {
        direction LR
        RegistryReview["Registry Review<br/>Last review date?<br/>Usage frequency?"] --> OverlapCheck["Overlap Check<br/>Merge candidates?<br/>Sunset candidates?"]
        OverlapCheck --> ArchHealth["Architecture Health<br/>Gaps? Sprawl?<br/>Organization?"]
        ArchHealth --> GovReport["Governance Report<br/>Actions for<br/>next cycle"]
    }

    state "5. RESEARCH" as Research {
        direction LR
        ScanLiterature["Scan Literature<br/>New findings on<br/>agent design"] --> ValidateDecisions["Validate Decisions<br/>Do our patterns<br/>still hold?"]
        ValidateDecisions --> UpdatePatterns["Update Patterns<br/>Add / modify /<br/>deprecate"]
    }

    Architect --> Audit : Agent meets 9 requirements,<br/>registered in portfolio

    Audit --> Iterate : Diagnosis complete,<br/>improvement plan agreed

    Iterate --> Audit : Re-audit after patch<br/>to verify fix

    Iterate --> Govern : Agent stable,<br/>no outstanding issues

    Govern --> Audit : Overdue for review<br/>or overlap detected

    Govern --> Research : Monthly validation<br/>cycle

    Research --> Audit : New findings invalidate<br/>existing pattern

    Research --> Govern : Patterns confirmed,<br/>no changes needed

    note right of Architect
        Entry criteria:
        - Clear problem statement
        - No existing agent covers this
        - User/audience defined

        Exit criteria:
        - Meets all 9 standard requirements
        - Registered in portfolio
        - v1.0 shipped
    end note

    note right of Govern
        Cadence: Monthly
        Aligned with Research audit

        Exit criteria:
        - All agents reviewed
        - Merge/sunset decisions made
        - Action items assigned
    end note
```
