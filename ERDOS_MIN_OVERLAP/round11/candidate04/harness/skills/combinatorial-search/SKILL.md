---
name: combinatorial-search
description: Direct combinatorial search for step function structures, avoiding latent optimization.
---

# Combinatorial Search for Erdos Minimum Overlap

## Core Idea
Generate step functions DIRECTLY as binary/multistep functions with specific structures. This avoids the limitations of gradient descent in latent space.

## Step 1: Generate Candidate Structures
Generate step functions with mathematically motivated structures:
- Bimodal: two peaks at positions (sep, 1-sep) for various sep in [0.2, 0.6]
- Tripeak: three peaks at (a, 0.5, 1-a) for various a
- Periodic: 2-period or higher periodic patterns
- Golomb-inspired: peak placements based on optimal spacing

## Step 2: Screen with Probe
Use probe_solution to quickly compute approximate c5_bound. Accept only candidates with:
- integral(h) ≈ 1.0 (within 5%)
- c5_bound < 0.381 (approximate threshold)

## Step 3: Full Evaluation
Evaluate top 5-10 candidates with evaluate_solution to get exact c5_bound.

## Step 4: Structural Refinement
For promising candidates, explore:
- **Merge**: Combine two adjacent peaks into one
- **Split**: Split a wide peak into narrower ones
- **Shift**: Move peak positions by small deltas (±0.05)
- **Narrow**: Reduce peak width (from 0.15 to 0.08, etc.)
- **Peak count**: Try 1, 2, 3, 4 peaks at different configurations

## Step 5: Iterative Search
Keep track of best c5_bound. For each iteration:
1. Generate new variants based on current best
2. Screen with probe
3. Evaluate promising ones
4. Update best if improved

## Key Heuristics
- Peak positions should be in [0.15, 0.85] to avoid boundary effects
- Two peaks symmetric around 0.5 is most promising
- Peak width should be 0.08-0.15 for good overlap reduction
- Avoid too many peaks (increases overlap)
- Narrower peaks generally give better bounds
