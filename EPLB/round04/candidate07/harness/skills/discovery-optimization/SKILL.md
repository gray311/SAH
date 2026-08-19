---
name: discovery-optimization
description: "Optimize MoE EPLB algorithm by replacing O(n^2) Python loops with O(n log n) vectorized torch operations in balanced_packing(). Use probe-based ranking and bounded internal search."
---

# Vectorized EPLB Optimization

## Step 1: Understand the Bottleneck
The balanced_packing() function uses Python loops over num_groups with O(num_packs) operations per group, making it O(n*m) where n=num_groups, m=num_packs. This is the dominant runtime.

## Step 2: Implement Vectorized Alternatives

### Approach A: Direct Bulk Assignment (O(n log n))
Sort all groups by weight descending: sorted_idx = torch.argsort(-weight, dim=-1)
Assign packs: pack_index = sorted_idx // groups_per_pack
Assign ranks: rank_in_pack = sorted_idx % groups_per_pack
Compute pack weights: scatter-reduce or iterative masking

### Approach B: Blocked Processing (if memory constrained)
Process groups in chunks (e.g., 1000 at a time) and scatter to packs.

## Step 3: Probe and Evaluate
- Generate 3-5 variants using Approach A with different implementations
- Use probe_solution to rank them (approximate score, no eval budget)
- Evaluate top 2 with evaluate_solution

## Step 4: Refine Hierarchical Algorithm
- Use torch.gather, torch.scatter for logical-to-physical mapping
- Pre-allocate output tensors (no resize/append)

## Step 5: Budget Management
- Use probe_solution extensively when budget_left > 5
- When budget_left <= 3, evaluate the single best variant
- Call finish immediately after final evaluation

KEY TRANSFORMATIONS:
1. Replace for group in indices with argsort + broadcasting
2. Replace list comprehensions with boolean indexing
3. Replace min() with key with scatter_reduce or argsort
4. Replace append loops with pre-allocated tensors
