You are optimizing a program to find a step function h: [0,2] → [0,1] minimizing:
max_k ∫ h(x)(1-h(x+k)) dx over k ∈ [0,2].

The evaluator rewards lower values of this maximum correlation (higher combined_score).
Current best: 0.38092303510845016. You must beat this.

The seed program uses gradient descent, but this is NOT effective for discrete step
function construction. Instead, systematically try CONSTRUCTING step functions with
specific piecewise constant patterns.

Strategy:
1. Use `construct_step_function` to generate structured step functions with
   chosen breakpoints and values in [0,1].
2. Ensure ∫h(x)dx = 1.0 exactly by choosing appropriate coefficients.
3. Test different partition structures: uniform, clustered, periodic, etc.
4. For promising candidates, use gradient-based refinement as a polishing step.
5. Stop when combined_score > 1.0 (meaning c5_bound < 0.38092303510845016).

Tools:
- `edit_solution`: Change the EVOLVE-BLOCK region with SEARCH/REPLACE or full rewrite.
- `evaluate_solution`: Run and get combined_score (higher=better).
- `probe_solution`: Cheap evaluation on 2000 subsamples (approximate, doesn't consume budget).
- `construct_step_function`: Build structured step functions with specified structure.
- `finish`: End when you cannot improve further.
