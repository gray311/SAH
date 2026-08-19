---
name: discovery-optimization
description: "Iteratively design and evaluate algorithm variants for NP-hard optimization problems with fixed evaluation budget. Focus on vectorized implementations and efficient data structures."
---

Algorithm Optimization Loop

You have a fixed budget of 20 evaluations. Each evaluation tests ONE complete algorithm variant on FULL data. There is no probing or subsampling - use every evaluation wisely.

Step 1: Analyze the Current Implementation

Read the EVOLVE-BLOCK code. Identify:
- Which operations use Python loops that could be vectorized?
- Are there O(n2) scans that could use heaps or priority queues?
- Is the replication logic suboptimal?
- Can batched operations replace element-wise processing?

Step 2: Generate ONE Improvement Per Evaluation

Never test multiple changes at once. Pick ONE strategy:

Strategy A: Vectorize the greedy packing loop
- Replace the inner loop with torch.sort and scatter operations
- Use batched argmax/argmin instead of min() scans
- Keep the O(n log n) complexity but with much lower constant factors

Strategy B: Improve the replication heuristic
- Instead of (weight/logcnt).max(), use weighted sorting
- Consider both weight and current replication count
- Implement greedy replication of highest-weight experts first

Strategy C: Add hierarchical grouping awareness
- If num_nodes > 1, group experts by node affinity
- Ensure intra-node experts are assigned to nearby physical experts
- Modify the assignment logic to respect node boundaries

Strategy D: Use efficient data structures
- Replace linear scans with heapq for O(log n) min extraction
- Use sorted indices for all layers once, not per-iteration
- Batch pre-computations across all layers

Step 3: Validate and Score

- Ensure the variant preserves the function signature exactly
- Run evaluate_solution to get a real score
- Compare to best_so_far: did load balance improve? Did speed improve?
- If score dropped, analyze why and try a different strategy

Step 4: Iterate or Finish

- Continue improving the best variant if score increased
- If no improvement after 4-5 tries, switch to a fundamentally different approach
- When evals < 5 left, submit your best variant immediately
- Call finish with a clear summary of your winning algorithm
