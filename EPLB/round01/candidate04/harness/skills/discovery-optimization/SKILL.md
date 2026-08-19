---
name: discovery-optimization
description: "Optimize MoE EPLB expert rearrangement algorithms for vLLM. Maximize combined_score by improving both load balancing quality and execution speed through vectorized PyTorch operations."
---

# MoE EPLB Algorithm Optimization

## Core Strategy: Vectorize Everything

The seed implementation uses slow Python nested loops. Replace with PyTorch vectorized ops:
- balanced_packing: Use torch.argsort + torch.cumsum or scatter to pack in O(n) time
- replicate_experts: Use torch.argsort on normalized weights + torch.cumsum for rankings

## Concrete Transformation Steps

1. For balanced_packing: Replace the nested for-loop with:
   Sort by weight descending, then assign packs using bucketization.
   Target: groups_per_pack items per pack, minimizing pack weight variance.

2. For replicate_experts: Use torch.argsort on weight/logcnt to find max-load experts.

## Use Probe Heavily

- Probe budget: around 30 cheap evaluations (subsampled, fast scoring)
- Use probes to rank 5 to 10 vectorized variants before spending full evaluations
- Only call evaluate_solution on top 2 to 3 variants that are syntactically valid, show promising probe scores, and have clean vectorized implementations

## Checklist Before Evaluation

- No Python for-loops over expert indices (use vectorized ops)
- All tensor operations use torch functions (argsort, scatter, cumsum)
- Memory layout optimized (contiguous tensors, proper dtype)
- Code runs in under 1 second on a single GPU
- Function signatures unchanged from seed

## Typical Improvements

- Speed: O(n^2) to O(n) via vectorization
- Score: Better load balance due to more exhaustive search in limited time

Remember: The evaluator rewards BOTH load balance AND speed. A fast algorithm that achieves good (not perfect) balance scores highest.
