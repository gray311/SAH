---
name: discovery-optimization
description: "Optimize MoE EPLB balanced_packing using FFD-preserving vectorization.\nSort once, assign packs via //, ranks via %. Keep num_packs loop small.\nUse probe for fast ranking before full evaluation."
---

# FFD-Preserving Vectorization for balanced_packing()

## Problem
Original code: O(n*m) where n=num_groups, m=num_packs
Uses Python loop over groups, with list comprehensions and min() calls.

## Solution: Sort-once, Assign with Arithmetic
1. Sort all groups descending: sorted_idx = torch.argsort(-weight, dim=-1)
2. Each group's pack = its rank within sorted order // groups_per_pack
3. Each group's rank within pack = sorted_idx % groups_per_pack
4. Pack weights: compute by grouping sorted indices

## Implementation Steps

### Step 1: Sort
sorted_indices = weight[i].float().sort(-1, descending=True).indices for each layer
(or use: sorted_indices = torch.argsort(-weight, dim=-1))

### Step 2: Assign packs and ranks (ONE LINE EACH)
pack_index = sorted_indices // groups_per_pack
rank_in_pack = sorted_indices % groups_per_pack

### Step 3: Compute pack weights (small loop over num_packs only)
pack_weights = torch.zeros(num_packs, device=weight.device)
for p in range(num_packs):
    mask = (flat_pack_idx == p)
    pack_weights[p] = flat_weight[mask].sum()

### Step 4: Flatten and return
Convert pack_index and rank_in_pack back to [num_layers, num_groups] shape

## Key Points
- This preserves FFD: heaviest items go first, distributed round-robin
- Runtime dominated by argsort (O(n log n)) instead of O(n*m)
- num_packs loop is small (typically << num_groups)

## Common Pitfalls
- DO NOT change the sorting criterion (descending by weight)
- DO NOT change groups_per_pack = num_groups // num_packs
- DO NOT use append() or resize() - pre-allocate tensors
- DO NOT forget to return correct shapes

## Workflow
1. Study the original code to understand FFD semantics
2. Apply the pattern above
3. Probe to check load variance (should be similar)
4. Probe to check runtime (should be 10-100x faster)
5. Evaluate best variant
