---
name: discovery-optimization
description: "Optimizes expert load balancer algorithms by identifying algorithmic bottlenecks and applying targeted PyTorch vectorization transformations, with evaluation on combined load balance and efficiency metrics."
---

# Vectorized Algorithm Optimization for EPLB

## Core Problem
The balanced_packing function has an O(n^2) Python loop. Replace with vectorized PyTorch operations.

## Step-by-Step Transformation

### Step 1: Analyze current code
- Locate the inner loop in balanced_packing that builds pack_items and pack_weights lists
- Note where min() and list comprehensions are used to find the best pack

### Step 2: Replace with vectorized approach
Strategy A (Block Assignment):
- After sorting groups by weight, assign group i to pack (i mod num_packs) for deterministic balancing
- Use: pack_index = (sorted_indices + torch.arange(num_groups)[:, None]) % num_packs

Strategy B (Greedy Vectorized):
- Pre-compute pack capacities using torch.full
- Use torch.argmin and torch.gather for batched pack selection

### Step 3: Key optimizations
- Replace [p for p in range(num_packs) if pack_items[p] < groups_per_pack] with boolean mask
- Replace min(pack_items[p] for p in valid) with torch.min(pack_items[valid])
- Pre-allocate all output tensors once

### Step 4: Validation
- Ensure vectorized version produces IDENTICAL outputs than the seed
- Check that execution time is reduced

### Step 5: Iterative refinement
- If block assignment is too coarse, try block-cyclic
- Experiment with tie-breaking strategies

## Tools to Use
- edit_solution: Submit SEARCH/REPLACE diffs focusing on balanced_packing function
- evaluate_solution: Score each variant
- Avoid probe_solution

## Success Criteria
- Vectorize at least one inner loop
- Maintain or improve load balance quality
- Pass validity checks
