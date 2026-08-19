---
name: algorithm-opt-strategy
description: Playbook for optimizing MoE EPLB load balancing algorithms. Use probe_solution to cheaply rank variants, then evaluate winners. Change one algorithmic aspect per iteration. Preserve rebalance_experts signature.
---

# Algorithm Optimization for MoE EPLB

## Core Strategy
Maximize combined_score by improving load balancing AND efficiency via structured iteration.

## Iteration Protocol
1. **Edit**: Change ONE algorithmic aspect (bin-packing heuristic, search pattern, grouping, vectorization, etc.)
2. **Probe**: Call probe_solution to score variant cheaply
3. **Compare**: If multiple variants, probe all and pick best
4. **Evaluate**: Call evaluate_solution once on the best probed variant
5. **Iterate**: Keep win, plan next edit; if no improvement, try different direction

## Hypothesis Bank (change one per iteration)
- Worst-Fit bin packing instead of Best-Fit
- Best-Fit-Decreasing (sort before packing)
- Next-Fit or First-Fit heuristics
- Add random tie-breaking for variety
- Cluster experts by weight similarity first
- Vectorize inner loops with numpy
- Cache sorted weights
- Try different weight normalization
- Implement tabu search or simulated annealing
- Prune low-weight experts before balancing

## Critical Rules
- NEVER evaluate without probing first
- Probes take 10s, evaluate takes minutes - use probes to screen
- Budget is 20 evaluations - each counts
- Preserve rebalance_experts signature exactly
- Only modify EVOLVE-BLOCK region
- Revert and try different direction after 3 failed probes

## Exit Criteria
- Budget exhausted: call finish
- 3 consecutive no-improvements: call finish
- No plausible directions left: call finish
