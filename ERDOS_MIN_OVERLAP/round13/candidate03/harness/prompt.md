Erdos minimum overlap problem: minimize max_k ∫ h(x)(1-h(x+k)) dx for h: [0,2]→[0,1] with ∫h=1.

Current best: C5 ≤ 0.38092303510845016
Goal: Find h with c5_bound < 0.380923 (combined_score > 1.0)

CRITICAL INSIGHT: The seed optimizer uses 12 init patterns but ALL produce functions with integral ≠ 1. The constraint penalty (61.0×) dominates the loss, so the optimizer wastes iterations fixing constraints instead of minimizing overlap.

NEW STRATEGY: Generate functions that SATISFY THE CONSTRAINT EXACTLY, then optimize overlap.

Steps:

1. CALL normalize_to_integral_one to create h with ∫h=1 EXACTLY (before any training)

2. EDIT to use this pre-normalized h as the INITIAL latent (no training needed for constraint)

3. Call probe_solution to check c5_bound of the NORMALIZED function (no training)

4. If c5_bound < 0.37, call evaluate_solution

5. If no success, EDIT to modify the FEW points where h violates constraints (e.g., adjust one interval)

Key: The constraint is the BOTTLENECK. Fix it FIRST, then optimize overlap. The seed's multi-restart is wasted if all candidates violate constraints.
