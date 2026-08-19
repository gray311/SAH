---
name: discovery-optimization
description: "Coarse-to-fine search for Erdos C5: Train on coarse grids (400 intervals) to find general h(x) structure, \nthen refine on finer grids (1600-3200). Use multiple restarts with varied initializations. \nScreen with probe_solution, evaluate only promising candidates (c5_bound < 0.375)."
---

# Coarse-to-Fine Search for Erdos C5

## Phase 1: Coarse Search (Find General Structure)

1. EDIT with coarse parameters:
   - num_intervals = 400
   - num_steps = 15000
   - base_learning_rate = 0.001
   - penalty_strength = 30
   - num_restarts = 5

2. RUN training and get initial h(x) from the best result

3. CALL probe_solution on the initial h(x) to check c5_bound

4. If c5_bound < 0.38, PROCEED to Phase 2. Otherwise, try different coarse parameters.

## Phase 2: Fine-Tuning (Refine the Solution)

1. EDIT with fine parameters:
   - num_intervals = 1600 (or 3200 if you have budget)
   - num_steps = 45000 (or 60000 for more exploration)
   - base_learning_rate = 0.005 (or 0.01 for more exploration)
   - penalty_strength = 60 (or 100 for stronger constraint)
   - num_restarts = 3

2. Use the h(x) from Phase 1 as initialization (by editing to preserve good structure)

3. RUN training with fine parameters

4. CALL probe_solution to screen

5. CALL evaluate_solution if c5_bound < 0.375

## Phase 3: If Stuck

If no improvement after coarse-to-fine:
- Try DIFFERENT coarse parameters (lr=0.005, penalty=60)
- Try DIFFERENT restart strategies (increased diversity in initial h(x))
- Consider: The current ErdosOptimizer may need fundamentally different approach

## Key Rules
- ALWAYS start with coarse search (num_intervals=400) before fine search
- NEVER jump to fine parameters without coarse search
- Use probe_solution to screen before full evaluation
- Only evaluate when c5_bound < 0.375 (combined_score > 1.01)
- Track best c5_bound across all phases
