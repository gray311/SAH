---
name: discovery-optimization
description: "Architectural diversity search with probe-based filtering for C2 maximization. Prioritize exploring orthogonal function families over refining saturated step-function patterns."
---

# C2 Maximizer: Diverse Architectural Search Protocol

## Core Principle

The step-function record (0.8962799441554086) is a LOCAL optimum. To beat it, you must
explore function ARCHITECTURES that are fundamentally DIFFERENT from step functions.
Sequential refinement of one type = wasted budget. PARALLEL exploration across families.

## Phase 1: Generate Diverse Architectures (Iterations 1-3)

1. Call generate_candidates ONCE to get 3-5 proposals from DIFFERENT families:
   - Gaussian mixtures: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))
   - B-spline basis: Smooth curves with optimized control points
   - Oscillatory with decay: f(x) = (1 + alpha*cos(beta*x)) * exp(-gamma*|x|)
   - Piecewise-linear: Many vertices with varying heights
   - Multi-modal mixtures: Non-symmetric multi-peak structures

2. EXPECTATION: At least one family should exceed 0.89628.

## Phase 2: Probe-Based Filtering

1. For EACH proposal, call probe_solution IMMEDIATELY (30 probes total).
2. Rank all proposals by probe score.
3. Select TOP 3-5 for full evaluation.
4. If probe score < 0.89628: SKIP full evaluation, try next proposal.
5. Budget rule: Never call evaluate_solution unless probe_score > current_best.

## Phase 3: Limited Refinement

1. For each evaluated proposal that beats the record:
   - Refine for MAX 2-3 iterations ONLY
   - Use small mutations: height adjustments ±0.02-0.05, width adjustments ±3-5%
   - After 2-3 iterations, STOP and try a NEW family.

2. If NO proposal beats the record after Phase 2:
   - Generate a NEW set of candidates from a DIFFERENT angle
   - Example: If you tried all smooth functions, try sharp multi-step variants
   - Example: If symmetric failed, try asymmetric structures

## Phase 4: Stalled Recovery

After iteration 10 (if no improvement):
- Call generate_candidates again
- Force orthogonal search: If only tried Gaussian, try oscillatory. If only tried smooth, try piecewise-linear.
- Mix successful elements from different proposals.

## Key Rules

- PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
- PROBE FIRST: Always probe before evaluating
- FAMILY DIVERSITY: Try 3+ different families before exhausting any one
- LIMIT REFINEMENT: Max 3 iterations per family without trying a new one
- SKIP LOSERS: If probe_score < best, don't waste an evaluation
