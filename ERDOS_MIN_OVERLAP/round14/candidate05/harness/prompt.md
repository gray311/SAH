You are solving the Erdős minimum overlap problem: minimize max_k ∫ h(x)(1-h(x+k)) dx for a step function h: [0,2] → [0,1] with ∫h=1.

Current best bound: C5 ≤ 0.38092303510845016
Goal: Find h with c5_bound < 0.380923 (combined_score > 1.0).

ROOT CAUSE OF FAILURE: The seed program's 12 initializations are all smooth/sigmoid-shaped and locally correlated.
The harness has been failing because it tries to "edit and train" starting from these similar seeds,
which wastes evaluations on variants that all converge to the same local optimum. The FFT-based objective
has MANY smooth valleys, and gradient-based refinement from similar starts cannot escape.

STRATEGY: Don't refine—REINVENT. The seed's 12 patterns are all thresholded sigmoids (smooth curves).
To escape, we need INITIALIZATIONS with FUNDAMENTALLY DIFFERENT SHAPE: hard-edged step functions,
piecewise constants with discontinuities, or Golomb ruler-based constructions. These break the smooth
landscape assumption and may land in different basins.

ACTION PLAN:
1. Call generate_diverse_init to create 4 hard-edged, piecewise-constant constructions (each is a
   complete step function, not a latent needing training).
2. For EACH construction, EDIT the seed to REPLACE the latent-based optimizer with this hard-edged h.
   - Set num_intervals=400 (coarser grid to reduce noise in FFT)
   - Set num_steps=1000 (fast convergence from a good start)
   - Set num_restarts=1, seed_start=0 (single run, no warmup)
3. Call probe_solution on each to get quick c5_bound estimate (500 intervals, 10s runtime).
4. Call evaluate_solution only on constructions with c5_bound < 0.37 (hard filter).
5. If none pass, EDIT to try a NEW hard-edged construction: 3 equal pieces [0,a), [a,b), [b,2] with
   heights h1,h2,h3 chosen to satisfy ∫h=1 and minimize overlap via FFT.

Key insight: The seed's optimizer is DESIGNED to refine smooth sigmoids. To find a better bound,
we need to BYPASS refinement and try completely different step functions that the seed's optimizer
would never naturally discover.
