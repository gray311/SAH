Maximize C2 constant in second autocorrelation inequality.
Current best: 0.8962799441554086. Target: SURPASS THIS.

Strategy:
1. EXPLORE STRUCTURED FUNCTION CLASSES: piecewise-constant, spline, Fourier-mode.
2. MULTI-SCALE OPTIMIZATION: coarse (15 intervals) to fine (60 intervals).
3. PROBE BEFORE EVALUATE: probe 10 variants, evaluate best 2-3.
4. POSITIVITY: f(x) >= 0 via softplus.
5. DETERMINISM: fixed seeds (42).

Tools: edit_solution, evaluate_solution (~20 budget), probe_solution (~20 calls), finish.

Always: probe to rank to evaluate top to iterate.
