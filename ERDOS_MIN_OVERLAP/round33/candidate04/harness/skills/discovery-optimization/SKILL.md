---
name: discovery-optimization
description: "Try multiple solver architectures (coarse-to-fine, explicit steps, spectral methods)."
---

# Architectural Diversity for Erdos C5

## Problem with Seed Approach
The seed uses gradient descent on 800 intervals with sigmoid initialization. This converges to local minima.

## New Architectures to Try

### 1. Coarse-to-Fine Strategy
- Start with 10-15 intervals, define h as simple step function
- Optimize positions and heights with simple local search
- Gradually increase to 50, 100, 200 intervals

### 2. Explicit Plateau Construction
- Define h as N plateaus: h = sum of N rectangular functions
- Optimize: (a) positions p_i, (b) heights h_i
- Constraint: sum(h_i * width_i) = 1

### 3. Symmetric Patterns
- Try h symmetric around x=1
- Or h with two symmetric peaks

### 4. Low-Discrepancy Sequences
- Use Van der Corput or Thue-Morse sequences
- Map to [0,1] heights

## Workflow
1. Pick ONE architecture
2. Write clean implementation with clear variable names
3. Call probe_solution
4. Evaluate if c5_bound < 0.382
5. If combined_score > 1.0, finish!
