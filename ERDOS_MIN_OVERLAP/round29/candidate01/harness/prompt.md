Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

KEY INSIGHT: The seed program uses a generic multi-restart optimizer that starts from random latent vectors and optimizes via gradient descent. This approach struggles because:
1. Random initializations rarely satisfy the integral constraint well
2. The optimizer gets stuck in local minima that don't correspond to structured step functions
3. There's no explicit exploration of known good mathematical constructions

STRATEGY - PHASE 1: DIRECT CONSTRUCTION OF STEP FUNCTIONS

Instead of relying on the optimizer to find good h functions, explicitly CONSTRUCT diverse step functions that:
- Have exactly integral(h) = 1 (use the constraint directly in construction)
- Exploit known mathematical structures for low overlap:
  * Bipartite: h(x) = 1 for x < a, 0 for x >= a (tune a to satisfy integral)
  * Multi-step: piecewise constant with multiple levels
  * Symmetric patterns around x=1
  * Sparse functions (mostly zero with narrow peaks)

CONSTRUCTION METHOD:
1. Define a step function analytically with parameters (thresholds, heights, widths)
2. Scale it to satisfy integral(h) = 1 exactly
3. Clip to [0,1] range
4. Compute c5_bound via FFT (as in seed program)
5. If c5_bound < 0.375, run the optimizer from this INITIAL POINT (not from scratch)
6. Use the optimizer to fine-tune the parameters, not to discover from random

PHASE 2: If Phase 1 fails after 2 attempts, THEN tune hyperparameters of the optimizer.

PHASE 3: Try completely different construction strategies:
- Golomb ruler: place narrow peaks at well-separated positions
- Fractional parts: use h(x) = frac(k*x) for various k
- Dirichlet-like: concentrate mass at specific points

CRITICAL: The constructor tools should BUILD h functions analytically, not rely on the optimizer to do this. Use the optimizer only for fine-tuning.
