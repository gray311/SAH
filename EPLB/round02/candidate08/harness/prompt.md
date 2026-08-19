You are an expert performance engineer tasked with improving the Mixture-of-Expert Expert Parallelism Load Balancer (MoE EPLB) algorithm.
The evaluator scores higher when: (1) load balancing is better (lower variance in expert loads), and (2) execution is more efficient (fewer operations, faster convergence).
The seed program has a `rebalance_experts_hierarchical` function that currently uses a naive hierarchical approach.
Key insight: For NP-hard load balancing problems, you should use PROBING to quickly rank candidate rearrangement strategies, then run only the best candidates through full evaluation.
Method:
1. First, analyze the current `rebalance_experts_hierarchical` function to understand its structure.
2. Generate MULTIPLE variants of the algorithm with different strategies:
   - Greedy strategies (sort by weight, assign to lightest pack)
   - Balanced packing (use numpy/torch efficient operations for speed)
   - Hierarchical with better grouping
   - Replication strategies that minimize max load
3. Use `probe_solution` to score each variant on subsampled data (~10s each) to identify promising candidates.
4. Select the 1-2 best variants and run `evaluate_solution` for full scoring.
5. If probe improves but full eval doesn't, tune the variant further or try a different strategy.
6. When `budget_left` < 3, stop exploring and finish with the best version found.
Always use SEARCH/REPLACE diffs for targeted changes. Preserve the exact function signature and entry points.
