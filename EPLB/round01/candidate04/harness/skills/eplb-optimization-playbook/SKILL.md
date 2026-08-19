---
name: eplb-optimization-playbook
description: Playbook for optimizing MoE EPLB expert rearrangement algorithms. Goal - Maximize combined_score by improving load balance AND execution speed. Score components - load balance quality + inverse of runtime penalty.
---

# EPLB Optimization Playbook

## Understanding the Score

The combined_score rewards:
1. Load balance quality: How evenly experts are distributed across physical replicas
2. Execution speed: How fast the algorithm completes (no timeout violations)

## Key Insight

The seed algorithm is O(n^2) due to nested Python loops over expert indices.
This is the PRIMARY bottleneck. Vectorization can achieve O(n) with minimal score loss.

## Transformation Guide

### balanced_packing

Problem: Nested loop assigns groups one-by-one, finding min pack each time (O(n^2)).
Solution: Use torch.argsort to sort globally, then // groups_per_pack for pack assignment.

OLD (slow):
for group in indices[i]:
    pack = min(...) if pack_items[i] < groups_per_pack), key=pack_weights.__getitem__)

NEW (fast):
indices = torch.argsort(weight, dim=-1, descending=True)
pack_index = indices // groups_per_pack
rank_in_pack = indices % groups_per_pack

### replicate_experts

Problem: Repeatedly search for max load logical expert (O(m * (phy-log))).
Solution: Precompute logical expert indices, use vectorized max operations where possible.

## Iteration Strategy

1. Call analyze_algorithm first to get complexity report
2. Replace loops with vectorized ops in balanced_packing (biggest win)
3. Probe 3 to 5 variants with probe_solution to rank by approximate score
4. Evaluate top 2 variants with evaluate_solution
5. Iterate on the best-performing variant

## Common Pitfalls

- Do not introduce Python loops over expert indices
- Ensure tensor dtypes match (int64 for indices, float for weights)
- Test on small inputs first (seed is small: num_logical_experts % num_groups == 0)
- Preserve function signatures exactly
- No device mismatches (all tensors on same device as input)

## Expected Improvements

- Speed: 10x to 100x faster (Python loops to vectorized ops)
- Score: Maintains around 90% to 95% of seed's balance quality
- Combined: 5% to 20% net score increase from speed penalty reduction

## Final Check Before Submit

- No for i in range( loops over expert indices
- All expert assignment uses torch.argsort() or equivalent
- All tensor ops inlined (no generator expressions in loops)
- Code runs under time limit (under 1 second)
- Function signatures unchanged
