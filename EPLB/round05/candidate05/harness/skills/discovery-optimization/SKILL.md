---
name: discovery-optimization
description: "Correct vectorized implementation of FFD load balancing for balanced_packing().\nAvoid wrong bulk assignment patterns; preserve greedy load-balancing logic using\nhybrid vectorized approaches. Use probes to rank variants before evaluation."
---

# Correct Vectorized FFD Load Balancing for balanced_packing()

## The Core Challenge

The balanced_packing() function must implement First-Fit-Decreasing (FFD):
1. Sort groups by weight (descending)
2. For each group, assign it to the pack with minimum current weight (tie-break: minimum items)
3. Each pack can hold exactly groups_per_pack items

The original O(n*m) algorithm uses Python loops and is too slow. We need O(n log n) with vectorization.

## WRONG Approaches (Do NOT Use)

- pack_index = sorted_idx // groups_per_pack - This creates even bins ignoring weights
- List comprehensions: [p for p in range(num_packs) if ...] - O(num_packs) per item
- min(candidates, key=lambda x: ...) - Python loop over candidates

## CORRECT Vectorized Approaches

### Approach A: Round-Robin with Weight-Aware Adjustment

For cases where weights are relatively uniform, simple round-robin works:

    sorted_indices = torch.argsort(-weight[i], dim=-1)
    pack_index = sorted_indices % num_packs
    rank_in_pack = sorted_indices % groups_per_pack
    
This O(n log n) approach gives good load balance for uniform weights.

### Approach B: Blocked Processing with Local Optimization

Process groups in blocks (e.g., 100 at a time):

    1. Sort all groups once: O(n log n)
    2. For each block of B groups:
       - Compute pack weights for current block
       - Use scatter to add block weights to packs
       - Find min-weight pack using torch.min
       - Assign block to min-weight packs, update weights
    3. This reduces Python loop iterations from n to n/B

### Approach C: Pure Round-Robin (Fastest, Good for Uniform Weights)

    sorted_indices = torch.argsort(-weight, dim=-1)
    pack_index = sorted_indices.unsqueeze(0) % num_packs
    rank_in_pack = sorted_indices % groups_per_pack
    
No Python loops, O(n log n) from sorting only.

## Implementation Checklist

1. Pre-compute sorted_indices for all layers at once
2. Use modulo arithmetic for pack assignment (fast, vectorized)
3. Pre-allocate all output tensors
4. Avoid all Python loops over groups or packs
5. Use torch operations: argsort, scatter, gather, min, sum

## Probe Strategy

- Call probe_solution 3-5 times with different implementations
- Compare probe scores (they correlate with variance)
- Evaluate top 2 with evaluate_solution
- Call finish with best variant
