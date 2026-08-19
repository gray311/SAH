---
name: discovery-optimization
description: "Optimize MoE EPLB algorithm for better load balance AND faster execution.\nUse probe_solution to rapidly rank algorithmic variants before full evaluation.\nFocus on reducing O(n^2) complexity in balanced_packing and exploring efficient constructions."
---

# MoE EPLB Optimization Strategy

## Phase 1: Rapid Exploration with Probes

Always start with probe_solution to test 5-8 different algorithmic approaches cheaply
before spending full evaluations. Look for patterns in what improves the score.

## Phase 2: Algorithmic Improvements to Try

Key bottlenecks in the current algorithm:
- The nested loop in balanced_packing is O(n^2) - replace with O(n log n) or O(n)
- Try using torch.topk or torch.sort with early stopping
- Consider approximations: binning by weight thresholds instead of exact min-fill
- Try greedy assignment with sorting first

Concrete modifications:
- Replace the while loop with: sort groups by weight, assign to pack with lowest current load
- Use vectorized operations: torch.argmin for finding minimum pack weights
- Try torch.bincount or similar for efficient counting

## Phase 3: Validation

1. Pick the top 2-3 probe-scoring variants
2. Run evaluate_solution on each
3. Keep the best, iterate from there

## Phase 4: Speed Optimization

If execution time is the limiter:
- Simplify the algorithm - perfect load balance is NP-hard, aim for good enough fast
- Use approximation algorithms with bounded error
- Reduce memory allocations
- Vectorize loops where possible

## Tool Usage Pattern

Use probe for 5-8 variants, evaluate best 2, then refine. Probe scores are approximate
but RANKINGS are reliable. Use them to guide your search.
