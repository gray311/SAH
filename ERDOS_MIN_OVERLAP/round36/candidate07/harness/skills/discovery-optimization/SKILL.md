---
name: discovery-optimization
description: "Sparse peak construction: Manually craft h arrays with 3-4 narrow peaks at strategic positions to minimize overlap at problematic shifts k=1,2,..."
---

# Sparse Peak Strategy for Erdos C5

## Problem Understanding
The C5 bound measures max_k integral h(x)(1-h(x+k)) dx. To minimize this, we need h to have LOW overlap with its shifts. Broad, smooth functions have high overlap at many k. Sparse, well-separated peaks have LOW overlap because:
- At small k, peaks don't overlap with their shifted versions
- At large k, the function value is zero (or near-zero)

## Step 1: Choose Peak Configuration
Select a PEAK COUNT and POSITIONS:
- Count: 2-4 peaks (start with 3)
- Positions: Divide [0,2] into equal segments, place peaks at centers
  - Example: 3 peaks at x = 0.0, 0.667, 1.333 (separation 2/3)
  - Example: 2 peaks at x = 0.0, 1.333 (separation 4/3)
  - Example: 4 peaks at x = 0.0, 0.5, 1.0, 1.5

## Step 2: Craft h Array with EDIT_DIRECT
Manually construct h as an array of N values where:
- N = num_intervals (match seed: 800, or try smaller: 200, 400)
- Each peak is a narrow Gaussian or boxcar: value approx 1.0 at center, decays to approx 0.1 at edges
- Ensure integral constraint: sum(h) * (2.0/N) = 1.0

## Step 3: Verify Constraints
Check:
1. sum(h) * (2.0/N) approx 1.0 (within tolerance 0.99-1.01)
2. All h[i] in [0.0, 1.0]
3. Peaks are narrow (width < 0.2 in x-units)

## Step 4: Evaluate
Call evaluate_solution on the crafted h.
- If combined_score > 1.0: SUCCESS!
- If combined_score <= 1.0: Try different peak count/positions

## Why This Works
The seed's 13+ patterns create high overlap at many k values because they're too broad.
Sparse peaks create LOW overlap at the problematic k values (typically k=1,2,3,...).
This is a STRUCTURED, NOT RANDOM, search.
