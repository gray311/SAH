Erdos C5 problem: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINTS: integral(h)=1 exactly, h in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h with c5_bound < 0.38092303510845016 (combined_score > 1.0).

SEARCH STRATEGY:

1. DIVERSIFIED INITIALIZATION: Start with multiple diverse initializations
   - Uniform distribution, bimodal, trimodal, Golomb ruler-like, piecewise constant
   - Use sigmoid of latent to ensure [0,1] range
   - Apply L2 projection to enforce integral=1 after each edit

2. SPECTRAL-AWARE MUTATIONS: The objective uses FFT correlation. Mutations that
   - Reduce energy at specific frequency bands corresponding to problematic shifts
   - Preserve low-frequency components (global integral constraint)
   - Try: peak shifting, peak splitting, peak merging, plateau adjustments

3. GRADIENT-INSPIRED ADJUSTMENTS: Even without gradients, try:
   - If h(x)(1-h(x+k)) is large for shift k, reduce h(x) or increase h(x+k)
   - Small perturbations (±0.05 to ±0.15) in regions of high overlap

4. PROBE-THEN-EVALUATE: Always call probe_solution before evaluate_solution.
   Only full evaluate if probe suggests c5_bound < 0.382.

5. ITERATIVE REFINEMENT: Start coarse (larger edits), refine with smaller edits.
Use the best probe results as starting point for next iteration.

TOOL USAGE:
- edit_solution: Make targeted structural changes (not random noise)
- probe_solution: Screen candidates cheaply (500 intervals, separate budget)
- evaluate_solution: Only for best probes with c5_bound < 0.382
- finish: When combined_score > 1.0
