Erdos minimum overlap (C5): Find step function h:[0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly, h in [0,1].
Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).
GOAL: Find h with c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The seed optimizer tests 15 hardcoded patterns. Most mutations should EDIT THE PATTERN DEFINITIONS, not just tune hyperparameters.

PATTERN MUTATION STRATEGY:
1. Golomb ruler (Pattern 12): marks = [0.0, 0.4, 0.8, 1.2, 1.6]. Try perturbations: [0.0, 0.35, 0.75, 1.15, 1.55], [0.0, 0.4, 0.85, 1.2, 1.65], etc.
2. Tri-modal (Pattern 14): peaks at [0.4, 1.0, 1.6]. Try narrow wide variations: widths [0.12, 0.1, 0.14], locations [0.45, 1.0, 1.55], etc.
3. Bipartite (Pattern 5/6/8/9/13): threshold at 0.5. Try asymmetric: 0.45, 0.55, 0.4, 0.6, 0.35, 0.65

WORKFLOW:
1. Call analyze_pattern_to_mutate - it will analyze current h and suggest a promising mutation
2. Apply the mutation by editing the EVOLVE-BLOCK pattern definition
3. Use probe_solution to quickly screen (approximate c5 in ~10s)
4. Only call evaluate_solution when probe shows c5_bound < 0.375

This is a structural search problem - mutate pattern structures, not hyperparameters.
