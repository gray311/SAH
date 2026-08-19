---
name: discovery-optimization
description: "Create diverse structural mutations (bipartite, multi-peak, step, Gaussian) using edit_solution.\nScreen with probe_solution before full evaluation."
---

Available tools: edit_solution, evaluate_solution, probe_solution, finish.

Step 1: Read seed - ErdosOptimizer with _get_best_initialization (15+ sigmoid patterns),
         _compute_c5_bound (FFT correlation).

Step 2: Create 4 mutation types:
  (A) Bipartite: h = sigmoid(10*(t-x)) for threshold t
  (B) Multi-peak: 3-5 narrow peaks at x0,x1,x2 separated by 0.3-0.4
  (C) Step-function: piecewise constant with 3-5 steps, values in [0,1]
  (D) Gaussian: h = sigmoid(-5*(x-center)^2) + offset

Step 3: For each mutation:
  - Call probe_solution (keep if c5_bound < 0.380)
  - Call evaluate_solution on promising candidates

Step 4: Avoid just tuning hyperparameters - change function form entirely.

Key insight: seed uses sigmoid(latent) framework - break out with binary-ish,
multi-modal, or piecewise functions.
