---
name: vectorization-playbook
description: Playbook for vectorizing MoE EPLB's balanced_packing() to eliminate Python loop overhead and speed up execution while maintaining load balance.
---

# Vectorization Playbook for MoE EPLB

## Problem
The seed's balanced_packing() uses nested Python loops that cause O(n^2) overhead:
for group in indices:
    valid = [p for p in range(num_packs) if pack_items[p] < groups_per_pack]
    best_pack = min(candidates, key=lambda x: (x[0], x[1]))[2]

## Solution: Rewrite with Torch Operations
Replace Python loops with:
1. torch.sort() with descending=True for ordering
2. torch.div() for pack assignment
3. Pre-allocated tensors instead of lists

## Key Principles
- Pre-allocate all output arrays upfront
- Use vectorized assignment with tensor masks
- Avoid Python min() calls - use argmin or arithmetic
- Single pass: sort once, assign in bulk

## Recommended Implementation
Replace balanced_packing with vectorized version:
- Sort each layer by weight descending
- Compute pack indices via integer division
- Compute ranks via modulo
- No nested Python loops

## Testing Strategy
- Use probe_solution to test different vectorization patterns
- Compare scores across patterns
- Evaluate best pattern with full evaluation

## Pattern Selection
- Start with rank-assignment (simplest)
- If no improvement, try weight-scatter
- If still no improvement, try bin-exhaustion
- Never retry same pattern with different parameters
