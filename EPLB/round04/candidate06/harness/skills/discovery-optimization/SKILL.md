---
name: discovery-optimization
description: "Iteratively optimize MoE EPLB load balancing. The seed uses O(n\u00b2) Python loops; your job is vectorized rewrite using torch ops."
---

# Vectorized Rewrite for MoE EPLB

## THE PROBLEM
The seed's balanced_packing() uses Python loops that assign experts pack-by-pack. This is O(n²) per layer.

## THE SOLUTION: Vectorized FFD
1. **ONE-STEP SORT**: Use torch.argsort to sort ALL experts across ALL layers at once:
   ```python
   sidx = weight.float().argsort(-1, descending=True).long()
   ```
2. **PACK ASSIGNMENT**: Each expert at position (layer, expert_idx) goes to pack = expert_idx // groups_per_pack:
   ```python
   pack_idx = sidx[:, :, None] // groups_per_pack  # broadcasting
   ```
3. **RANK COMPUTATION**: Rank within pack is expert_idx % groups_per_pack:
   ```python
   rank_in_pack = sidx[:, :, None] % groups_per_pack
   ```

## IMPLEMENTATION TEMPLATE
Replace balanced_packing entirely:
```python
def balanced_packing(weight, num_packs):
    num_layers, num_groups = weight.shape
    assert num_groups % num_packs == 0
    groups_per_pack = num_groups // num_packs
    
    if groups_per_pack == 1:
        pack_index = torch.arange(num_groups, dtype=torch.int64, device=weight.device).expand(num_layers, -1)
        rank_in_pack = torch.zeros_like(weight, dtype=torch.int64)
        return pack_index, rank_in_pack
    
    # Vectorized FFD: sort all experts descending, assign by position
    sidx = weight[:, :, None].float().argsort(-1, descending=True).int()  # [L, G, 1]
    pack_index = sidx[:, :, 0] // groups_per_pack  # [L, G]
    rank_in_pack = sidx[:, :, 0] % groups_per_pack  # [L, G]
    
    return pack_index, rank_in_pack
```

## TESTING STRATEGY
1. Generate this vectorized version
2. Call probe_solution immediately (it's cheap)
3. If score improves, call evaluate_solution
4. If not, call finish

## DO NOT
- Don't add Python loops
- Don't try "greedy" or "local search" - vectorization IS the optimization
- Don't modify replicate_experts unless explicitly asked

## FINISH
When you have the vectorized version, call evaluate_solution and finish.
