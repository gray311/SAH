You are optimizing the C2 constant for the second autocorrelation inequality:
C2 = ||f*f||_2^2 / ((∫f)^2 ||f*f||_∞)

Target: Beat 0.8962799441554086 (current record using step functions).

CRITICAL INSIGHT: Step functions WIN because they create sharp peaks in convolution.
Smooth functions (Gaussian, B-spline, oscillatory) SMOOTH out these peaks and UNDERPERFORM.

STRATEGY - STEP-PATTERN SEARCH WITHIN EXISTING GRID:

PHASE 1 (iterations 1-20): STEP PATTERN DIVERSIFICATION
1. Analyze current best step pattern's structure (levels, positions, heights)
2. Generate NEW step patterns by VARIING:
   - Number of levels (5-12 levels)
   - Level heights (asymmetric: high middle, low sides; or low-middle-high)
   - Support width (narrow vs wide)
   - Shift patterns (asymmetric placement)
3. For each new pattern: probe ALL, evaluate TOP 2
4. If beat record: switch to Phase 2. Otherwise: generate MORE step variations

PHASE 2 (iterations 21-30): TARGETED STEP REFINEMENT
1. Take best step pattern from Phase 1
2. Try local mutations: adjust ONE level height by ±10%, shift ONE boundary by ±5%, add/remove ONE level
3. Probe all variants, evaluate top 1
4. If no improvement: go back to Phase 1 with NEW structural changes

RULES:
- NEVER try Gaussian/B-spline/oscillatory - they smooth convolution peaks and fail
- Always use probe_solution to rank 8-15 step variants before full evals (30 probe budget)
- If iteration 12+: try completely NEW step architectures (different number of levels)
- Ensure f >= 0 using jax.nn.relu or jax.numpy.maximum
