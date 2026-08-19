You are an expert in functional analysis, harmonic analysis, and mathematical discovery.
Your mission: Surpass C2 = 0.8962799441554086 (the current world record) for the second autocorrelation inequality constant.

The seed program uses gradient descent on a parametric function representation. While this found 0.999789xrecord, it is stuck in local optima.

CORE INSIGHT: Step functions and their combinations (used by AlphaEvolve) achieve the record. Pure gradient descent struggles.

STRATEGY:
1. Use probe_solution to explore function variants cheaply (first ~2000 discretization points)
2. Implement multi-strategy exploration:
   - Strategy A: Refine existing continuous optimization with adaptive learning rates
   - Strategy B: Construct piecewise linear/step functions explicitly (combining known good building blocks)
   - Strategy C: Try Fourier-space optimization with positivity constraints
3. Only call evaluate_solution once you have strong probe evidence a variant will beat record
4. If stuck near 0.999789, explicitly try step-function hybrids: combine a Gaussian center with step-function wings

Preserve the entry function. Make one substantive change per turn. Never evaluate the same code twice.
