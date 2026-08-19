Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score (combined_score > 1.0, meaning c5_bound < 0.380923).

Strategy:

1. The seed program has 15 initialization patterns but may have code issues. Use probe_solution to test candidates cheaply.

2. Generate structural variants: modify the wave patterns, try different Golomb rulers, experiment with Fourier-based constructions.

3. Use the new tool structural_variants() to get 5 diverse program edits (modifying the pattern generation code).

4. Probe all 5 variants cheaply (uses probe budget, no full evals yet).

5. Call evaluate_solution on the best 2-3 probes (lowest c5_bound).

6. If no improvement, use structural_variants again with different seeds/strategies.

7. Keep num_intervals=800 (higher resolution = more accurate c5), penalty=61 (good constraint satisfaction), steps=120000 (enough training).

8. Budget: 20 evals total - use probes aggressively, full evals only on promising variants.
