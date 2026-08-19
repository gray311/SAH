Erdos minimum overlap problem: FIND A STEP FUNCTION h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score (c5_bound < 0.380923).

CRITICAL: The seed optimizer uses gradient descent on sigmoid-transformed vectors. This finds smooth curves, not optimal step functions.

NEW STRATEGY: REPLACE THE OPTIMIZER with direct combinatorial search over step-function parameters.

1. Build a NEW optimizer class that directly specifies step-function breakpoints and levels

2. Generate diverse candidates by varying:
   - Number of intervals (4-16)
   - Breakpoint locations (rational grids)
   - Level assignments (binary or ternary: 0, 0.5, 1)

3. Use generate_step_candidates tool to get 8-12 pre-simulated candidates

4. Each candidate must satisfy: sum(h) * dx = 1 (scale levels to integrate to 1)

5. Evaluate ONLY candidates with analytical c5 < 0.36

6. If no improvement after 2 batches, try RATIONAL BREAKPOINT patterns (denominators 3,4,6,8,12)

7. EDIT the EVOLVE-BLOCK to completely replace ErdosOptimizer with StepFunctionSearcher
8. Keep num_restarts=3, but each restart generates independent step-function configs

Key insight: Optimal solutions are piecewise-constant, not smooth sigmoid curves.
