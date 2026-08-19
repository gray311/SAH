---
name: optimizer-improvement
description: Direct optimizer improvement through EVOLVE-BLOCK edits and probe screening.  The seed optimizer has 15 initialization patterns. We need to - 1. Edit hyperparameters (num_intervals, lr, num_steps, penalty_strength) 2. Add better initialization patterns 3. Screen all edits with probe_solution (500 intervals) 4. Only full-evaluate configs with c5_bound < 0.375  This is more effective than generating
---

# Direct Optimizer Improvement Strategy

## Problem
The seed optimizer already has 15 diverse patterns and FFT-based c5 computation.
Generating external candidates (like generate_ready_candidates) wastes budget.

## Solution: Edit and Probe
1. EDIT EVOLVE-BLOCK to change hyperparameters or add patterns
2. CALL probe_solution (500 intervals, fast) to get c5_bound estimate
3. If c5_bound < 0.375: CALL evaluate_solution (full 59000 steps)
4. If c5_bound >= 0.375: EDIT EVOLVE-BLOCK with a different approach
5. Repeat until budget exhausted or combined_score > 1.0

## Example Hyperparameter Changes
- num_intervals: 400, 600, 800, 1000, 1200 (affects FFT resolution)
- base_learning_rate: 0.001, 0.005, 0.01, 0.02 (affects optimization speed)
- num_steps: 10000, 30000, 59000, 100000 (affects convergence)
- penalty_strength: 10, 30, 60, 100 (affects integral constraint enforcement)

## Example New Patterns
Add to _get_best_initialization():
- Golomb with 5 marks: [0.0, 0.5, 1.0, 1.5, 2.0]
- Bipartite split at a=0.4: high on [0,a), low on [a,2)
- Tri-peak at [0.3, 0.8, 1.6]
- Multi-peak at [0.2, 0.6, 1.2, 1.8]

## Budget Discipline
- Max 2 probe calls per eval
- Never evaluate without probe first
- Use evals only for configs with probe c5_bound < 0.375
