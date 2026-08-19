---
name: discovery-optimization
description: "Diverse architectural exploration for C2 maximization. Escape local optima by exploring FUNCTION FAMILIES, not just refining step patterns. Use probe-based filtering to efficiently rank diverse candidates. Always prioritize ABRUPT architectural changes over incremental refinements."
---

# C2 Maximizer: Architectural Escape Protocol

## Core Principle

Step functions are a LOCAL OPTIMUM. Beat the record by exploring DIFFERENT function families in PARALLEL.

## Phase 1: Initial Setup

1. Call analyze_function_space ONCE to understand:
   - Why step functions achieve C2 ≈ 0.8963
   - Where the L2/∞ ratio is optimized
   - Weak points to exploit for improvement

2. Call generate_candidates to get 3-5 proposals across DIFFERENT families:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level sharp steps (4-6 levels, asymmetric)

## Phase 2: Probe-Based Ranking

1. For EACH proposal, call probe_solution to get approximate scores.
   - You have 30 probes - use ALL of them to rank candidates.
   - Do NOT evaluate anything without probing first.

2. Select top 3-5 by probe score for full evaluation.
   - Skip candidates with probe score < 0.89628.

## Phase 3: Full Evaluation & Family Cycling

1. Evaluate top candidates with evaluate_solution.

2. If ANY candidate beats 0.89628:
   - Slightly refine it (small mutations), BUT do not exhaust it.
   - Immediately generate a NEW set of candidates from a DIFFERENT family.

3. If NO candidate beats the record after evaluating 5+ from one generation:
   - Call generate_candidates AGAIN with DIFFERENT families.
   - Mix and match: if tried smooth functions, try sharp ones next.

## Phase 4: Stalled Recovery

If stuck after 10 iterations:
- Call generate_candidates with completely new families
- Combine elements: e.g., "oscillatory Gaussian mixture" or "piecewise Gaussian"
- Try BOTH smooth AND sharp function types

## Key Rules

- NEVER refine step functions exhaustively. One failed refinement = switch families.
- PROBE BEFORE EVALUATE: Use 30 probes to filter before spending evaluations.
- PARALLEL EXPLORATION: Try multiple families simultaneously, not sequentially.
- ABUPT CHANGES: Architectural changes beat incremental perturbations.
- Track which families work best; cycle through them if stuck.
