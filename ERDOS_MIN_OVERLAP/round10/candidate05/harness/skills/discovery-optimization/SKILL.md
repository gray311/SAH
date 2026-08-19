---
name: discovery-optimization
description: "Construction-based search for Erdos minimum overlap. Generate diverse step function patterns directly and screen with probes, rather than relying on gradient optimization."
---

# Construction-Based Strategy for Erdos Minimum Overlap

## Why This Works
The seed program's optimizer is already well-tuned but stuck in local minima.
Direct construction of diverse patterns can escape these minima by exploring fundamentally different function shapes.

## Construction Families to Try

### 1. Binary Step Functions
Create h(x) that takes values 0 or 1 (or scaled versions):
- Two-block: h(x) = 1 for x in [0, a], 0 elsewhere, then normalize
- Three-block: h(x) has two peaks separated by a valley
- Multi-peak: 3-5 peaks with varying widths

Example: 
  x = np.linspace(0, 2, N)
  h = np.where((x >= a1) & (x <= a2), 1.0, 0.0)
  h = h / np.sum(h) * num_intervals  # normalize to integral = 1

### 2. Periodic Patterns
h(x) = |sin(2*pi*x/period)|^alpha or similar

### 3. Golomb-Ruler Inspired
Place "mass" at positions corresponding to optimal spacing:
- For 5 marks: positions ~[0, 0.5, 1.0, 1.5, 2.0] with Gaussian kernels
- Each kernel has width tuned to minimize overlap

### 4. Asymmetric Constructions
- h(x) = 1 for x in [0, 1/3], alpha for x in [1/3, 2/3], beta for x in [2/3, 2]
- Choose alpha, beta so integral = 1

## Execution Strategy

1. **FIRST**: Edit EVOLVE-BLOCK to replace optimizer with DIRECT CONSTRUCTION
   - Remove the ErdosOptimizer class
   - Add construction logic in main or solve() function
   - Generate ONE construction per eval call

2. **SCREEN**: Call probe_solution for each construction to check:
   - integral constraint (should be ~1)
   - approximate c5_bound (should be < 0.39 as initial filter)

3. **EXPLORE**: Try 10-15 different constructions using probe:
   - 3 binary step functions with different peak counts
   - 3 periodic patterns with different periods
   - 3 Golomb-inspired with different mark counts
   - 3 asymmetric constructions
   - 3 random perturbations of good patterns

4. **CONFIRM**: Call evaluate_solution on top 2-3 that pass probe

5. **ITERATE**: If all fail, try:
   - Finer-grained constructions (more peaks, narrower)
   - Different mathematical functions (exponential, triangular)
   - Shift known good constructions

## Key Principle
DIVERSITY over optimization. Try many fundamentally different shapes, not slight variations of one shape.
