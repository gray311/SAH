---
name: orthogonal-exploration-protocol
description: Parallel exploration of orthogonal function families with probe-based filtering.
---

# Orthogonal Exploration Protocol for C₂ Maximization

## Core Principle
The step-function record (0.8962799441554086) is a LOCAL optimum. To break through,
you MUST explore FUNCTION FAMILIES ORTHOGONAL to step functions in PARALLEL.
Sequential refinement wastes iterations.

## Phase 1: Seed Analysis (Iteration 1)
1. Call analyze_seed ONCE to understand the current solution's structure
2. Identify what makes step functions work (discretization, pattern symmetry, etc.)
3. Generate orthogonal strategies: smooth functions, oscillatory patterns, etc.

## Phase 2: Diverse Generation
Call generate_candidates to get 5-7 proposals across DIFFERENT families:
- Gaussian mixtures: smooth, multi-peaked, naturally optimized ||f★f||₂/||f★f||_∞ ratio
- B-spline basis: flexible smooth transitions with optimized control points
- Oscillatory with decay: structured convolutions that may resonate better
- Piecewise-linear: controlled smoothness, can bridge step and smooth
- Multi-level asymmetric steps: variations on step functions with new patterns

## Phase 3: Probe-Based Filtering
You have 30 probes. Use them EFFICIENTLY:
1. Call probe_solution on EACH proposal (30 probes can cover all of them!)
2. Rank by probe score
3. Select TOP 3-4 for full evaluation
4. SKIP any proposal with probe < current best (waste budget)

## Phase 4: Full Evaluation
For each top proposal, call evaluate_solution ONCE to confirm.
- If one beats the record: note the family, but DO NOT exhaust it
- If none beat the record: generate NEW candidates from a DIFFERENT angle

## Phase 5: Stalled Recovery (after 10 iterations with no improvement)
- Generate completely new families (e.g., Fourier-space optimized, fractal-like)
- Mix elements: combine successful features from different proposals
- Change discretization: try different N (400, 800, 1000)

## Key Rules
1. PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
2. USE PROBES TO FILTER — you have 30 cheap evaluations
3. When one family fails, immediately switch to a new family
4. Document which family achieved the best score for reference
