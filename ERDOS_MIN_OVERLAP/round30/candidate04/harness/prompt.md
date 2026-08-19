Erdos C5: Minimize max_k integral h(x)(1-h(x+k))dx over h:[0,2]->[0,1] with integral(h)=1.

Current best: C5 <= 0.38092303510845016.

STRATEGY:

1. Start from seed program's initial h

2. Call local_optimize to improve h via limited-step gradient optimization (10-20 steps)

3. If no improvement, call local_optimize again with different regularization

4. Only after exhausting local_optimize, try search_patterns for diverse initializations

5. Evaluate best candidates with c5_bound < 0.375

KEY: local_optimize modifies h directly; use it before search_patterns.
