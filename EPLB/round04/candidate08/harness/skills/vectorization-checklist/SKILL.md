---
name: vectorization-checklist
description: Checklist for replacing O(n2) Python loops with O(n log n) torch vectorized operations. Follow this EXACTLY when editing balanced_packing() or replicate_experts().
---

# Vectorization Checklist for MoE EPLB

## BEFORE EDITING:
[ ] Have you called vectorize_weight_analysis to understand weight structure?
[ ] Do you know which torch operation to use (sort, gather, scatter)?

## balanced_packing() Transformation:
- [ ] REPLACE: for group in indices: with sorted_indices = torch.argsort(-weight, dim=-1)
- [ ] REPLACE: valid = [p for p in range(num_packs) if pack_items[p] < groups_per_pack] with pre-allocate with torch.full()
- [ ] REPLACE: candidates = [(pack_items[p], pack_weights[p], p) for p in valid] with torch.min(pack_items[valid], dim=0)
- [ ] REPLACE: min(candidates, key=lambda x: ...) with torch.argmin() on vectorized comparison
- [ ] Ensure all loops over groups/items are eliminated
- [ ] Pre-allocate pack_index and rank_in_pack with torch.full() before the loop
- [ ] Use // and % operators instead of manual counters

## replicate_experts() Transformation:
- [ ] Use torch.topk() or argmax() to find heaviest experts
- [ ] Use torch.arange() and broadcasting for replica indices
- [ ] Pre-allocate phy2log, rank, logcnt with correct shapes
- [ ] Use vectorized increment: logcnt[redundant] += 1

## Final Checks:
- [ ] No Python for loops over groups, items, or packs
- [ ] All tensor operations are vectorized (torch.* functions)
- [ ] Function signature unchanged
- [ ] Output shapes match original: balanced_packing returns [num_layers, num_groups], [num_layers, num_groups]
- [ ] replicate_experts returns [num_layers, num_phy], [num_layers, num_phy], [num_layers, num_log]

## TESTING:
1. Probe the new implementation for shape correctness
2. Check if it runs without timeout (~10s budget for probe)
3. Compare probe scores across 2-3 variants
4. Evaluate only the best variant (save 15+ evals)"
