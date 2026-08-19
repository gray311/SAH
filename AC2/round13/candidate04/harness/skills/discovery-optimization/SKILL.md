---
name: discovery-optimization
description: "Architectural exploration with probe-based filtering for C2 maximization. Use generate_candidates to explore diverse function families, rank with probes, and evaluate only top candidates."
---

# C₂ Maximizer: Architectural Exploration Protocol

## Core Principle

The step-function record (0.8962799441554086) is a LOCAL OPTIMUM. To beat it, you MUST explore DIFFERENT function architectures, not refine step functions.

## Phase 1: Architectural Generation (Iterations 1-3)

1. Call generate_candidates ONCE to get 3-5 proposals across DIFFERENT families.

2. Families to explore:
   - Gaussian mixtures: f(x) = Σ wᵢ · exp(-(x-μᵢ)²/(2σᵢ²)) — smooth, multi-peaked
   - B-spline basis: Flexible smooth with optimized control points
   - Piecewise-linear: Controlled smoothness, mimics steps with transitions
   - Oscillatory with decay: f(x) = (1 + α·cos(βx)) · exp(-γ|x|) — structured convolutions
   - Multi-level steps: Refined asymmetric multi-level patterns

3. EXPECTATION: At least one family should beat the record.

## Phase 2: Probe-Based Filtering (Critical Step)

1. For EACH proposal, call probe_solution to get approximate scores.

2. You have 30 probes — use them to RANK ALL proposals BEFORE any full evaluation.

3. Select TOP 2-3 by probe score for full evaluation.

4. Rule: If probe score < current best, SKIP full evaluation.

## Phase 3: Evaluation & Diversification

1. For each top proposal, call evaluate_solution ONCE.

2. If a proposal beats the record: celebrate, then immediately generate NEW candidates from a DIFFERENT family.

3. If NO proposal beats the record: generate a NEW set of candidates.

## Phase 4: Stalled Recovery (After iteration 10)

- Call generate_candidates with a DIFFERENT strategy
- Example: If only tried smooth functions, try sharp ones
- Mix elements from successful proposals

## Key Rules

1. PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT
2. DO NOT start by editing the seed program
3. PROBE BEFORE EVALUATE — use all 30 probes
4. SWITCH ARCHITECTURES quickly when one fails
5. The step-function patterns are a TRAP — break out of them.
