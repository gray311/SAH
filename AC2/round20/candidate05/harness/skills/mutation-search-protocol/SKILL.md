---
name: mutation-search-protocol
description: Systematically explore mutation directions to escape step-function local optimum. Target specific weaknesses with large changes.
---

# Mutation Search Protocol for C2 Maximization

## Core Strategy
Small mutations (5% changes) cannot escape the step-function local optimum. You MUST apply LARGE, TARGETED mutations that address specific mathematical weaknesses.

## Five Mutation Directions

1. WIDEN: Extend support by 10%, reduce peak height proportionally
   Why: Reduces ||f*f||_∞ more than ||f*f||₂²

2. NARROW: Reduce support by 10%, increase peak height
   Why: Concentrates L2 norm more effectively

3. ASYMMETRY: Break left-right symmetry by 5-10%
   Why: Current best is symmetric - asymmetry may improve ratio

4. SPIKE: Increase central peak by 0.15 (large change!)
   Why: Sharp peaks may improve the ratio

5. SIDE_LOBE: Add a small bump (height 0.15, width 15% of support)
   Why: Tests if adding structure helps

## Execution Flow

Phase 1: Mutation Exploration (iterations 1-20)
1. Call mutate_step_function to get all 5 mutations
2. Probe ALL 5 mutations immediately
3. Evaluate only those with probe_score > seed (0.8962799441554086)

Phase 2: Hard Restart (iteration 21+)
If all mutations fail:
- Switch to Gaussian bimodal or bimodal step patterns
- Probe 3 variants, evaluate best

## Critical Rules
- Apply LARGE changes (0.15, 10%) - not 0.05 or 5%
- Probe BEFORE evaluating
- If stuck after 2 iterations of same mutation pattern: HARD RESTART
- Each probe must test a DIFFERENT direction
