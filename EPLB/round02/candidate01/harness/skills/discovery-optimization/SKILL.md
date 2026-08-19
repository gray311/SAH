---
name: discovery-optimization
description: "Optimize EPLB load balancing algorithms to improve combined_score (load balance + speed). Use load_balance_probe to iterate variants cheaply before full evaluation."
---

# EPLB Algorithm Optimization Objective: Maximize combined_score balancing load distribution and execution efficiency.
## Workflow 1. **Understand the metrics**: combined_score rewards better load balance (lower variance, lower max_load) AND faster execution time.
2. **Generate variants using load_balance_probe**: This tool computes load metrics and execution time on sampled data cheaply. Call it 3-5 times with different approaches before calling evaluate_solution.
3. **Targeted search strategies**: - **Vectorization**: Replace Python loops with torch operations where possible - **Greedy with lookahead**: Instead of min-load only, consider load + count + weight heuristics - **Batching**: Process multiple groups together instead of one-by-one - **Early termination**: Check if near-optimal packing is achieved - **Replication strategy**: Try different replication orders (heaviest first, or weight-sorted)
4. **Edit the EVOLVE-BLOCK region**: Use SEARCH/REPLACE diffs for small changes or full rewrite for structural changes. Keep the function signature identical.
5. **Evaluate**: Call evaluate_solution on your best probe-ranked variant.
## Probing Strategy - Probe with: greedy_replication, vectorized_pack, hierarchical_variant_1 - Compare: load_variance (lower better), max_load (lower better), execution_time (lower better) - Pick variant with best tradeoff and evaluate it
## Common Pitfalls - Don't just optimize one metric (speed OR balance) - both matter for combined_score - Don't forget to test edge cases (1 pack, 1 expert per node) - Keep operations in GPU/device context to avoid CPU copies - Use torch operations instead of Python loops when possible
