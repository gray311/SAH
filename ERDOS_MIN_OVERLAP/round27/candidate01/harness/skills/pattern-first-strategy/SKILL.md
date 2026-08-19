---
name: pattern-first-strategy
description: Use test_pattern_direct FIRST before any training-based exploration. Screen patterns analytically, then train from winners.
---

# Pattern-First Strategy for Erdos C5

## Core Principle

Don't waste evals on training from random initializations.
The seed has 6 proven pattern types - use test_pattern_direct to score them instantly.

## Step-by-Step

1. FIRST CALL: test_pattern_direct (no args needed)
   - Instantly constructs 6 patterns (analytical c5)
   - Takes ~0.1s, no evaluation budget used

2. SELECT: Pick pattern(s) with c5_bound < 0.37
   - Ideally find one with c5_bound < 0.365
   - Pattern "sym4_01" (4 peaks) is promising for minimizing overlap
   - Pattern "trirect_12" (3 rectangles) may concentrate mass well

3. TRAIN: Call edit_solution to enable single-restart training:
   - Set num_restarts=1 (use one pattern, not 3)
   - Set num_steps=59000 (full training from this good start)
   - Keep other hyperparameters near defaults

4. EVALUATE: Call evaluate_solution once
   - The optimizer should refine the pattern
   - Goal: c5_bound < 0.380923

## If No Success

- Try the same pattern with different width parameters
- Try variations: Sym4 with w=0.08, 0.12, 0.15
- Then consider hyperparameter tuning

## Why This Works

- The 6 patterns are analytical solutions to "how to distribute mass"
- Training from a good pattern can fine-tune it
- Random initializations (seed default) don't know about good patterns
- test_pattern_direct gives you the "map" before you "hike"
