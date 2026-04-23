# autoimprove Changelog

## [2026-03-29] [PHASE] Three agents improved, judge upgraded, creator research complete

**What:** Full autoimprove session: Scout (72.0->76.3, +4.3), Chief of Staff (66.3->69.1, +2.8), Build-in-Public (59.3->75.7, +16.4). Upgraded judge from Haiku to Sonnet for better evaluation quality. Researched 11 LinkedIn benchmark creators (Elena Verna, Dan Shipper, Kyle Poyar, etc.) to ground build-in-public test cases in real-world quality standards. Build-in-public had a breakthrough at iteration 4 (+11.8 in one step) driven by adding mandatory specificity requirements and structured pushback on vague input.
**Why:** Proving the engine works across different agent types (research, operations, content). The build-in-public improvement is high-value because it directly affects David's public reputation and content quality.
**Impact:** Three improved agent files ready for promotion in `work/`. Creator research saved to `~/os/projects/writing-system/research/benchmark-creators-2026-03-29.md`. Total session cost: $2.83 across all three runs. The Sonnet judge produces wider score distributions and catches quality gaps Haiku missed.
**Files:** `work/scout.md`, `work/chief-of-staff.md`, `work/build-in-public.md`, `src/config.py`, `test-cases/build-in-public/`, `directives/build-in-public.md`, `results/experiments.jsonl`

## [2026-03-29] [PHASE] First successful improvement run on Scout

**What:** Built and ran the full autoimprove engine: evaluate.py (6-dimension hybrid scorer), runner.py (Claude API skill executor), loop.py (git-ratcheted improvement loop), 3 Scout test cases, improvement directive. First run: baseline 72.0 -> 76.3 (+4.3) in 3 iterations, 2 committed improvements, 1 regression correctly rejected. Total cost: $0.75.
**Why:** Weekend 3 of the engine upgrade. Proving that skills can be autonomously, measurably improved through controlled experiment loops.
**Impact:** The improvement engine works. Scout's confidence calibration jumped from 57 to 90 in one iteration. Completeness improved from 61 to 73. The git ratchet correctly blocked a regression. Ready for scaling to more skills.
**Files:** `src/evaluate.py`, `src/runner.py`, `src/loop.py`, `src/config.py`, `test-cases/scout/`, `directives/scout.md`, `results/experiments.jsonl`, `work/scout.md`, `LEARNINGS.md`, `CLAUDE.md`

## [2026-03-28] [ARCHITECTURE] Project created with full implementation plan

**What:** Created autoimprove project -- autonomous skill/agent improvement engine adapted from Karpathy's autoresearch
**Why:** PAIOS skills have no measurable quality metrics. Need automated evaluation + improvement loops to scale quality and build toward AI automation services offering.
**Impact:** Foundation for compounding skill improvement. Connects to services vision (G1 -> consulting/services).
**Files:** `PLAN.md`, `CLAUDE.md`, `CHANGELOG.md`
