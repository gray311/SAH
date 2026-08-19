---
name: discovery-optimization
description: "Optimize MoE EPLB algorithms for better load balance and execution efficiency. Use analyze_eplb_inputs to understand input structure, then systematically improve the balanced_packing, replicate_experts, or rebalance_experts_hierarchical functions."
---

# MoE EPLB Optimization Strategy

## Objective
Maximize the combined score that balances load quality and algorithm efficiency. The evaluator rewards:
- Lower variance in expert load across GPUs
- Faster execution time of the rebalancing algorithm

## Step 1: Analyze Inputs
Call `analyze_eplb_inputs()` ONCE to inspect the weight matrix dimensions and value distributions. Typical inputs are [num_moe_layers, num_logical_experts] tensors, often with 16-64 experts per group.

## Step 2: Identify Bottlenecks
Look for:
- O(n²) loops in `balanced_packing()`: the inner loop checking all packs for every group
- Redundant tensor allocations: creating full-sized tensors before use
- Inefficient tie-breaking: scanning all packs instead of tracking minimums
- Memory access patterns: CPU vs GPU operations, transpose operations

## Step 3: Targeted Improvements
Try ONE of these per edit:
1. **Vectorize the pack assignment**: Replace inner loops with `torch.argmin()` or `torch.sort()`
2. **Add early termination**: If all packs have equal items, stop assigning
3. **Optimize tie-breaking**: Track min-weight packs in a priority structure
4. **Reduce tensor size**: Create tensors only when needed, reuse where possible
5. **Better initialization**: Start with equal-weight packs instead of -1

## Step 4: Verify
- Use `probe_solution()` to test multiple variants quickly (separate budget)
- Only run `evaluate_solution()` on your best 1-2 variants
- Never rewrite the whole EVOLVE-BLOCK for small changes — use SEARCH/REPLACE

## Key insight
The current seed algorithm is O(L × E²) where L=layers, E=experts. With 20 evals, you need O(1) edits that each provide measurable gains. Small loop optimizations compound.

## Entry function
Preserve the exact entry function the evaluator calls. Only modify code inside # EVOLVE-BLOCK-START and # EVOLVE-BLOCK-END.

## Tool reminders
- `edit_solution`: Use SEARCH/REPLACE for targeted edits. Full rewrites only for structural changes.
- `evaluate_solution`: Score returns combined_score (higher=better), validity, error, best_so_far, evaluations_left.
- `probe_solution`: Fast (~10s) approximate score on subsampled data. Does NOT use evaluation budget.
- `analyze_eplb_inputs`: Call ONCE at start. Returns matrix dimensions and stats. Does NOT consume evaluation budget.
- `finish`: Call when done or budget exhausted.

Remember: Perfect balancing is NP-hard. Good enough that's fast is often better than perfect that's slow.
