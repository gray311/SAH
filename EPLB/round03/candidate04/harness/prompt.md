You are an expert performance engineer improving the Mixture-of-Expert Expert Parallelism Load Balancer.
The evaluator rewards: (1) lower variance in expert loads across physical experts (load balancing), and (2) fewer total operations (efficiency).

The seed program has a truncated `rebalance_experts_hierarchical` function that needs completion.

Key insight: This is a WEIGHTED BIN PACKING problem. You should:
1. FIRST: Use analyze_weights to understand the weight distribution across experts and layers
2. COMPLETE the truncated rebalance_experts_hierarchical function with a proper hierarchical strategy
3. IMPLEMENT BOUNDED INTERNAL SEARCH: Try 3-5 different packing strategies per evaluation, pick the best, then evaluate
4. Use SEARCH/REPLACE to add complete code blocks, not random edits
5. Preserve function signatures: rebalance_experts_hierarchical(weight, num_physical_experts, num_groups, num_nodes, num_gpus)
6. Return physical_to_logical_map, logical_to_physical_map, logical_count

Packing strategies to implement:
- Greedy: Sort experts by weight descending, assign to lightest pack
- Balanced: Distribute experts evenly across packs, balance by weight
- Hierarchical: Group experts, pack within groups, then across groups
- Randomized: Shuffle then pack (for baseline)

After completing the algorithm, call evaluate_solution to score. If budget_left < 3, finish with the best version.
