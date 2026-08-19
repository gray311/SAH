---
name: two-stage-step-optimization
description: Two-stage optimization - first explore simple step variants, then expand to complex architectures. Prevents premature complexity and ensures viable candidates.
---

# Two-Stage Step Optimization for C2 Maximization

## Why This Works
The seed's step-function patterns are proven to work (1.042 combined_score).
Complex architectures (Gaussian, splines) often have bugs or numerical issues.
Start simple, find a working variant, THEN expand.

## Stage 1: Simple Step Exploration (iterations 1-12)
1. Analyze current best's pattern structure
2. Generate 2-3 variants with SMALL mutations:
   - Height adjustment: ±10-15% on existing levels
   - Position shift: move level boundaries by ±10%
   - Add one level: insert a new level between existing ones
   - Remove one level: simplify an over-parameterized pattern
3. Probe ALL variants (use 3-5 probes per iteration)
4. Evaluate TOP 1 variant (1 eval per iteration)
5. Track which mutation type works best

## Stage 2: Controlled Complexity (iterations 13-20)
ONLY if Stage 1 found a variant with combined_score > 1.0:
1. Take the best Stage 1 winner
2. Generate 2 variants that ADD ONE level of complexity:
   - Split one existing level into two
   - Add a small "wing" level at the edges
   - Create asymmetry with different left/right heights
3. Probe both, evaluate top 1
4. If no improvement after 2 iterations: revert to Stage 1 mutations

## Stage 3: Radical Redesign (iterations 21-30)
ONLY if all else fails:
1. Generate ONE simple variant from a DIFFERENT family:
   - Gaussian mixture with 2-3 components (smooth, no oscillations)
   - Piecewise-linear with 3-4 segments (simple, monotonic)
2. Probe it, evaluate if promising
3. If fails, return to Stage 1 with fresh step mutations

## Key Rules
- NEVER generate 5 diverse families at once - too error-prone
- ALWAYS start with simple step variants (guaranteed to work)
- Use probes to filter: only evaluate if probe_score > 1.0
- If stuck at iteration 10: try different mutation types, not new families
- Maximum 1 full evaluation per iteration - save budget for exploration
