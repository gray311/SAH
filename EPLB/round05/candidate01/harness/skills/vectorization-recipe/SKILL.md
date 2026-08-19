---
name: vectorization-recipe
description: Concrete recipes to convert O(n^2) balanced_packing loops into O(n log n) vectorized torch code. Use these exact patterns.
---

# Vectorization Recipe for balanced_packing()

## Pattern 1: Direct Bulk Assignment
Sort all groups by weight descending: sorted_idx = torch.argsort(-weight, dim=-1)
Assign packs: pack_index = sorted_idx // groups_per_pack
Assign ranks: rank_in_pack = sorted_idx % groups_per_pack
Compute pack weights via scatter-reduce or iterative masking.

## Pattern 2: Blocked Processing
Process groups in blocks of B groups and scatter to packs.

## Key Transformations:
1. Replace for group in indices with argsort + broadcasting
2. Replace list comprehensions with boolean indexing
3. Replace min() with key with scatter_reduce or argsort
4. Replace append loops with pre-allocated tensors
