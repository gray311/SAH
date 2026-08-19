---
name: discovery-optimization
description: "Optimize MoE EPLB algorithm to improve load balance and efficiency. Use vectorized torch operations\nand bounded internal search to beat the O(n^2) baseline. Probe before evaluate, focus on balanced_packing rewrite."
---

# MoE EPLB Optimization Playbook

## Understanding the Baseline
The seed program has O(n^2) behavior in balanced_packing(): nested Python loops, list comprehensions,
and repeated min() calls. This dominates runtime and hurts the efficiency metric.

## Winning Strategy: Vectorization + Bounded Search

### Phase 1: Rewrite balanced_packing with Torch
Replace the entire balanced_packing function with vectorized implementation:
- Pre-allocate pack_index and rank_in_pack as full tensors
- Use weight.argsort(descending=True) to get all items sorted once per layer
- Use scatter_indices and gather for assignments
- Compute pack assignments via mod operations

Example transformation for greedy packing:
OLD (loop): for group in indices: valid = [p for p in range(num_packs)]
NEW (vectorized): pack_assignments = (torch.arange(num_groups) // groups_per_pack) % num_packs

### Phase 2: Add Bounded Local Search
After initial packing, add a refinement pass with explicit iteration bound:
max_refine = min(10, num_packs * groups_per_pack)
for step in range(max_refine):
    # Find heaviest overloaded pack and lightest underloaded pack
    # Swap if improves balance
    # Break early if no improvement in 3 steps

This bounded loop MUST complete within the time limit - keep max_refine small.

### Phase 3: Optimize replicate_experts
Replace the loop with torch operations:
Compute log_weighted = weight / logcnt
Use argmax to find redundant experts in one operation
Accumulate counts using scatter_add

### Phase 4: Iterate Strategically
- Turn 1-3: Generate 3 balanced_packing variants (pure vectorization, vectorization+refine, hybrid)
- Turn 4-6: Probe all variants, identify top 2 by probe score
- Turn 7-8: Evaluate top 2, pick best
- Turn 9+: Generate targeted improvements on winning variant

## Probe Before Evaluate Rule
ALWAYS use probe_solution first (3-5 variants). probe scores are approximate but consistent.
Only call evaluate_solution on the top 2 probes. This saves 75% of your budget.

## Emergency Protocol
When evaluations_left <= 5:
1. Generate all remaining variants (2-3)
2. Probe them all
3. Evaluate only the probe-top-1
4. Call finish immediately after result
