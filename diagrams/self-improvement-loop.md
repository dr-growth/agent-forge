# Self-Improvement Loop

The feedback cycle that makes agents better over time. Two systems work together: OpenSpace monitors in real-time, autoimprove optimizes overnight.

```mermaid
flowchart TD
    subgraph daily["Daily Use"]
        RealWork["Real Work<br/>Agents handle actual tasks"]
    end

    subgraph openspace["OpenSpace (The Immune System)"]
        direction TB
        Watch["Monitor agent<br/>execution in real-time"]

        Watch --> SkillBreak{"Skill breaks?"}
        Watch --> BetterWay{"Better approach<br/>exists?"}
        Watch --> Novel{"Novel pattern<br/>detected?"}

        SkillBreak -->|Yes| Fix["FIX<br/>Patch the skill<br/>immediately"]
        BetterWay -->|Yes| Derive["DERIVED<br/>Create improved<br/>version"]
        Novel -->|Yes| Capture["CAPTURED<br/>Log for review"]
    end

    subgraph metrics["Usage Metrics"]
        direction TB
        TaskSuccess["Task success rate"]
        RevisionRate["Revision rate"]
        RoutingAccuracy["Routing accuracy"]
        ConfidenceCalibration["Confidence calibration"]
        ScopeViolations["Scope violations"]
    end

    subgraph autoimprove["autoimprove (The Lab)"]
        direction TB
        Prioritize["Prioritize improvements<br/>by impact"]
        Optimize["Generate optimized<br/>agent versions"]
        Test["Test against<br/>historical inputs"]
        Ship["Ship improved<br/>agents"]
    end

    subgraph patterns["Knowledge Base"]
        ProvenPatterns["Proven Patterns<br/>Library"]
        AntiPatterns["Anti-Patterns<br/>Library"]
    end

    RealWork --> Watch
    Fix --> metrics
    Derive --> metrics
    Capture --> metrics
    metrics --> Prioritize
    Prioritize --> Optimize
    Optimize --> Test
    Test --> Ship
    Ship -->|"Improved agents"| RealWork

    Capture --> ProvenPatterns
    Fix --> AntiPatterns
    Derive --> ProvenPatterns

    classDef daily fill:#e3f2fd,stroke:#1565C0
    classDef openspace fill:#fff3e0,stroke:#E65100
    classDef metrics fill:#f3e5f5,stroke:#6A1B9A
    classDef lab fill:#e8f5e9,stroke:#2E7D32
    classDef knowledge fill:#fce4ec,stroke:#AD1457

    class RealWork daily
    class Watch,SkillBreak,BetterWay,Novel,Fix,Derive,Capture openspace
    class TaskSuccess,RevisionRate,RoutingAccuracy,ConfidenceCalibration,ScopeViolations metrics
    class Prioritize,Optimize,Test,Ship lab
    class ProvenPatterns,AntiPatterns knowledge
```

## How the Two Systems Differ

```mermaid
graph LR
    subgraph openspace["OpenSpace"]
        direction TB
        os1["Watches in real-time"]
        os2["Reacts to immediate failures"]
        os3["Patches broken skills"]
        os4["Captures novel patterns"]
        os5["Defensive: prevents degradation"]
    end

    subgraph autoimprove["autoimprove"]
        direction TB
        ai1["Runs overnight / on-demand"]
        ai2["Analyzes aggregate metrics"]
        ai3["Generates optimized versions"]
        ai4["Tests against historical data"]
        ai5["Offensive: drives improvement"]
    end

    openspace ---|"Real-time signals<br/>feed overnight<br/>optimization"| autoimprove
    autoimprove ---|"Improved agents<br/>monitored by<br/>immune system"| openspace
```
