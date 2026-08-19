---
name: diverse-initialization-search
description: Use construct_structured_init to generate diverse initializations, optimize each separately, and track the best.
---

# Diverse Initialization Search for Erdos Optimizer

## Overview
The key to improving the Erdos bound is not hyperparameter tuning, but generating DIVERSE initializations
that start from different regions of the loss landscape.

## Step-by-Step Procedure

### 1. Generate Initializations
Call construct_structured_init ONCE to get 4 initializations:
- bimodal_tight: Two peaks at 0.25 and 0.75 (known good for this problem)
- triangular_3step: Three-level pattern
- periodic_2: Asymmetric periodic pattern
- golomb_5: Optimal spacing from Golomb ruler

### 2. Optimize Each Initialization
For EACH of the 4 initializations:

a) EDIT the EVOLVE-BLOCK to:
   - Replace the initialization code with YOUR specific initialization
   - Add small random noise (scale 0.1-0.3) to break symmetry
   - Keep all optimizer hyperparameters the same

b) OPTIMIZE: Run the optimizer to completion (59000 steps)

c) TRACK: Record the final c5_bound

### 3. Evaluate the Best
Pick the initialization with the LOWEST c5_bound and call evaluate_solution.

### 4. If No Improvement
EDIT to try a DIFFERENT construction type from construct_structured_init
Return to Step 2

## Key Principles
- DIVERSITY > TUNING: Different initializations > better hyperparameters
- OPTIMIZE EACH: Full optimization for each initialization
- TRACK EVERYTHING: Record scores for all 4 initializations
- ITERATE ON CONSTRUCTION: If one construction fails, try another

## Expected Outcome
- Finding an initialization that leads to a c5_bound < 0.380923
- This requires trying ALL 4 constructions before giving up
