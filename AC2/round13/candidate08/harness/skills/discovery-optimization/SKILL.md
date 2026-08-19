---
name: discovery-optimization
description: "Diverse function family exploration for C_2 maximization. Generate candidates from \nmultiple mathematical families (Gaussian, spline, oscillatory, asymmetric) and use \nprobe-based filtering to identify promising architectures before full evaluation. \nParallel exploration beats sequential refinement. Avoid getting stuck in step-function \nlocal optima by systematically trying fundamentally different function classes."
---

# C_2 Maximizer: Diverse Function Family Exploration Protocol

## Core Principle

The step-function record (0.8962799441554086) is a LOCAL optimum. To beat it, you MUST 
explore COMPLETELY DIFFERENT function architectures with fundamentally different convolution 
structures. Sequential refinement of step functions will never break through.

## Phase 1: Initial Diverse Generation (Iterations 1-5)

1. CALL generate_candidates ONCE to get 3-5 function proposals from DIFFERENT families:
   - Gaussian mixtures (smooth, multi-peaked convolutions)
   - B-spline basis (flexible smooth transitions)
   - Oscillatory with decay (structured multi-peak convolutions)
   - Asymmetric multi-peaked functions (strategic peak placement)
   - Piecewise-linear with smooth transitions

2. For each proposal, CALL probe_solution to get approximate scores (30 budget total).

3. RANK by probe score and select TOP 2-3 for full evaluation with evaluate_solution.

4. CRITICAL: If a proposal fails to beat the record, DISCARD IT. Do not spend 
   multiple iterations refining a failed architecture.

## Phase 2: Parallel Pipeline Exploration (Iterations 6+)

Maintain a "pipeline" of active function families:

- For EACH family that has shown promise (probe score > 1.02):
  * Implement 1-2 small mutations using edit_solution
  * Evaluate each variant (ONE evaluation per variant)
  * If beats record: keep as current best, but DON'T exhaust - try a NEW family next

- For EACH family that has failed:
  * Either try a different proposal from the same family (if one remains)
  * OR immediately switch to a completely new family

## Phase 3: Stalled Recovery

If no improvement for 8+ iterations:
1. Call generate_candidates with a FRESH random seed
2. Try families you may have skipped (e.g., if only tried smooth functions, try sharp asymmetric ones)

## Phase 4: Final Push

As budget depletes:
- Focus on the single best-performing function family
- Make very small, targeted mutations
- Evaluate each carefully
- If still below record after budget exhaustion, report the best achieved

## Key Rules

1. PARALLEL > SEQUENTIAL: Never refine one function type for 5+ iterations without 
   trying a completely different architecture.

2. DIVERSE GENERATION: Each generate_candidates call should produce proposals from 
   DIFFERENT families, not variants of the same type.

3. EARLY DISCARD: Failed proposals are dead. Move on quickly.

4. PROBE FIRST: Always use probe to filter before spending full evaluations (EXCEPT this task - use evaluate directly per instructions).

5. COMPLETE REWRITES: For NEW function classes, write complete code from scratch, 
   not SEARCH/REPLACE patches on step functions.
