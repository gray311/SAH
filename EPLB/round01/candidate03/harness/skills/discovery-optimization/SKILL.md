---
name: discovery-optimization
description: "Optimize Expert Parallelism Load Balancer algorithms for vLLM MoE models. \nSpecializes in improving load balancing quality while reducing execution time \nthrough algorithmic innovations, vectorization, and memory optimizations."
---

# Expert Parallelism Load Balancer Optimization

## Understanding the Problem

The rebalance_experts function must:
- Take expert weights from MoE layers
- Rearrange experts to balance load across physical replicas
- Return: physical_to_logical_map, logical_to_physical_map, logical_count
- Score combines: load_balance_ratio / execution_time

## Optimization Strategies

### 1. Vectorization over Loops
Replace O(n*m) nested loops with single-pass vectorized ops. Use torch.sort descending, then cumulative sum. Apply with torch.arange for efficient indexing.

### 2. Memory Layout Optimizations  
Pre-allocate arrays once, avoid repeated torch.full_like. Use in-place operations where possible. Consider memory views/slicing instead of copies.

### 3. Algorithmic Improvements
- balanced_packing: Use water-filling heuristic, cumulative weight distribution
- replicate_experts: Sort by weight-descending before replication
- rebalance_experts_hierarchical: Cache per-layer stats, batch computations

### 4. Known Pattern: Sort-and-Greedy for Packing
For balanced_packing:
1. Sort items by weight descending (single pass)
2. Assign greedily to current-min pack
3. Use vectorized cumsum for pack weight tracking

### 5. Known Pattern: Pre-compute Statistics
Compute layer statistics before per-item loops. Use torch.max/min on full layer, not repeated per-item.

### 6. Debugging Invalidity
If validity=0: Check for out-of-bounds indices, dtype mismatches. Test with small shapes mentally before submit. Match return types exactly: int64, float32 as needed.

## Iteration Strategy

1. Keep your BEST working version always available (best_so_far is auto-saved)
2. Make ONE structural change per edit, not multiple at once
3. If score drops: revert to previous iteration, try different direction
4. Track: last good edit mentally - do not rewrite it

## When Budget is Low (<5 evals)

Apply your highest-confidence remaining optimization. Avoid risky changes (no untested algorithms). If already stable, consider finish.
