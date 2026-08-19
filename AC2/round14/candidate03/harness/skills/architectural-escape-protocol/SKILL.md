---
name: architectural-escape-protocol
description: Escape step-function local optimum by exploring diverse function families in parallel. Use probe-based filtering to efficiently rank candidates across families. Always switch families after failed refinement attempts.
---

# Architectural Escape Protocol for C2 Maximization

## Core Philosophy

The step-function record (C2 ≈ 0.8963) is a LOCAL OPTIMUM. Refining it further wastes
precious evaluations. The path to new records lies in ABRUPT ARCHITECTURAL CHANGES,
not incremental refinements.

## Phase 1: Analysis & Generation (Iteration 1)

1. Call analyze_function_space ONCE to understand:
   - Why step functions work (concentrated L2, high L∞)
   - Weak points: modality, smoothness, symmetry, spacing

2. Call generate_candidates to get 3-5 proposals across DIFFERENT families:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level sharp steps (4-6 levels, asymmetric)

## Phase 2: Probe-Based Ranking

1. For EACH proposal, call probe_solution (30 probes available).
   - Rank ALL candidates by probe score.
   - Skip candidates with probe < 0.89628.

2. Select top 3-5 by probe score for full evaluation.

## Phase 3: Family Cycling

1. Evaluate top candidates with evaluate_solution.

2. If ANY candidate beats 0.89628:
   - Slightly refine it (tiny mutations only), then IMMEDIATELY switch families.
   - Do NOT exhaust one family; explore in parallel.

3. If NO improvement after 5+ evals from one family:
   - Call generate_candidates AGAIN with DIFFERENT families.
   - Mix smooth and sharp, multi-modal and single-modal.

## Phase 4: Stalled Recovery

After 10 iterations without improvement:
- Call generate_candidates with novel combinations (e.g., "piecewise Gaussian")
- Try both extremes: ultra-smooth Gaussians AND ultra-sharp multi-level steps

## Critical Rules

✓ PROBE BEFORE EVALUATE: Use 30 probes to filter candidates.
✓ PARALLEL EXPLORATION: Try multiple families, not sequentially.
✓ ABUPT CHANGES: Architectural > incremental improvements.
✓ FAMILY CYCLING: Switch families after 2-3 failed attempts.
✓ TRACK WHAT WORKS: Note which families beat the record; prioritize them.
✗ NEVER refine step functions exhaustively. One failure = switch.
