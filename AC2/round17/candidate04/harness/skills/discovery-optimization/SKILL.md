---
name: discovery-optimization
description: "Parallel diverse exploration across function families (Gaussian, B-spline, oscillatory, piecewise) from iteration 1. Use probe-based filtering to quickly identify winners. Stop refining failing families after 3 iterations. Early stop on winners to avoid overfitting."
---

# C₂ Maximizer: Parallel Diverse Exploration Protocol

## Core Principle

Step functions are a STRONG LOCAL OPTIMUM. The seed's refinement mutations have FAILED repeatedly. TO BEAT THE RECORD, you MUST explore DIFFERENT function architectures in PARALLEL, not sequentially refine one type.

## Phase 1: Diverse Generation (Every Iteration)

1. Call generate_candidates to get 5-7 proposals across DIFFERENT families:
   - Gaussian mixtures: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))
   - B-spline basis: 30-50 control points with softplus positivity
   - Piecewise-linear: linear segments with optimized vertices
   - Oscillatory decay: (1 + alpha * cos(beta*x)) * exp(-gamma*|x|)
   - Multi-level improved steps: asymmetric heights/positions
   - Convex combinations of simple functions

2. Do NOT refine step functions - they're a trap. Focus on fundamentally different architectures.

## Phase 2: Probe-Based Filtering

1. For each proposal, call probe_solution to get approximate scores
2. You have 30 probes - use them to RANK all 5-7 proposals
3. Call evaluate_solution on top 2-3 by probe score ONLY
4. If a probe score is < current best, SKIP full evaluation

## Phase 3: Full Evaluation & Decision

1. For each top proposal, call evaluate_solution ONCE to confirm
2. If a proposal beats the record:
   - Refine it VERY LITTLE (2-3 small mutations max)
   - Then STOP and generate NEW candidates (don't over-refine)
3. If NO proposal beats the record:
   - Generate a NEW set of candidates from a different angle
   - Try completely new families if stuck

## Phase 4: Stall Recovery

After ANY 3 iterations on the same family:
- Immediately switch to a NEW family
- Do NOT spend 5+ iterations on a failing approach

## Key Rules

- PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
- Probe 5-7 variants, evaluate top 2 (30 probes = ~5 evals)
- Max 3 iterations per family before switching
- Early stopping on winners: refine minimally, then explore new directions
- When one type fails, IMMEDIATELY switch to a new type (no 5+ iterations)

## Tool Usage

- edit_solution: Implement proposals from generate_candidates, OR tiny mutations (<=3) on a winner
- evaluate_solution: Call AFTER probing. Only top 2 by probe score. Budget 30.
- probe_solution: Rank 5-7 variants cheaply before full evaluation.
- generate_candidates: Call EVERY iteration unless you have a clear winner.

## Mathematical Priorities

- Smooth functions (Gaussian, spline) may achieve better ||f||_2^2 / ||f||_infty ratio than sharp steps
- Oscillatory functions create structured convolutions that might beat step patterns
- Asymmetric structures can reduce constructive interference in convolution
- Always ensure f(x) >= 0 using softplus or max(0,·)
