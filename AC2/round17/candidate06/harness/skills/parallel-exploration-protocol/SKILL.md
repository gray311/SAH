---
name: parallel-exploration-protocol
description: Parallel exploration across function families with probe-based filtering and early diversification.
---

# Parallel Exploration Protocol for C₂ Maximization

## Core Principle

The step-function record is a LOCAL optimum. Beat it by EXPLORING DIFFERENT FUNCTION FAMILIES IN PARALLEL from the START, not by sequentially refining step patterns.

## Phase 1: Diverse Generation (Iteration 1)

### Step 1: Immediate Diversity
1. Call generate_candidates at iteration 1 (do NOT wait).
2. Expect 3-5 proposals across DIFFERENT families:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level asymmetric steps
   - Hybrid step-spline combinations

### Step 2: Probe-Based Ranking
1. For EACH proposal, call probe_solution (5-8 probes per proposal = 25-40 total).
2. If probe budget exceeded, reduce to 3 proposals each.
3. Generate 2-3 variants of TOP 2 proposals by probe score.
4. Probe all variants to build complete ranking.

### Step 3: Full Evaluation
1. Select TOP 3-4 proposals by probe score.
2. Call evaluate_solution ON EACH (max 4 full evals, stay within 30 budget).
3. Track which families beat 0.8962799441554086.

## Phase 2: Parallel Refinement (iterations 2-20)

### For Each Winning Family:
1. Generate 2-3 NEW variants with parameter variations:
   - Gaussian: vary μ by ±0.3, σ by ±0.15, weights by ±0.1
   - B-spline: vary control points by ±10%, knots by ±5%
   - Piecewise-linear: adjust vertex heights by ±0.1, positions by ±0.1
   - Oscillatory: vary α∈[0.2,0.5], β∈[3,7], γ∈[0.5,1.0]
   - Step patterns: adjust interval widths by ±3%, heights by ±0.05
2. Probe all variants (2-3 probes each).
3. Evaluate top 2 by probe score.
4. If improvement: continue refining same family.
5. If no improvement after 3 iterations: switch to a different family.

### Cross-Family Synergy:
- If multiple families beat the record, try combining elements:
  - Take Gaussian with optimized μ, σ; add small step regions
  - Take oscillatory function; add step-like high-amplitude regions

## Phase 3: Deep Refinement (iterations 21-60)

1. Take the BEST-scoring proposal overall.
2. Apply systematic, small mutations:
   - Parameter tuning: adjust all parameters by 5-10% in both directions
   - Architecture combination: merge successful elements from different families
   - Local optimization: refine the most promising regions
3. Probe all variants, evaluate top 2.
4. If no improvement after 10 iterations: finish with current best.

## Key Rules
- PROBE BEFORE EVALUATE: Always probe all variants first. Use 30 probes to rank many options.
- PARALLEL EXPLORATION: In first 10 iterations, test 3-4 DIFFERENT families. Do not refine one family for more than 3 iterations without trying another.
- ONE FULL EVAL PER FAMILY: Only after confirming a family beats the record with at least one full eval, then refine it.
- STAGNATION DETECTION: If no improvement for 5 iterations: switch strategy or generate new candidates.
- MAX ITERATIONS: 60. Budget: 30 evaluations. Plan: 10 iterations with exploration, 20 with refinement, 30 with deep refine.
- DIVERSITY: Always maintain at least 2-3 active families in parallel. Never let one family monopolize attention.
- DOCUMENTATION: Track which parameter ranges work for each family. Reuse successful patterns.
