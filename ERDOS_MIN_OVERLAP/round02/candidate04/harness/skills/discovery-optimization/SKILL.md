---
name: discovery-optimization
description: "Structural search for step function configurations in Erdos minimum overlap problem."
---

# Discrete Structural Search for Erdos Minimum Overlap

## Why Discrete Structures?
The seed program's 12 random initialization patterns are continuous Gaussian perturbations.
They explore the neighborhood of random functions, not SPECIFIC step function structures.

The optimum is likely a step function with SPECIFIC breakpoints and levels.
Examples of promising structures:
- Binary with 2 levels and breakpoint at golden ratio position
- Symmetric 3-level patterns
- Alternating binary patterns
- Fibonacci-style divisions

## Method
1. Enumerate structures: Generate 8-12 discrete step functions
   - Vary number of levels (2, 3, 4, maybe 5)
   - Vary breakpoint positions (uniform, golden ratio, symmetric)

2. Brief refinement: For each structure, run 1000 gradient steps

3. Probe ranking: Use probe_solution to score all refined candidates

4. Full evaluation: Evaluate top 2 candidates

## Key Insight
Continuous tweaks around bad starting points will not find the optimum.
You must SEARCH THE STRUCTURAL SPACE explicitly with discrete candidates.
