You are an expert in harmonic analysis and combinatorial optimization. Your task is to find a step function h: [0,2] -> [0,1] that minimizes the maximum overlap integral max_k ∫ h(x)(1-h(x+k)) dx.

**OBJECTIVE**: Maximize combined_score = 0.38092303510845016 / c5_bound
Current best: 0.38092303510845016 (so c5_bound = 0.38092303510845016)
Goal: Find c5_bound < 0.38092303510845016 to get combined_score > 1.0

**CONSTRAINTS**: 
- h(x) ∈ [0,1] for all x
- ∫₀² h(x) dx = 1 (exactly)
- h is a step function (piecewise constant)

**CRITICAL INSIGHT**: The gradient-based optimizer in the seed is trapped in poor local optima. 
DON'T try to tune the optimizer. Instead, CONSTRUCT candidate solutions directly using mathematical reasoning.

**SEARCH STRATEGY**: Use a hybrid approach:
1. **Construct** candidate step functions with SPECIFIC structural patterns
2. **Evaluate** each construction immediately
3. **Iterate** by modifying promising candidates (change breakpoints, adjust heights)
4. Use metaheuristic principles: try many diverse constructions, keep the best

**STRATEGIC PATTERNS TO EXPLORE**:
- Symmetric step functions around x=1
- Two-level step functions with specific plateau configurations
- Functions that concentrate mass in specific regions to minimize overlap
- Try varying the number of steps: 2, 3, 4, 5, 6, 8, 10 steps
- Breakpoints at rational locations: 1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8, 1, etc.

**EXECUTION**: Complete rewrites are essential. Each edit should be a fresh construction attempt, not a tweak.
