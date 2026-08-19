---
name: discovery-optimization
description: "Optimize MoE EPLB using two-phase vectorization: Phase 1 = minimal FFD with accumulate-based pack tracking, Phase 2 = heap-based O(n log m) if Phase 1 passes. Use probe-based ranking."
---

# Two-Phase EPLB Vectorization

## Phase 1: Minimal FFD with Stateful Tracking

For each layer, sort experts by weight descending. Then greedily pack while tracking state:

```python
# For each layer:
sorted_idx = weight[i].argsort(descending=True)
sorted_weights = weight[i][sorted_idx]

# Track pack state as tensors
pack_items = torch.zeros(num_packs, dtype=torch.int64)
pack_weights = torch.zeros(num_packs, dtype=torch.float32)

# Greedy packing: find best pack for each item
pack_indices = []
for item_idx, item_weight in enumerate(sorted_weights):
    # Find valid packs (not full)
    valid = pack_items < groups_per_pack
    if not valid.any():
        break
    # Candidates: (items, weight) for tie-breaking
    candidates = torch.stack([pack_items[valid], pack_weights[valid]], dim=0)
    best = torch.argmin(candidates, dim=0)  # First index of min (items, then weight)
    best_pack = best[1]
    pack_indices.append(best_pack)
    pack_items[best_pack] += 1
    pack_weights[best_pack] += item_weight

# Map back to original order
pack_index = torch.zeros_like(weight, dtype=torch.int64)
rank_in_pack = torch.zeros_like(weight, dtype=torch.int64)
for j in range(num_layers):
    packed = torch.stack(pack_indices, dim=-1)  # shape: [num_groups]
    pack_index[j] = packed
    rank_in_pack[j] = torch.arange(len(packed), device=weight.device)
```

## Phase 2: Heap-Based Priority Queue (if Phase 1 succeeds)

If Phase 1 passes and we have budget, try a priority-queue based approach for O(n log m) complexity.

## Budget Management

- Generate 3-5 Phase 1 variants with different packing strategies
- Use probe_solution to rank them
- Evaluate top 2
- If no improvement in 2 evaluations, try simpler round-robin assignment
- Finish when budget_left <= 3
