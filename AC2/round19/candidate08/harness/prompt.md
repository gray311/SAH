You are a C2 constant optimizer. Current best: 0.8962799441554086 (step functions).

CRITICAL: The seed's step-function patterns are under-explored, not trapped. 
STEP FUNCTIONS CAN STILL IMPROVE C2! Do NOT jump to smooth functions until after exhaustive step search.

STRATEGY - STEP FUNCTION OPTIMIZATION FIRST:

PHASE 1 (iterations 1-20): STEP FUNCTION DIVERSITY
1. Analyze current best's convolution profile (using existing methods)
2. Generate 8 step-function variants: vary level count (3-7 levels), heights (0.5-3.0), positions (asymmetric)
3. Use probe_solution on ALL 8 (accept approximate scores for steps)
4. Evaluate TOP 2 by probe score (max 2 evals per phase)
5. If neither beats record: generate NEW step families (fractal, mirror-symmetric, clustered peaks)

PHASE 2 (iterations 21-30): REFINEMENT OR SMOOTH FUNCTIONS
- If step functions beat record: refine with small mutations (+/-3% width, +/-0.03 height)
- If no improvement after 15 iterations: THEN try smooth functions (Gaussian mixtures) with 3 evals

RULES:
- NEVER call generate_candidates for smooth functions until iteration 20+ with no step improvements
- Always ensure f >= 0 with jax.nn.softplus or max(0, ·)
- For steps: use f = f.at[start:end].set(value) for mutability
- Use existing probe_solution (approximate but good enough for relative ranking)
