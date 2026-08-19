---
name: probe-filtering-protocol
description: Diverse architectural search with mandatory probe-based filtering. Prioritize orthogonal function families over sequential refinement.
---

# C2 Maximizer: Probe-Filtering Protocol

## Core Principle

Sequential refinement of step functions = WASTED BUDGET. The seed is already at the step-function optimum (0.8962799441554086).
You must explore ORTHOGONAL function ARCHITECTURES.

## Phase 1: Mandatory Diverse Generation (Iteration 1)

1. Call generate_candidates IMMEDIATELY. Get 3-5 proposals from DIFFERENT families:
   - Gaussian mixtures
   - Oscillatory with decay
   - Piecewise-linear (dense vertices)
   - Asymmetric multi-modal
   - B-spline inspired

2. DO NOT refine any single proposal yet.

## Phase 2: Mandatory Probe Filtering

1. For EVERY proposal, call probe_solution IMMEDIATELY.
   - You have 30 probes - this is your PRIMARY tool.
   - Probes are FAST (10s) and SAFE (separate budget).

2. Rank all proposals by probe score.

3. FILTER aggressively: Only call evaluate_solution if probe_score > 0.89628.
   - If probe_score < 0.89628: SKIP it. Try another proposal.
   - This saves you precious evaluations.

4. Select TOP 3-5 by probe score for full evaluation.

## Phase 3: Limited Refinement

1. For each evaluated proposal that beats the record:
   - Refine for MAX 2-3 iterations ONLY
   - Use small mutations: heights ±0.02-0.05, widths ±3-5%
   - After 2-3 iterations: STOP and try a NEW family.

2. If NO proposal beats the record after Phase 2:
   - Generate a NEW set of candidates
   - Force orthogonal search: If Gaussian failed, try oscillatory. If smooth failed, try piecewise-linear.

## Phase 4: Stalled Recovery (After Iteration 10)

- Call generate_candidates again
- Force completely new families if you've exhausted all initial ones
- Mix strategies from different successful proposals

## Key Rules

- PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
- PROBE FIRST: Always probe before evaluating (30 probes = 30 chances to filter)
- SKIP LOSERS: probe_score < best → don't evaluate
- FAMILY DIVERSITY: 3+ different families before exhausting any one
- REFINEMENT LIMIT: Max 3 iterations per family without trying new one
