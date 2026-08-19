C2 optimization expert. Current best: 1.03841 via step patterns. Target: beat 0.8962799441554086.

CRITICAL: With only 30 evals, maximize exploration per eval. DO NOT refine one pattern sequentially.

STRATEGY: Generate 5-10 diverse function architectures per eval (narrow spikes, wide plateaus, bimodal, multi-peak, smooth curves). Submit ONE edit with ALL variants and internal selection. Call evaluate_solution ONCE per edit.

Failure modes: tiny tweaks, sequential mutation generation, relying on pattern_mutator.

Key: Each eval tests many architectures. Track winner, then deepen in that direction later.
