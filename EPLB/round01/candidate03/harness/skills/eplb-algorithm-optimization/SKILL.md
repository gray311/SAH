---
name: eplb-algorithm-optimization
description: Optimization playbook for Expert Parallelism Load Balancers.  Provides concrete algorithm patterns, known pitfalls, and vectorization  techniques specifically for EPLB-style load balancing algorithms. Use when improving rebalance_experts or similar MoE scheduling code.
---

# EPLB Algorithm Optimization Patterns

## Core Functions to Optimize

### balanced_packing(weight, num_packs)
**Goal**: Minimize max-min load variance across packs

**Common mistakes**:
- Per-item greedy with O(n*m) complexity
- Repeated pack_weight array initialization
- Index assignment via Python loops

**Optimized approaches**:

**Pattern A: Sort-and-Cumulative**
1. Sort all items by weight descending (single torch.sort)
2. Assign items cyclically to packs (mod arithmetic)
3. Track pack weights via cumulative sum
4. Use torch.arange and indexing for assignments

**Pattern B: Vectorized Greedy**
1. Sort descending: sorted_items = weight.argsort(descending=True)
2. Compute cumulative weights: cumsum = torch.cumsum(...)
3. For each item, find best pack via: pack = (cumsum % pack_capacity).argmin()
4. Batch assignments with torch.gather/gather_nd

### replicate_experts(weight, num_physical)
**Goal**: Add replica experts to minimize max load

**Pattern**: Sort-by-Weight-Replicate
1. Sort logical experts by weight descending
2. Replicate highest-weight experts first
3. Use 1D indexing: phy2log[redundant_indices] = redundant_expert_ids
4. Avoid per-replica loops; vectorize counts with cumsum

## Memory Optimization Techniques

1. Pre-allocation: Allocate final tensor shapes once, reshape instead of concatenate
2. In-place ops: Use .update_(), .add_() for iterative accumulation
3. View over copy: Use tensor views ([:, None]) instead of copying dims
4. GPU placement: Keep all tensors on same device, avoid .cpu() unless necessary

## Algorithm Complexity Reduction

O(n2) to O(n log n): Replace nested assignment loops with sort + index ops

O(n) to O(1) amortized: Pre-compute statistics (layer means, ranges) outside loops

Avoid: Repeated torch.full_like, new Tensor allocations, Python range loops

## Debug Checklist

- Return types match: int64 for indices, float for weights
- Shapes align: weight.device matches all tensor devices
- No out-of-bounds: indices < num_experts, packs < num_packs
- Deterministic: same input to same output (no random seeding)
- Performance: run locally with small shapes, time the hot path

## When to Use Which Pattern

| Pattern | Best When | Complexity |
|---------|-----------|------------|
| Sort-and-Cumulative | Uniform items, many packs | O(n log n) |
| Vectorized Greedy | Highly skewed weights | O(n log n) |
| Precompute + Greedy | Many layers, independent | O(n + m) |
| In-place Memory | Memory-constrained runs | Same, less alloc |
