---
name: discovery-optimization
description: "Mathematical optimization for Erd\u0151s minimum overlap problem. The solver must find a step function h that minimizes max_k \u222bh(x)(1-h(x+k))dx while satisfying \u222bh=1. Use structured constructions, informed initialization, and targeted perturbations. The seed uses 800 intervals; consider starting simpler and refining."
---

# Erdős Minimum Overlap Problem Solver

## Problem
Find step function h: [0,2]→[0,1] with ∫h=1 minimizing max_k ∫h(x)(1-h(x+k))dx.
Target: beat C5 ≤ 0.380923 (combined_score > 1.0).

## Strategy

### Phase 1: Understand the Seed
- Seed uses 800 intervals, Adam optimizer, 59000 steps
- Already achieves 0.999641 (very close to 1.0 = current best bound)
- Uses multi-restart with 12 pattern initializations

### Phase 2: Key Improvements

1. **SIMPLER INITIALIZATION**: Start with fewer intervals (100-200) to converge faster, then refine.

2. **STRUCTURED STEP FUNCTIONS**: Instead of continuous functions, explicitly design piecewise constant functions:
   - Try 3-5 steps: e.g., h = [1,1,...,1, 0,0,...,0] with exact integral=1
   - Try alternating patterns: [a,b,a,b,...] where a,b chosen to satisfy constraints

3. **INFORMED PERTURBATIONS**: From a working solution:
   - Move one step boundary by ±10 intervals
   - Change one step height by ±0.1 (normalize to keep integral=1)
   - Add a small step at an underutilized region

4. **CONSTRAINT HANDLING**: 
   - Don't rely on penalty alone - explicitly normalize h to satisfy ∫h=1
   - Consider constrained optimization or post-hoc normalization

### Phase 3: Evaluation Order

1. First, reduce intervals and retrain from structured initialization
2. Then, add complexity (more intervals) to refine the solution
3. Finally, fine-tune the best solution found

## Warning
Only 30 evaluations. Each must be substantive. Don't waste on trivial changes.

## Tools
- edit_solution: Change EVOLVE-BLOCK with targeted diffs
- evaluate_solution: Score your solution (combined_score > 1 means new best)
- finish: Submit your best result when done
