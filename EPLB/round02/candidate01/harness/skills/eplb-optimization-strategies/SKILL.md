---
name: eplb-optimization-strategies
description: Method playbook for optimizing EPLB load balancing algorithms. Focus on speed and balance tradeoffs.
---

# EPLB Optimization Strategies

## Core Problem
The EPLB algorithm must:
1. Distribute expert load evenly across physical experts
2. Do so efficiently (execution time counts against score)
3. Handle the case where we need to replicate logical experts

## Search Space (what you can change in EVOLVE-BLOCK)

### Packing Strategies
- **Greedy min-load**: Assign each expert to the pack with lowest current load
- **Greedy min-weight**: Assign to pack with lowest total weight (more stable)
- **Hybrid**: Combine load + weight tie-breaking
- **Batch packing**: Process multiple experts together in one operation
- **Vectorized**: Use torch operations instead of Python loops

### Replication Strategies
- **Round-robin**: Assign logical experts sequentially
- **Load-balanced**: Replicate based on weight ratios
- **Heaviest-first**: Replicate heaviest experts first (most impact)
- **Weight-sorted**: Sort by weight then assign replicas

### Advanced Techniques
- **Multi-stage**: Do coarse packing first, then refine
- **Hierarchical**: Group experts at multiple levels
- **Early termination**: Stop if within tolerance of optimal
- **Approximate optimization**: Use greedy with bounded suboptimality

## Metric Interpretation
- **load_variance**: Lower = better balance. Ideal is 0.
- **max_load**: Lower = better worst-case. Lower max = higher balanced.
- **execution_time**: Lower = faster algorithm. Speed matters!
- **combined_score**: Rewards low variance, low max, and low time

## Probing Before Evaluation
1. Call load_balance_probe with 2-3 variants (e.g., greedy, vectorized, hybrid)
2. Compare normalized_score from probe
3. Pick top candidate and call evaluate_solution
4. If score improved, iterate. If worse, try a different strategy.

## Common Algorithm Patterns
```python
# BAD: Python loop over each expert (slow)
for i in range(num_experts):
    for p in range(num_packs):
        if condition:
            assign = p
    
# GOOD: Vectorized torch ops (fast)
ranks = torch.arange(num_packs).repeat_interleave(...)
packs = torch.bincount(...)  # batch operation
```

## Don't Forget
- Preserve function signature in EVOLVE-BLOCK
- Handle edge cases (1 pack, 1 expert)
- Use device=weight.device to avoid CPU transfers
- Test with sampled data first via probe_solution"
