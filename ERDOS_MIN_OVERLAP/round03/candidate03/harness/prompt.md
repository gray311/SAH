You are solving the Erdős minimum overlap problem: find a step function h: [0,2]→[0,1] with integral(h)=1 that minimizes max_k ∫ h(x)(1-h(x+k))dx.

Current best bound: C5 ≤ 0.38092303510845016. Goal: exceed it (combined_score > 1.0).

Critical insight: The optimal solution is a DISCRETE step function, not a smooth function. Gradient descent fails here. You must enumerate COMBINATORIAL CONSTRUCTIONS.

Proven constructions to test (implement as step functions exactly):

1. **2-periodic bimodal**: h(x)=1 on [a, a+δ]∪[1-a, 1-a+δ], 0 elsewhere. Vary a∈{0, 0.1,...,1.0}, δ∈{0.05,0.08,0.1,0.12,0.15}. Normalize to integral=1.

2. **3-periodic**: h(x)=1 on [a,a+δ]∪[a+0.667,a+0.667+δ]∪[a+1.333,a+1.333+δ] (wrap at 2). Test all (a,δ) pairs.

3. **Golomb-5 construction**: Place 5 peaks at positions from optimal Golomb ruler [0,1,4,9,11] scaled to [0,2]. Use exact step functions (widths as discrete fractions).

4. **General N-periodic**: For N=4,5,7: place mass at N equally-spaced locations with width δ. Vary δ to satisfy integral=1.

Algorithm:
PHASE 1: Generate 50+ candidate step functions by enumerating (period_type, a, δ, N) tuples.
PHASE 2: For each candidate, compute c5_bound directly using FFT (no optimization, exact calculation).
PHASE 3: Rank by c5_bound, keep top 5 candidates.
PHASE 4: Run full evaluate_solution on top 5.

DO NOT use gradient descent. DO NOT use sigmoid smoothing. Implement step functions with exact floor/ceiling logic.

Tool edits required:
- Remove all optimizer imports (optax, jax gradient-based code).
- Implement exact step function evaluator that takes period_type, a, δ, N as parameters.
- Enumerate candidates systematically, compute c5_bound directly via FFT.
- Report best c5_bound found.
