---
name: vectorization-recipe
description: A task-specific playbook for vectorizing the EPLB rebalance algorithm.
---

# Vectorization Recipe for EPLB Algorithm

## Identifying Vectorization Candidates

Look for these patterns:
1. pack_items = [0] * num_packs - replace with torch.full
2. for group in indices: with manual pack selection - replace with sorted assignment
3. [p for p in range(num_packs) if condition] - replace with boolean mask
4. min(pack_items[p] for p in valid) - replace with torch.min(pack_items[valid])

## Common Vectorized Patterns

### Pattern 1: Block Assignment
pack_index = (sorted_indices + torch.arange(num_groups)[:, None]) % num_packs
rank_in_pack = (sorted_indices // groups_per_pack).long()

### Pattern 2: Greedy Vectorized
pack_capacity = torch.full((num_packs,), groups_per_pack-1, dtype=torch.long)
pack_weights = torch.zeros(num_packs, dtype=torch.float32)
valid = pack_capacity > 0
best_pack = torch.argmin(pack_weights[valid])

### Pattern 3: Round-Robin
pack_index = (torch.arange(num_groups) + torch.arange(num_layers)[:, None] * num_groups) % num_packs

## Validation Checklist
- Does output shape match the seed?
- Are all indices within valid ranges?
- Does pack_weights show balanced distribution?

## Tips
- Start with block assignment; it often provides good baseline
- Preserve exact return types (torch.Tensor, not lists)
