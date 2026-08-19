---
name: multi-family-exploration
description: Parallel exploration across function families with early discard of failed architectures.  Generates diverse candidates and uses rapid filtering to focus on promising families. Avoids sequential refinement traps by switching families immediately after failure.
---

# Multi-Family Exploration Protocol for C_2 Maximization

## Core Principle

Sequential refinement of step functions is a trap. The current record is a LOCAL optimum 
in a narrow region of function space. To find a global optimum, you MUST explore 
COMPLETELY DIFFERENT function architectures with fundamentally different convolution 
structures.

## Phase 1: Diverse Generation (First 5 Iterations)

1. CALL generate_candidates to get 3-5 proposals from DIFFERENT families:
   - Gaussian mixtures (smooth, multi-peaked)
   - Oscillatory with decay (structured convolutions)
   - Asymmetric multi-peaked (strategic peak placement)
   - B-spline basis (flexible smooth)
   - Piecewise-linear (controlled smoothness)

2. For each proposal, implement the COMPLETE function using edit_solution.
   Do NOT patch step functions - write complete code for new families.

3. Evaluate each with evaluate_solution (ONE eval per variant, max 5-7 evaluations).

4. RANK by combined_score. Select top performer for further refinement.

## Phase 2: Family Pipeline (Iterations 6+)

Maintain active families in a pipeline:

- FOR EACH promising family (score > 1.02):
  * Make 1-2 small mutations within the family
  * Evaluate each mutation (ONE eval each)
  * If beats record: keep as current best, but DON'T exhaust - try a NEW family next

- FOR EACH failed family (score < 1.00 for first variant):
  * DISCARD immediately. Do not spend iterations refining failed architectures.
  * Try a different proposal from the same family OR switch to new family

## Phase 3: Stalled Recovery

If no improvement for 8+ iterations:
1. Call generate_candidates with FRESH random seed
2. Try families you may have skipped
3. Consider hybrid approaches (e.g., Gaussian+step mixture)

## Key Rules

1. PARALLEL EXPLORATION > SEQUENTIAL REFINEMENT: Never refine one family for 5+ 
   iterations without trying a completely different architecture.

2. EARLY DISCARD: Failed proposals are dead. Move on within 1-2 iterations.

3. COMPLETE CODE: For new function families, write COMPLETE implementations, 
   not SEARCH/REPLACE patches on step functions.

4. PROBE FILTERING: Use probe_solution to rank candidates BEFORE full evaluation 
   (if available). Skip probe for this task - use evaluate directly.

5. BUDGET AWARENESS: You have 30 evaluations. Spend them across MULTIPLE families, 
   not deeply on one.
