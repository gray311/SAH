---
name: structured-step-functions
description: Generate step functions with mathematical patterns (bipartite, multi-modal, Golomb-inspired).
---

# Structured Step Functions for Erdos C5

## Why Structural Patterns Work

The Erdős C5 problem rewards functions with specific geometric properties.
Random sigmoid curves rarely achieve good bounds because:
- They don't naturally create the separation needed to minimize overlap
- They waste "mass" in regions that don't contribute to the objective

Instead, directly generate step functions with known-good structures.

## Pattern Families

### 1. Bipartite Functions
A single threshold: h(x) = 1 if x < t, else 0.
Simple but often yields decent bounds.

### 2. Multi-Modal Functions
Multiple narrow peaks separated by valleys.
- **Bipolar**: Two peaks (often symmetric or asymmetric)
- **Tripolar**: Three peaks (often symmetric around x=1.0)
- **Four-modal**: Four peaks with controlled spacing

Key insight: Peaks should be separated by at least their own width
to minimize overlap at various shifts k.

### 3. Golomb-Ruler Inspired
Place peaks at positions from a Golomb ruler (no two pairs have the same distance).
This minimizes overlap at many shift values simultaneously.

## Workflow

1. Call step_function_generator with different pattern types
2. Use probe_solution to screen (target c5_bound < 0.382)
3. Evaluate promising candidates
4. Iterate: adjust peak positions, widths, heights

## Never Generate
- Random sigmoid curves (latents passed through sigmoid)
- Hyperparameter-tuned random functions without structural changes
- Functions with overlapping peaks (wastes mass)

## Always Generate
- Step functions with clear peak/valley structure
- Peeks separated by at least 1-2x their width
- Patterns from the families above
