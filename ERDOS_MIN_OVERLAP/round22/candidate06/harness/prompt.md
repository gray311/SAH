Erdos minimum overlap problem: find a STEP FUNCTION h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

KEY INSIGHT: The optimal solution is likely a TRUE STEP FUNCTION (piecewise constant with few jumps), NOT a smooth curve.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score (c5_bound < 0.380923).

STRATEGY:

1. REDUCE discretization DRAMATICALLY: Set num_intervals=50 or fewer to force step-function structure. The seed code optimizes smooth curves but we need coarse grids.

2. CHANGE initialization: Generate HARD step functions (not sigmoid curves). Use direct threshold-based h values (0, 0.5, 1.0) rather than soft sigmoid outputs.

3. EDIT to simplify the optimizer: Reduce num_steps to 5000-10000 (no need for long training when structure is fixed), keep penalty_strength=61.0.

4. Try SPECIFIC step patterns: Uniform steps (equal heights), binary steps (0 or 1), and asymmetric step functions.

5. If training-based approaches fail, EDIT to remove the optimizer entirely and use direct formula-based step functions.

6. Coarse grid = faster evaluation + natural step-function discovery. Use 8-12 evals for this structural search.
