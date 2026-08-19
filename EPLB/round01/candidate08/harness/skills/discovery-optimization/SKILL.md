---
name: discovery-optimization
description: "Iteratively optimize a program's EVOLVE-BLOCK to maximize an automatic evaluator score under a fixed evaluation budget. This skill is optimized for algorithm-speed and heuristic discovery tasks."
---

# Expert Load Balancer Optimization Playbook

## Objective
Maximize combined_score by balancing load distribution quality vs algorithm runtime.

## Key Strategy: Probe-Then-Evaluate
With ~20 evaluations, use probes:
1. For each iteration, create 2-3 variant edits
2. Call probe_solution on each (costs NO eval budget)
3. Pick top-ranked variant, call evaluate_solution
4. This allows exploring 4-6 variants per eval call

## Parameter Tuning Priority
Focus on: thresholds, batch sizes, grouping strategies, iteration bounds.
Try small increments (±5-10%).

## Exploration Loop
When evaluations_left > 5:
1. Generate 3 variant edits (different parameter sets or strategies)
2. Probe all 3 → rank them
3. Full-eval the top 2 → keep best
4. Repeat or converge

## Failure Recovery
- validity=0: Fix error, retry
- Score drop: Revert to best_so_far, try different change category
- Stalled after 3 cycles: Call finish

## Budget Discipline
- Use probes for variant ranking (free!)
- Save evaluate_solution for promising variants only
- With 20 evals, you can afford ~10 good variants + their probes"
