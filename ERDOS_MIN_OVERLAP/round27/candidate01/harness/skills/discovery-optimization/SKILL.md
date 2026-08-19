---
name: discovery-optimization
description: "Analytical pattern screening for Erdos C5. Use test_pattern_direct to instantly construct and score\n6 patterns (bipartite, tri-modal variants, symmetric-4). Each pattern is: latent -> sigmoid -> integral=1 normalize -> c5 via FFT.\nNo training (instant). Call once, pick best c5_bound < 0.37, then evaluate fully."
---

# Analytical Pattern Screening

## Strategy

The seed code has 15 initialization patterns (5-14). Training from them takes 59000 steps.
Instead, use test_pattern_direct to instantly construct and score these patterns.

## Workflow

1. CALL test_pattern_direct (no args needed)
   - Returns 6 patterns with precomputed c5_bound (analytical, no training)
   - Each h has integral=1 guaranteed

2. EXAMINE results:
   - Look for c5_bound < 0.37 (promising)
   - Skip patterns with c5_bound > 0.375 (too bad)

3. CALL evaluate_solution on the TOP 1-2 patterns (best c5_bound)
   - These will train from good initializations
   - With good start, training may find c5_bound < 0.380923

4. If no improvement, try the SAME patterns with different widths:
   - For tri-modal: try widths 0.06, 0.1, 0.15, 0.2
   - For bipartite: try split points 0.4, 0.5, 0.55, 0.6

5. If stuck, try hyperparameter tuning of training (num_steps, lr, penalty)

## Expected Outcome

One of the 6 analytical patterns should have c5_bound < 0.37.
Training from that pattern may yield c5_bound < 0.380923.
