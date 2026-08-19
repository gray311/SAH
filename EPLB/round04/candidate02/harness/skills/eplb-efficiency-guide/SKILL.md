---
name: eplb-efficiency-guide
description: Guide for optimizing EPLB algorithms for speed and balance. Focus on reducing computational complexity.
---

# EPLB Efficiency Guide

## Complexity Matters: The evaluator rewards faster execution

## Common patterns and their complexities:
for loop over items -> O(n²) -> torch.gather/scatter
for loop over packs -> O(num_packs * n) -> argmin over vector
List min/max with lambda -> O(k) per item -> torch.argmin on tensor

## Rewrite rules for balanced_packing:
1. Pre-sort ALL layers at once with torch.sort
2. Create pack assignments via index arithmetic, not iteration
3. Use scatter to assign ranks in O(n) total time
4. Avoid building pack_items/pack_weights lists; use tensors

## Testing strategy:
- Always call analyze_pack_structure first
- Probe vectorized version before full evaluation
- If score improves, try further vectorization on replicate_experts
