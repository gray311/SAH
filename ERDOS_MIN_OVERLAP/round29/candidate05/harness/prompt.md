Erdos C5: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx with integral(h)=1.

CURRENT BEST: c5 <= 0.38092303510845016 (combined_score = 1.0)
GOAL: Find c5 < 0.38092303510845016 (combined_score > 1.0)

KEY INSIGHT: The current ErdosOptimizer uses fixed hyperparameters that may be suboptimal. 
Instead of generating diverse patterns and hoping training improves them, use a COARSE-TO-FINE 
SEARCH STRATEGY: train on coarse grids (400-800 intervals) first to find general structure, 
then refine on finer grids (1600-3200). This reduces early training noise and helps find 
better local optima.

STRATEGY:
1. FIRST: Train with coarse discretization (num_intervals=400, num_steps=15000) to find rough h(x)
2. THEN: Fine-tune with finer discretization (num_intervals=1600, num_steps=45000) 
3. TRY DIFFERENT INITIALIZATIONS: Use multiple restarts with varied initial h(x) (not just random)
4. ADAPTIVE HYPERPARAMETERS: If training stalls (no improvement in last 5000 steps), adjust lr or penalty

EVALUATION: Use probe_solution to screen candidates before full evaluation. Only evaluate when 
c5_bound < 0.375 (combined_score > 1.01).


When editing: TEST COARSE-TO-FINE by setting num_intervals=400, num_steps=15000 first. Then refine.
NEVER jump directly to num_intervals=800 with full budget - coarse search first!


Hyperparameters to try:
- num_intervals: 400 (coarse), 800, 1600, 3200 (fine)
- base_learning_rate: 0.001 (coarse), 0.005, 0.01 (fine)
- penalty_strength: 30 (coarse), 60, 100 (fine)
- num_steps: 15000 (coarse), 30000, 45000, 60000 (fine)
- num_restarts: 5 (more restarts for coarse search)


Evaluate ONLY when combined_score > 1.01 (c5_bound < 0.375)
