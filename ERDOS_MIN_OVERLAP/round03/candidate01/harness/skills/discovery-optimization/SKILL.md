---
name: discovery-optimization
description: "Discrete structure search for Erd\u0151s optimization. Generates sparse step-function candidates with clean transitions, avoiding the failure mode of continuous gradient descent that gets stuck."
---

# Discrete Structure Search for Erdős Minimum Overlap

## Why Discrete Structures Beat Continuous Optimization

The current best bound C5 ≤ 0.380923 comes from a STRUCTURED construction. Continuous gradient descent from random/structured seeds gets STUCK.

## New Strategy: Enumerate Sparse Step Functions

### Step 1: Generate Discrete Candidates (probe_discrete_structures)
Generate 10-15 SPARSE step functions:
- 3-step functions: Two thresholds dividing [0,2] into 3 regions
- 4-step functions: Three thresholds, 4 regions
- 5-step functions: Four thresholds, 5 regions

Each must satisfy ∫h = 1 exactly.

### Step 2: Quick Screening
Use probe_solution on each discrete candidate (instant eval).
Rank by c5_bound.

### Step 3: Optional Refinement
For top 2-3 structures, add short gradient descent (1000-2000 steps max).
Often unnecessary - the discrete structure is already optimal.

### Example 3-Step Construction
x ∈ [0, a) → h = h1
x ∈ [a, b) → h = h2
x ∈ [b, 2] → h = h3
Constraint: h1*a + h2*(b-a) + h3*(2-b) = 1

### Key Insight
Erdős problems have COMBINATORIAL optima. Systematically enumerate structures,
don't blindly optimize. The best C5 bound likely comes from a 3-6 step function
with carefully chosen thresholds, not a smooth sigmoidal curve.
