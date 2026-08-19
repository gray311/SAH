---
name: eplb-optimization-strategy
description: Strategy for improving EPLB load balancer with both quality and efficiency.
---

# EPLB Optimization Strategy

Your goal: minimize load variance AND reduce operations.

Step 1: Use analyze_expert_loads to get baseline metrics.
- If load_variance > 0.5: focus on better packing/replication logic
- If op_count > 1000: focus on vectorization, reduce iterations
- If both high: try hierarchical grouping that reduces both

Step 2: Target the bottleneck:
- Packing issues: try different sorting order (ascending vs descending),
  try balancing by weight vs by count, try round-robin assignment
- Replication issues: try replicating experts with highest weight first,
  try limiting redundant assignments
- Hierarchical issues: try coarser grouping (group by node first),
  try different tie-breaking strategies

Step 3: Iterate with probe_solution to quickly rank variants,
then evaluate the best 1-2 candidates with evaluate_solution.

Important: Keep edits small and targeted. Use SEARCH/REPLACE diffs.
Preserve function signatures. Don't rewrite entire functions.

Common patterns that work:
- Replace list-based loops with torch operations where possible
- Add early-exit when max load is already balanced
- Use pre-sorted indices to avoid repeated sorting
- Cache intermediate results
