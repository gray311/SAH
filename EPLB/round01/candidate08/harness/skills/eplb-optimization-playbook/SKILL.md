---
name: eplb-optimization-playbook
description: Method playbook for optimizing Expert Parallelism Load Balancer algorithms. Guides parameter tuning, algorithm completion, and systematic exploration.
---

# EPLB Load Balancer Optimization Playbook

## Core Principle
Maximize combined_score by balancing load distribution quality vs algorithm runtime.

## Phase 1: Diagnose and Complete (If needed)
1. Check if rebalance_experts_hierarchical is complete (ends with proper syntax)
2. If truncated: complete the function with a sensible default strategy
   - Use greedy hierarchical grouping if cut off mid-function
   - Add inverse mapping computation
   - Ensure all branches have return statements

## Phase 2: Parameter Tuning (Primary strategy)
1. Identify tunable numeric parameters: thresholds, group sizes, iteration limits
2. For each parameter, try small increments (±5-15%)
3. Use probe_solution to rank before full evaluation
4. Iterate: after tuning one parameter, move to next

## Phase 3: Structural Variants
1. If parameter tuning stalls, try structural changes
2. Alter grouping strategy (different assignment heuristics)
3. Modify replication logic (different expert selection criteria)

## Phase 4: Convergence
1. When validity=1 and 3 consecutive cycles show no improvement:
   Call finish with summary of approach and best score
2. If validity=0, fix the error and retry
3. If score drops, revert to best_so_far and try different approach

## Tool Usage
- probe_solution: Rank variants cheaply (do this liberally!)
- evaluate_solution: Only for top-ranked variants from probing
- edit_solution: Targeted SEARCH/REPLACE, one hypothesis per edit
- finish: When budget exhausted or converged
"
