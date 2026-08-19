You are optimizing C2 for the second autocorrelation inequality.
Current best: 0.8962799441554086 (AlphaEvolve step functions).

CRITICAL: Step functions are good but not optimal. The seed explores 12 patterns, but these are LIMITED variations.
TO BEAT THE RECORD, you MUST explore NEW FUNCTION FAMILIES: piecewise linear, spline-based, Gaussian mixtures.

STRATEGY - FAMILY EXPLORATION (30 iterations, budget 30 evals):

PHASE 1 (iterations 1-12): EXPLORE NEW FAMILIES
1. Choose ONE family: Piecewise linear, Gaussian mixture, or spline
2. Generate prototype and call probe_family (new tool - fast family probe)
3. If probe >= 1.0: evaluate. If beats record: switch to Phase 2.
4. If < 1.0 after 2 tries: try next family

PHASE 2 (iterations 13-24): REFINEMENT
Generate 3 variants per family, probe all, evaluate best.

PHASE 3 (iterations 25-30): HYBRID PUSH
Try hybrids: step+Gaussian tails. Probe 2, evaluate best, submit.

RULES: DO NOT refine step patterns - explore new families. PROBE FIRST.
