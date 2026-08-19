---
name: simple-step-strategy
description: Generate exact integral=1 step functions, compute c5 via FFT, evaluate if c5 < 0.38.
---

# Step Function Strategy

Three patterns with integral=1 by construction:
1. Bipartite: h=2 on [0.5,1)
2. Two-block: h=1 on [0,0.5) and [1,1.5)
3. Tri-step: h=2.5 on [0.4,0.8)

Workflow:
1. generate_valid_simple -> 3 candidates
2. Check c5_bound < 0.38
3. evaluate_solution on accepted
4. If no progress: regenerate with higher T

Budget: 30 evals, max 4-5 full evaluations
