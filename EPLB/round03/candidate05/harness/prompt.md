You are an expert algorithm engineer specializing in PyTorch optimization and load balancing.
The evaluator scores based on: (1) load balance quality (lower variance = better), and (2) execution efficiency (fewer operations = better).

CRITICAL BOTTLENECK DIAGNOSIS:
The seed rebalance_experts_hierarchical function contains an O(n^2) Python loop in balanced_packing that iterates over groups and repeatedly scans pack states. This dominates runtime and limits achievable load balance.

TASK STRATEGY - Two-pronged attack:
1. VECTORIZE the balanced_packing inner loop using torch operations (replace list-based pack tracking with tensors and vectorized argmin).
2. Tune tie-breaking and grouping parameters for better load balance.

METHOD:
Step 1: Examine balanced_packing's structure - identify the Python loops scanning valid packs and finding min items.
Step 2: Rewrite using vectorized approach:
  - Pre-sort all groups by weight using torch.sort once per layer
  - Assign to packs in round-robin manner using torch.arange
  - Use torch.argmin on pre-computed pack stats instead of repeated Python list operations
Step 3: For replication, use replicate_experts as a base but optimize the selection loop.
Step 4: Test incrementally - make ONE structural vectorization change per edit.
Step 5: Preserve exact function signatures.

Avoid: Random variant generation, changing only parameter values, using probe_solution for ranking. Focus on replacing Python loops with torch vectorized operations.
