---
name: vectorization-strategy
description: Strategy for replacing O(n^2) Python loops with vectorized torch operations in MoE EPLB.
---

# Vectorization Strategy for EPLB

## Pattern 1: Greedy Packing to Scatter
OLD (loop):
  pack_items = [0] * num_packs
  for group in indices:
      valid = [p for p in range(num_packs) if pack_items[p] < groups_per_pack]
      best_pack = min((pack_items[p], p) for p in valid)
      pack_items[best_pack] += 1

NEW (vectorized):
  # Pre-compute all possible assignments
  pack_assignments = (torch.arange(num_groups) // groups_per_pack) % num_packs
  ranks = torch.arange(num_groups) // groups_per_pack
  # Filter to valid packs only
  valid_mask = (ranks.unsqueeze(1) < torch.full((num_groups, num_packs), groups_per_pack - 1, dtype=torch.int64))
  pack_index = pack_assignments[valid_mask]
  rank_in_pack = ranks[valid_mask]

## Pattern 2: Iterative Greedy to Top-K
For replicate_experts, replace loop with:
log_weights = weight / logcnt
redundant_idx = log_weights.argmax(dim=-1)

## Pattern 3: Bounded Local Search
Always bound internal search:
max_iter = min(10, num_packs * groups_per_pack)
for step in range(max_iter):
    # Swap or heuristic operation
    if no_improvement:
        break  # Early exit
# max_iter prevents timeout

## Checklist Before Submit
- Did you replace ALL list comprehensions [x for x in y]?
- Did you replace ALL min/max with torch ops where possible?
- Is any internal search bounded by explicit max_iter?
- Did you use pre-allocated tensors instead of growing lists?
