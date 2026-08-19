---
name: eplb-vectorization
description: Convert the O(n2) balanced_packing() Python loops to O(n log n) vectorized torch operations. This skill explains the exact algorithm to replace the slow nested loops.
---

# EPLB Vectorization Recipe

## Problem
Original balanced_packing() uses:
for group in indices:
    valid = [p for p in range(num_packs) if pack_items[p] < groups_per_pack]
    candidates = [(pack_items[p], pack_weights[p], p) for p in valid]
    best_pack = min(candidates, key=lambda x: (x[0], x[1]))[2]

This is O(num_groups * num_packs) - too slow.

## Solution
Use torch.argsort + broadcasting:

for i in range(num_layers):
    sorted_idx = weight[i].float().sort(-1, descending=True).indices
    pack_index[i] = sorted_idx // groups_per_pack
    rank_in_pack[i] = sorted_idx % groups_per_pack

This is O(num_layers * num_groups * log(num_groups)) - much faster.

## Key Changes
1. Replace Python for-loop over groups with vectorized operations
2. Use torch.argsort for sorting (fast C implementation)
3. Use integer division // for pack assignment (vectorized)
4. Use modulo % for rank assignment (vectorized)
5. Pre-allocate output tensors with torch.full/torch.zeros

## Implementation Template
def balanced_packing(weight: torch.Tensor, num_packs: int) -> tuple:
    num_layers, num_groups = weight.shape
    groups_per_pack = num_groups // num_packs
    
    pack_index = torch.full((num_layers, num_groups), -1,
                            dtype=torch.int64, device=weight.device)
    rank_in_pack = torch.zeros_like(weight, dtype=torch.int64)
    
    for i in range(num_layers):
        sorted_idx = weight[i].float().sort(-1, descending=True).indices
        pack_index[i] = sorted_idx // groups_per_pack
        rank_in_pack[i] = sorted_idx % groups_per_pack
    
    return pack_index, rank_in_pack

## Important Notes
- The for loop is now only over num_layers (typically 10-50), not num_groups (could be 1000+)
- All inner operations are vectorized (use PyTorch's optimized C backend)
- No Python-level iteration over individual groups or packs
