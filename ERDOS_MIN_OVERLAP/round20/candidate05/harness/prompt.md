Erdos minimum overlap problem: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

Constraint: integral(h) = 1 exactly.

Current best: C5 <= 0.38092303510845016.

Goal: Beat seed score of 0.999945 (c5_bound < 0.380923).

Method (CRITICAL):

1. The seed optimizer trains for 59000 steps per candidate. This is too slow - we cannot afford 59000 steps.

2. Replace the training loop with a FAST analytical scoring approach: use FFT-based c5 computation directly on the latent vector (no gradient descent).

3. Generate MANY diverse candidates using structural patterns (Golomb ruler, bipartite, tri-modal, threshold patterns).

4. Score candidates analytically (FFT) to get c5_bound instantly.

5. Only run full optimization on the BEST 1-3 candidates (those with c5_bound < 0.36).

6. If full optimization confirms improvement, submit.

7. Key insight: The seed optimizer is a distraction - we need analytical scoring, not training.
