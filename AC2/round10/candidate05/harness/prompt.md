You are optimizing functions to maximize C₂ = ||f★f||₂² / ((∫f)²||f★f||∞) in the second autocorrelation inequality.

The seed program uses 13 pre-defined step function patterns. Your goal is NOT to make small parameter tweaks - you must discover NEW pattern architectures that exceed the current best of 1.03492.

Strategy:
1. Explore DIVERSE function structures: try radically different numbers of steps (200-600 intervals), new symmetry properties (even/odd/asymmetric), and novel pattern shapes (triangular, multi-peak, plateau, exponential-like)
2. Use probe_solution to cheaply screen 5-10 diverse structural variants per iteration
3. Only call evaluate_solution on the single best probe result
4. When stalled, completely reinitialize with a new pattern class from a different "archetype" (e.g., from narrow-peaked to wide-plateaued to multi-armed)
5. Track which archetype produced the best score, and continue mutating within that successful archetype's family
6. Never make only tiny parameter changes - always try at least one structural innovation per evaluation

Key insight: The seed's 13 patterns may already be locally optimized. You need to find a NEW starting point, then refine it. Use structural diversity + focused refinement.
