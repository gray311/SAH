Erdos minimum overlap: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Goal: Beat C5=0.380923 (score > 1.0).

Strategy:
1. CALL jump_to_pattern to create diverse VALID candidates (integral=1 guaranteed).
2. Analyze c5_bound from the tool output.
3. CALL evaluate_solution on best candidates (c5 < 0.36).
4. Iterate 10-15 times, using 2 evals per iteration.
5. If stuck, try temperature=0.9 for more exploration.

Key insight: The seed optimizer trains for 59000 steps on ONE candidate. We need to try MANY different starting points - structural patterns like two-level, three-level, Golomb-like, sinusoidal that are guaranteed valid.
