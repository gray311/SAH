---
name: discovery-optimization
description: "Systematically explore function representations to maximize C2. Prioritize step functions (current record-holders) over piecewise-linear. Use probe-based ranking to test 10+ variants per family before evaluation. Diversify aggressively\u2014reset to new families when stuck."
---

# C2 Optimization: Step-Function First Strategy

## Core Principle

The C2 record (0.8963) is held by STEP FUNCTIONS. The seed's piecewise-linear approach is likely a distraction. YOUR JOB: Force exploration of step functions first.

## Phase 1: Step Function Blitz

Generate these STEP FUNCTION variants and PROBE all:

| Pattern | Support | Heights | Description |
|---------|---------|---------|-------------|
| S1 | 0.2n-0.8n | 1.0 | Standard wide step |
| S2 | 0.2n-0.8n | 1.2 | Taller step |
| S3 | 0.3n-0.7n | 1.3 | Narrower, taller |
| S4 | 0.1n-0.9n | 0.9 | Wider, shorter |
| S5 | 0.1n-0.4n, 0.6n-0.9n | 1.5, 1.5 | Dual regions |
| S6 | 0.2n-0.5n, 0.6n-0.9n | 2.0, 0.8 | Asymmetric |
| S7 | 0.1n-0.3n, 0.4n-0.7n, 0.8n-0.9n | 1.0, 1.5, 0.7 | Three-level |
| S8 | 0.3n-0.4n, 0.5n-0.6n | 3.0, 1.0 | Twin spikes |
| S9 | 0.25n-0.75n | 1.1 | Slightly varied |
| S10 | 0.1n-0.9n | 0.7 | Wide, short |

Expected: 2-3 will exceed 0.8963

## Phase 2: Gaussian Mixtures

If step functions plateau at ≤0.8965, try Gaussians:
- K=2: means at ±0.5, sigma=0.15
- K=3: means at -0.5, 0.0, 0.5, sigma=0.12
- K=5: uniform spacing, sigma=0.1

## Phase 3: Evaluate Top Candidates

Select top 3 from Phase 1-2 probes. For each:
- Run 3 seeds with evaluate_solution
- Keep best result

## Phase 4: Escalation

If still ≤0.8965 after 10 evals:
- Try piecewise-linear with 1000+ intervals
- Try exponential combinations

## Critical Rules

- STEP FUNCTIONS FIRST: They are known to work
- PROBE BEFORE EVAL: 10+ probes per family, ≤3 evals per family
- RESET HARD: When stuck, completely new representation
- TRACK: Note which variant beat what

Success = beating 0.8963. Anything less is a failure.
