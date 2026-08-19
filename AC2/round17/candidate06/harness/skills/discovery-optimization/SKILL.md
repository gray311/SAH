---
name: discovery-optimization
description: "Parallel architecture exploration with probe-based filtering. Generate diverse function families, probe all to rank, evaluate top 3-4, then refine winners."
---

# C₂ Maximizer: Parallel Architecture Exploration Protocol

## Core Principle

The step-function record is a LOCAL optimum. Beat it by EXPLORING DIFFERENT FUNCTION FAMILIES IN PARALLEL, not by sequentially refining step patterns.

## Phase 1: Parallel Exploration (iterations 1-20)

### Step 1: Generate Diverse Candidates
1. Call generate_candidates immediately (at iteration 1).
2. Expect 3-5 proposals across different families:
   - Gaussian mixtures (smooth, multi-peaked)
   - B-spline basis (flexible smooth transitions)
   - Piecewise-linear (controlled smoothness)
   - Oscillatory with decay (structured convolutions)
   - Multi-level improved steps (asymmetric heights/positions)
   - Hybrid approaches (step-spline combinations)

### Step 2: Probe-Based Ranking
1. For EACH proposal, call probe_solution to get approximate scores.
2. You have 30 probes - use them to RANK all proposals.
3. Generate slight variations of top-ranked proposals (2-3 variants each).
4. Probe ALL variants to build a complete ranking.

### Step 3: Full Evaluation
1. Select TOP 3-4 proposals by probe score.
2. Call evaluate_solution ON EACH (max 3-4 full evals per iteration).
3. Track which families beat the current best (0.8962799441554086).

### Step 4: Decision Point
- If ANY family beats the record: move to Phase 2 (refine winners).
- If NO family beats the record by iteration 15: generate a NEW set of candidates with different parameters.

## Phase 2: Parallel Refinement (iterations 21-50)

### For Each Winning Family:
1. Generate 2-3 NEW variants with parameter variations:
   - Gaussian: vary μ, σ, weights by ±10%
   - B-spline: vary knot positions, control point magnitudes
   - Piecewise-linear: adjust vertex heights/positions
   - Oscillatory: vary α, β, γ parameters
2. Probe all variants.
3. Evaluate top 2 by probe score.
4. If improvement: continue refining same family.
5. If no improvement after 3 iterations: switch to a different family or generate new candidates.

### Cross-Family Synergy:
- If multiple families beat the record, try combining elements:
  - Take the best step pattern and add small Gaussian bumps
  - Take the best oscillatory function and add step-like regions

## Phase 3: Deep Refinement (iterations 51-60)

1. Take the BEST-scoring proposal overall.
2. Apply systematic, small mutations:
   - Parameter tuning: adjust all parameters by 5-10% in both directions
   - Architecture combination: merge successful elements from different families
   - Local optimization: refine the most promising regions
3. Probe all variants, evaluate top 2.
4. If no improvement: finish with current best.

## Key Rules
- PROBE BEFORE EVALUATE: Always probe all variants first. Use 30 probes to rank many options.
- PARALLEL EXPLORATION: In first 20 iterations, test 3-4 DIFFERENT families. Do not refine one family for more than 3 iterations without trying another.
- ONE FULL EVAL PER FAMILY: Only after confirming a family beats the record with at least one full eval, then refine it.
- STAGNATION DETECTION: If no improvement for 5 iterations: switch strategy or generate new candidates.
- MAX ITERATIONS: 60. Budget: 30 evaluations. Plan: 20 iterations with probing, 25 with refine, 15 with deep refine.
- DIVERSITY: Always maintain at least 2-3 active families in parallel. Never let one family monopolize attention.
- DOCUMENTATION: Track which parameter ranges work for each family. Reuse successful patterns.
