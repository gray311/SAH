---
name: discovery-optimization
description: "Use structural_analyzer to check constraint satisfaction and targeted_mutations to explore diverse step functions."
---

# Erdos C5 Optimization - Structural Analysis Approach
## Phase 1: Structural Analysis (MUST CALL FIRST)
1. CALL structural_analyzer ON THE CURRENT BEST PROGRAM - This returns the h array in numpy format - Reports if integral(h) = 1 is satisfied - Reports if all h values are in [0,1] - Identifies the step count and region boundaries
2. EXAMINE the structural report - If constraints are violated, regenerate from scratch - If constraints are satisfied, note the region boundaries and step heights
3. Call targeted_mutations with the structural report as context - Request mutations that preserve structure but improve overlap - Try multiple mutation types: "bipartite", "tri-modal", "uniform-noise"
## Phase 2: Validation Before Evaluation
1. For EACH mutation candidate: - CALL structural_analyzer on the candidate - If integral(h) != 1 or h values outside [0,1], DISCARD IMMEDIATELY - If constraints satisfied, call probe_solution to screen
2. Only call evaluate_solution on candidates with: - c5_bound < 0.375 (from probe) - Constraint satisfaction confirmed
## Phase 3: Iteration
1. If no improvement after 3 iterations: - Try a COMPLETELY NEW structure (bipartite, then tri-modal) - Do NOT refine the same structure repeatedly
## Key Rules - ALWAYS call structural_analyzer before evaluate_solution - DISCARD candidates that fail constraint checks - Use probe_solution to screen before full evaluation - Evaluate only when c5_bound < 0.375
