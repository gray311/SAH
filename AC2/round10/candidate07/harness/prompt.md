You are optimizing step functions to maximize C₂ = ||f★f||₂² / ((∫f)²||f★f||∞) in the second autocorrelation inequality.

The seed program achieves ~1.034 using 400-interval step functions with 12 pre-defined multi-level patterns.

CRITICAL: Small parameter tweaks are INSUFFICIENT. You must REARRANGE the combinatorial structure.

STRATEGY:
1. Use restructure_steps early to fundamentally alter the pattern class (merge/split steps, create new architectures)
2. Test with probe_solution (cheap approximation)
3. Only evaluate patterns with probe score > best_so_far
4. If stuck, try radically different pattern classes (pyramid, bimodal, plateau, skewed)
5. Be AGGRESSIVE - don't worry about preserving if patterns are suboptimal

Goal: Surpass 1.03492 by discovering new step function architectures.
