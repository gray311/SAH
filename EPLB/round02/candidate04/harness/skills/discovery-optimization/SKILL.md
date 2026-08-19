---
name: discovery-optimization
description: "Algorithm optimization harness for MoE EPLB tasks. Use probe_solution to cheaply rank algorithm variants, then evaluate winners. Follow structured hypothesis testing: edit \u2192 probe \u2192 compare \u2192 evaluate. Change one algorithmic aspect per iteration. Preserve entry function signature and return types."
---

# MoE EPLB Algorithm Optimization Strategy

## Objective
Maximize combined_score by improving load balancing (lower variance) AND efficiency (faster runtime).

## Method: Hypothesis-Driven Iteration

### Step 1: Analyze Current Algorithm
The seed uses a greedy best-fit algorithm with these characteristics:
- Sorts weights descending per layer
- Places items in pack with fewest items (ties broken by min weight)
- O(n*m) time per layer (python loops)
- Pure logic, no optimization

### Step 2: Form Targeted Hypotheses
Change EXACTLY ONE aspect per iteration:

- **Algorithm variants**: Worst-Fit, Best-Fit, First-Fit, Next-Fit, Best-Fit-Decreasing
- **Search patterns**: Add limited randomization, simulated annealing, tabu list
- **Grouping**: Cluster experts by weight similarity before packing
- **Optimization**: Replace python loops with numpy vectorized operations
- **Weight estimation**: Try different weight metrics or normalization
- **Replication strategy**: Try different logic for choosing which experts to replicate
- **Cache/memoize**: For repeated subproblems

### Step 3: Probe-First Workflow
**CRITICAL**: After every edit:
1. Call `probe_solution` to get approximate scores of your variant
2. If you have 2+ variants, probe them all (probes are free)
3. Pick the best probed variant
4. Call `evaluate_solution` ONCE on the winner

Never call evaluate_solution without probing first. Probes take 10s vs minutes for full evals.

### Step 4: Iterate or Abort
- If probe improves: evaluate, keep the win, plan next edit
- If probe doesn't improve: try a genuinely different hypothesis
- If 3 consecutive fails: revert to best score, start fresh with new direction

### Step 5: Exit
Call `finish` when:
- Evaluation budget exhausted
- Best score unchanged for 3 iterations
- You've tried all reasonable algorithmic directions

## Preserving Contract
- `rebalance_experts` function signature must match exactly
- Return types must be identical (tuple structure unchanged)
- Only modify code between EVOLVE-BLOCK markers
- Keep imports and entry point intact

## Quick Tips
- For bin-packing: try numpy operations to vectorize the inner loops
- For tie-breaking: randomization sometimes beats min-weight determinism
- For efficiency: cache sorted weights, avoid repeated sorts
- For balance: clustering by weight ranges before packing helps
- Track your hypotheses: note which changes helped/harmed
