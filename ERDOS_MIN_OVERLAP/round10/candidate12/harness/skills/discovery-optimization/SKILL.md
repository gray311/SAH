---
name: discovery-optimization
description: "Structured initialization search for Erdos optimizer. Instead of sweeping hyperparameters,\ngenerate mathematically principled initializations from known construction strategies,\nrun short optimizations, and iterate with diverse restarts."
---

# Erdos Minimum Overlap - Structured Initialization Strategy

## Why Structure Matters More Than Hyperparameters

The seed optimizer uses 12 initialization patterns but they're all variations on 
basic themes (periodic, triangular, Gaussian). The problem's optimal solution likely 
uses a fundamentally different structure that these patterns don't capture.

## Winning Strategy: Diverse Structural Search

### Phase 1: Generate Diverse Constructions (Use All 30 Evals)
1. Call generate_erdos_constructs to get 5-6 structurally different initializations
   - These are mathematically principled, not random
   - Each has a different "shape" (bimodal, Golomb, finite-field, etc.)

2. For each construction:
   - EDIT the EVOLVE-BLOCK: set num_intervals=400 (coarser for faster iteration)
   - EDIT: num_steps=3000 (short optimization runs)
   - EDIT: num_restarts=1 (single focused optimization per variant)
   - Call probe_solution to check constraint satisfaction quickly
   - If constraint satisfied, call evaluate_solution

3. After testing all constructions, pick the best-scoring one and refine it

### Phase 2: Iterative Refinement
- Once a promising structure is found, incrementally:
  - Increase num_intervals to 800 or 1600 for finer resolution
  - Increase num_steps to 10000-20000 for better convergence
  - Add SMALL perturbations to the initialization (add/subtract small noise)
  - Try slightly different parameter values in the construction

### Phase 3: Structure Mutation
If still stuck:
- Call generate_erdos_constructs again (gets NEW constructions each time)
- Try combining elements from multiple constructions
- Experiment with num_intervals=1600, 2000, 2500 for different resolutions

## Key Principles

1. STRUCTURAL DIVERSITY > Parameter Tweaking
   - A completely different structure beats a finely tuned similar one
   - generate_erdos_constructs provides this diversity

2. Short, Many Iterations > Long, Few
   - 20 restarts × 3000 steps explores more than 1 restart × 60000 steps

3. Use probe_solution to quickly filter constraint violations

4. Each evaluation should test a NEW structural variant
