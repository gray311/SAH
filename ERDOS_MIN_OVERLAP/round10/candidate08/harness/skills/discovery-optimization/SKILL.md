---
name: discovery-optimization
description: "Diverse initialization search for Erdos optimizer using structured patterns."
---

# Erdos Minimum Overlap - Diverse Initialization Strategy

## Problem
The seed optimizer uses 12 initialization patterns, but they're not diverse enough to escape local minima.

## Solution: Structured Initialization Search

### Step 1: Generate Diverse Initializations
Call construct_structured_init to get 4 mathematically principled initializations:
- bimodal_tight: Two narrow peaks at 0.25 and 0.75
- triangular_3step: Three-level pattern
- periodic_2: Alternating pattern
- golomb_5: Optimal spacing pattern

### Step 2: Optimize Each Separately
For EACH initialization:
1. EDIT to add small random perturbation (noise level 0.1-0.3)
2. OPTIMIZE using the optimizer (full training run)
3. TRACK the best score

### Step 3: Evaluate Best
CALL evaluate_solution on the best optimized initialization

### Step 4: If No Improvement
EDIT to try a different construction from construct_structured_init
Repeat from Step 2

## Why This Works
- construct_structured_init generates INITIALIZATIONS, not just hyperparameters
- Each initialization starts from a DIFFERENT region of the loss landscape
- Optimizing from diverse starting points increases chance of finding global optimum

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- Document which construction achieved best result
