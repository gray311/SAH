---
name: discovery-optimization
description: "Complete algorithm replacement for MoE EPLB load balancing using vectorized torch operations."
---

# Vectorized Load Balancing Algorithm

## CRITICAL: Complete Replacement Required

The NP-hard load balancing problem CANNOT be solved with incremental tweaks.
You must REPLACE the balanced_packing() and replicate_experts() functions with FULLY
VECTORIZED implementations.

## Phase 1: Vectorized balanced_packing()

OLD PATTERN (AVOID):
- Python loops over groups: for group in indices:
- List comprehensions: valid = [p for p in range(num_packs) if ...]
- min() with lambda for tie-breaking

NEW PATTERN (REQUIRED):
import torch

# Sort indices once per layer
sorted_indices = torch.argsort(-weight[i], dim=-1)  # O(n log n)

# Vectorized pack assignment
pack_items = torch.zeros(num_packs, dtype=torch.long)  # pre-allocate
pack_weights = torch.zeros(num_packs, dtype=torch.float32)  # pre-allocate

# Create item-to-pack mapping in vectorized form
pack_assignment = torch.arange(num_groups) // groups_per_pack  # round-robin base

# Use torch.where or torch.div for refined assignment
pack_idx = (sorted_indices // groups_per_pack) % num_packs  # vectorized modulo
rank_in_pack = sorted_indices % groups_per_pack  # vectorized remainder

Key vectorization tricks:
- torch.argsort() replaces sorting loop
- // and % operators replace manual counting
- Pre-allocate tensors with torch.zeros()
- Use torch.arange() for index generation
- Avoid all Python for loops over items/groups

## Phase 2: Vectorized replicate_experts()

The replication logic can be vectorized by:
1. Computing redundant load per layer
2. Using torch.topk() or argmax() to find heaviest experts
3. Broadcasting assignment across all replicas

Example:
# Find which logical experts need replication
log_load = weight.sum(dim=0)  # sum across layers
redundant = log_load.argsort(descending=True)[:num_redundant]  # top k heaviest

# Assign replicas in vectorized form
logcnt = torch.ones(n, num_logical, dtype=torch.long)
logcnt[redundant] += 1  # vectorized increment

## Phase 3: Testing Strategy

1. Generate ONE vectorized implementation per turn
2. Use probe_solution to quickly check if syntax/shape is correct
3. Never edit both functions in one turn
4. When stuck, try DIFFERENT vectorization pattern (not same pattern with tweaks)

## Phase 4: Final Submission

When budget_left <= 3:
1. Probe both functions final versions
2. If both probe scores improve, evaluate the combined program
3. Call finish immediately
