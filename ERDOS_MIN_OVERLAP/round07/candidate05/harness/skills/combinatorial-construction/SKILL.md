---
name: combinatorial-construction
description: Generate step functions with integral=1 for C5. Use combinatorial patterns before gradient descent.
---

# C5 Combinatorial Construction

## Why Simple Patterns Work
Seed: 800 intervals, 59k steps - overkill. Simple candidates better.

## Patterns
Single: h=1 on [0,1], integral=1.
Double: h=0.5 on [0,0.5] and [1.5,2].
Concentrated: h~1 on small interval.
Sinusoidal: sin(pi*x)+0.5, clamped, normalized.

## Execution
1. Try patterns with num_intervals=100, num_steps=2000
2. Measure c5_bound
3. Pick best, increase intervals to 200-400
4. Fine-tune only if baseline good

Success: combined_score > 1.0 (c5_bound < 0.380923).
