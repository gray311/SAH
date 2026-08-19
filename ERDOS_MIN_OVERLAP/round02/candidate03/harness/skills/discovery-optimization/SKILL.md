---
name: discovery-optimization
description: "Constructive search for minimum overlap step functions using spectral analysis and combinatorial constructions."
---

# Constructive Search Playbook for Erdos Minimum Overlap

## Why Gradient Descent Fails
The objective has a highly non-convex landscape. Random initializations followed by gradient descent get stuck.

## Pattern Library

### Pattern 1: Grid Uniform
N values: 100, 200, 500, 1000, 2000
Try: even spacing, clustered first half, alternating halves

### Pattern 2: Periodic Alternating
Periods: 1, 2, 4, 8, 16, 32
Formula: h(x) = (1 + cos(2*pi*x/p))^power / 2

### Pattern 3: Strategic Multi-step
Steps: 3, 4, 5, 6
Key positions: 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75

### Pattern 4: Bimodal with Variable Ratios
Mass ratios: 0.25, 0.30, 0.333, 0.35, 0.375, 0.40

## Search Procedure
1. Start with grid uniform (Pattern 1)
2. Use probe_solution to test 5-10 variants
3. When one beats seed, refine its pattern
4. Use analyze_spectrum_properties to guide next parameter variation
5. Never use gradient descent
6. Ensemble top 2-3 candidates

## Target: Beat 0.999641, ideally > 1.0
