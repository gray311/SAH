---
name: step-refinement-playbook
description: Systematic step-pattern refinement to beat the 1.03896 record. Focus on small, targeted mutations before exploring hybrids or non-step functions.
---

# Step-Pattern Refinement Playbook for C₂ Maximization

## Objective

Beat the current combined_score of 1.03896 (C₂ = 0.89628) by systematically refining step patterns.

## Core Insight

Step functions WORK for this problem. The record is LOCAL but beatable via SMALL, targeted mutations.
Smooth functions (Gaussian, splines) typically UNDERPERFORM step functions for the C₂ ratio.

## Phase 1: Structural Analysis (Iteration 1)

1. Call analyze_step_pattern ONCE to extract:
   - Number of levels (typically 4-6)
   - Height values per level
   - Interval positions (as fraction of domain)
   - Symmetry properties (symmetric vs asymmetric)

2. Identify "weak links":
   - Level pairs with largest height differences
   - Narrowest intervals (may need widening)
   - Excessively wide intervals (may need contracting)

## Phase 2: Guided Mutation Sequence (Iterations 2-15)

Execute mutations in this order:

**STEP 1: Height Perturbation** (DO THIS FIRST)
- Increase core/middle level height by 0.03-0.06
- Decrease wing/outer levels by 0.02-0.04
- Create slight asymmetry: left +0.025, right -0.025
- Generate 3-5 variants with different perturbation magnitudes

**STEP 2: Width Optimization**
- Expand the widest interval by 5-7%
- Contract the narrowest interval by 3-5%
- Keep total domain length constant
- Generate 2-3 variants

**STEP 3: Asymmetry Breaking**
- Take a symmetric pattern and introduce left-right imbalance
- Left side: +0.02 to +0.03
- Right side: -0.02 to -0.03
- Generate 2-3 variants

**STEP 4: Level Addition**
- Split the middle interval into two
- Add intermediate level(s) between existing levels
- Go from 4→5 or 5→6 levels
- Generate 2-3 variants

## Phase 3: Hybrid Patterns (Iterations 16-25)

If single-pattern refinement stalls for 6+ iterations:

1. Combine TWO seed patterns:
   - Take left 40% of pattern A, right 60% of pattern B
   - Or: left 50% of pattern A, middle 30% of pattern B, right 20% of pattern C
2. Smooth the transition zone with a linear ramp
3. Generate 2-3 hybrid variants

## Phase 4: Diverse Exploration (Iteration 26+)

Only if stuck for 10+ iterations:

1. Call generate_candidates for non-step families
2. Use probe_solution to filter to top 3-5
3. Call evaluate_solution ONCE per candidate
4. If nothing beats record, RETURN TO STEP-PATTERN REFINEMENT

## Evaluation Protocol

Every iteration:
1. Call analyze_step_pattern (first iteration only)
2. Call step_mutator to get 10-12 mutations
3. Call probe_solution for all 10-12 mutations
4. Select top 3-5 by probe score
5. Call evaluate_solution for top 3-5
6. If any beat record: focus mutations on that type
7. If none beat record: try next mutation type or generate new batch

## Constraints & Best Practices

- f(x) ≥ 0: always apply jnp.maximum(f, 0) or use softplus
- Interval width: keep all intervals ≥2% of domain
- Height changes: start small (±0.02-0.04), increase to ±0.06-0.08 only if needed
- Width changes: ±3-7% max per interval
- Start with 600 intervals; refine to 800-1000 if stuck
- Never spend 3+ evals without probe filtering
- Maximum 2 evals per non-step family
