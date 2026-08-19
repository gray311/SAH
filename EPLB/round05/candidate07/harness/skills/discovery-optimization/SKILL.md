---
name: discovery-optimization
description: "Optimize MoE EPLB balanced_packing() by implementing FFD with vectorized tensor operations: pre-sort once, use vectorized min for pack selection, scatter-reduce for pack weight updates. Focus on speedup while preserving FFD correctness."
---

# Vectorized FFD for MoE EPLB Optimization

## The Correct Algorithm

The balanced_packing() function must implement First-Fit-Decreasing (FFD):
- Sort groups by weight descending
- For each group, find pack with FEWEST items (tie-break: least weight)
- Assign and update pack state

This is O(n*m) where n=groups, m=packs. We want O(n log n).

## Correct Vectorization Strategy

### Step 1: Pre-sort all layers
```python
for i in range(num_layers):
    sorted_indices[i] = torch.argsort(-weight[i], dim=-1)  # O(n log n) per layer
```

### Step 2: Vectorized pack selection
Instead of Python loop `for group in indices`, vectorize:
- Create validity mask: `valid = pack_items < groups_per_pack`
- Build candidate tensors: `candidates = [pack_items[valid], pack_weights[valid], valid]`
- Find best: `best = min(candidates[0] + candidates[1]*eps + candidates[2], axis=0)`
- This still has O(n) candidates but uses vectorized ops

### Step 3: Atomic updates
Use scatter operations to update pack_items and pack_weights in bulk.

## Key Transformations

1. Sort ONCE per layer with argsort (O(n log n))
2. Use vectorized min/where instead of Python loop over packs
3. Pre-allocate output tensors
4. Avoid list comprehensions; use boolean indexing

## Probe Strategy

- Generate 3-5 variants: different ways to vectorize the pack selection
- Use probe_solution to rank them (10s each)
- Evaluate top 2 with evaluate_solution
- When budget_left < 5, call finish with best variant
