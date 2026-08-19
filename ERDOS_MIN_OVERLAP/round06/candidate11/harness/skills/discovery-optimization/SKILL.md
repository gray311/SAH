---
name: discovery-optimization
description: "Piecewise constant construction harness for C\u2085 bound. Generates explicit step functions with few breakpoints, ensuring validity (\u222bh=1, h\u2208[0,1]). Focus on constructive discrete approaches over gradient descent."
---

# C₅ Bound: Piecewise Constant Construction Strategy

## Why Gradient Descent Fails

The seed program uses Adam optimizer on 800 continuous points initialized from sigmoid waveforms. This is fundamentally mismatched:
- The optimal solution is likely a simple piecewise constant function
- 800 points create a flat, featureless landscape
- Gradient initialization doesn't discover good breakpoint structures

## Proven Construction Strategy

### Step 1: Generate Candidates with FEW Breakpoints

Use `construct_candidates` to get 5-10 explicit piecewise constant functions:
- Single symmetric bump: mass concentrated in [0.5, 1.5]
- Two symmetric bumps: mass in [0.25, 0.75] and [1.25, 1.75]
- Center-concentrated: taller middle section
- Left-heavy: asymmetric mass distribution
- Threshold with decay: simple piecewise constant

Each candidate is guaranteed:
- Values in [0,1]
- Integral exactly 1 over [0,2]
- Only 2-6 breakpoints (vs 800 parameters)

### Step 2: Evaluate and Select

For each candidate from construct_candidates:
1. Call evaluate_solution to get combined_score
2. Identify the top 2-3 candidates with best scores
3. Analyze their structures

### Step 3: Refine Breakpoint Structures

Once you have a winning structure:
1. Reduce num_intervals to 100-200 (coarser is better for structure discovery)
2. Write a COMPLETE REWRITE with:
   - Same breakpoint structure (2-6 breakpoints)
   - Just 5-10 parameters (breakpoint positions, heights)
   - Use a simple optimizer (even grid search over breakpoints)
3. Expand num_intervals to 400-800 for final refinement

### Step 4: Try Variations

Once you find a good pattern, try variations:
- Shift the bumps left/right
- Add more bumps
- Change the relative heights
- Try asymmetric distributions

## Execution Plan

1. Call construct_candidates (1 eval or 0 if embedded)
2. Evaluate top 3 candidates
3. Pick winner, rewrite with its structure (coarse intervals)
4. Refine structure for 3-5 iterations
5. Final refinement with 400-800 intervals

## Key Patterns to Look For

- **Symmetric constructions** often work well
- **Concentrated mass** (less spread out) tends to reduce overlap
- **Few breakpoints** = easier to optimize, less prone to local minima

## Important

- **Construct explicit structures first** - don't trust gradient initialization
- **Start coarse** (50-100 intervals), refine later
- **Breakpoint optimization** is easier than 800-point optimization
- **Your goal is >1.0 combined_score** - that's a record!
