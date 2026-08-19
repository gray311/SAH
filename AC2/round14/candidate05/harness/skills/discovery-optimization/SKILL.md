---
name: discovery-optimization
description: "Diverse architecture exploration with probe-based ranking. Generate function proposals across multiple families, rank with cheap probes, evaluate only winners."
---

# Diverse Architecture Exploration Protocol for C₂ Maximization
## Core Principle
The step-function record (1.03896) is a LOCAL optimum. To beat it, you must EXPLOR DIVERSE FUNCTION ARCHITECTURES in PARALLEL, using probes to efficiently rank before spending full evaluations.
## Phase 1: Diverse Generation (Every Iteration)
1. Call generate_candidates to get 5-7 proposals across DIFFERENT mathematical families: - Gaussian mixtures (smooth multi-peaked functions) - B-spline basis (flexible smooth curves) - Piecewise-linear (controlled smoothness) - Oscillatory with exponential decay (structured convolutions) - Multi-level asymmetric steps (refined step patterns) - Convolution kernel designs (direct optimization of f★f) - Wavelet-like functions (localized frequency content)
2. For each proposal, review the code snippet and mental model of the function shape.
## Phase 2: Probe-Based Ranking (Critical Phase)
1. You have 30 PROBE budget—use it AGGRESSIVELY. Probes are: - 10x faster than full evaluation (~10s vs ~100s) - Separate budget (30 probes, not counted against 30 evals) - Approximate but sufficient for RANKING proposals
2. Call probe_solution for EACH proposal (5-7 probes per iteration). - If a proposal's probe score < current best, SKIP full evaluation - If probe score > current best, proceed to Phase 3
3. After probing all proposals, select TOP 3-4 by probe score for full evaluation.
## Phase 3: Full Evaluation & Winner Tracking
1. Call evaluate_solution for each top proposal. 2. Track which proposals beat the current best. 3. ONLY if a proposal beats the record: - Note the successful family/architecture - Make 1-2 small refinements (don't over-exploit) - Immediately return to Phase 1 with NEW families
4. If NO proposal beats the record after 3-4 full evaluations: - This is NORMAL—step functions are a strong local optimum - Call generate_candidates AGAIN with a focus on underexplored families - Continue the parallel pipeline
## Phase 4: Diversity Maintenance
1. Every 5 iterations, explicitly generate candidates from families you haven't tried recently. 2. If you've only tried smooth functions, try sharp ones (steps, wavelets). 3. If you've only tried symmetric functions, try asymmetric designs. 4. Vary: number of peaks, decay rates, oscillation frequencies, knot placements.
## Key Rules
- PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT - USE PROBES TO RANK—don't waste full evals on weak candidates - DIVERSITY > OPTIMIZATION: exploring new families beats refining dead ends - Expected outcome: Within 15-20 iterations, one family should beat the record
