You are an expert in harmonic analysis and the Erdős minimum overlap problem.

Goal: Beat C5 ≤ 0.38092303510845016 by finding a step function h: [0,2]→[0,1] with ∫h=1 that minimizes max_k ∫h(x)(1−h(x+k))dx.

STRATEGY (follow this order):
1) BEFORE optimizing, call bound_probe(h_initial) to get a fast approximate score.
2) Generate diverse initializations using construct_structured_init().
3) For each candidate h, compute its bound_probe. Only optimize those with bound_probe < 0.385.
4) After optimizing a few candidates, use bound_probe to rank them and keep only the top 3 for full evaluation.
5) Run full evaluate_solution on the top candidates.

Why this works:
- bound_probe is 10x faster than evaluate_solution and does not consume the limited eval budget.
- Random/unstructured candidates waste evaluations. Filter them out first.
- Optimizing from bad starts often converges to worse local minima.

Target: combined_score > 1.0 (i.e., c5_bound < 0.380923).

Edit instructions:
- Implement bound_probe() as a cheap FFT-based evaluator using subsampling.
- Implement construct_structured_init() to generate 4–6 diverse initial h (bimodal peaks, triangular levels, periodic pattern, Golomb ruler-inspired, piecewise-constant).
- Integrate bound_probe into the workflow: generate → probe → optimize promising → eval top.
