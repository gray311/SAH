---
name: discovery-optimization
description: "Transform balanced_packing() from O(n^2) to O(n log n) vectorized torch ops. Use: argsort + integer division for pack/rank assignment. Generate 3-5 variants with probe, evaluate top 2."
---

# EPLB Vectorization Method

## Phase 2: Vectorized Replacement Pattern

Step 1: sorted_idx = torch.argsort(weight, dim=-1, descending=True)
Step 2: pack_idx = sorted_idx // groups_per_pack
Step 3: rank_in_pack = sorted_idx % groups_per_pack
Step 4: Accumulate weights via minimal layer loop

## Phase 3: Validation Strategy
1. Generate 3-5 variants
2. Call probe_solution to rank them
3. Call evaluate_solution on top 2
4. Call finish on best result

## Critical Rules
- NEVER use for loops over groups or packs
- Use integer division for pack assignment
- Use modulus for rank assignment
- Pure PyTorch only
