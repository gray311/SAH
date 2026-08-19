---
name: circle-packing
description: Geometric construction strategies for circle packing in a unit square. AUTO-ENACTED - provides explicit construction patterns and positioning heuristics.
---

# Circle Packing Construction Strategies

## Problem Understanding
The task is to construct 26 circles in a unit square to maximize the sum of their radii. The seed achieves only 0.364, far below the AlphaEvolve benchmark of 2.635.

## Key Geometric Principles

### 1. Hexagonal Packing Density
- Densest infinite packing: π/(2√3) ≈ 0.9069
- Hexagonal arrangement: each circle touches 6 neighbors
- Staggered rows: offset every other row by half a diameter

### 2. Square Container Constraints
- Edge effects reduce achievable density
- Circles near boundaries must have smaller radii
- Consider "shells" or "layers" from center outward

### 3. Construction Strategies

#### Strategy A: Layered Hexagonal Packing
- Place large central circle(s)
- Build outward in hexagonal shells
- Each shell adds ~6 circles (minus edge effects)
- Stagger rows to maximize density

#### Strategy B: Greedy Placement with Optimization
- Start with largest feasible circle
- Iteratively place remaining circles in available gaps
- Use local optimization to adjust positions

#### Strategy C: Pattern-Based Construction
- Use known optimal patterns from literature
- Adapt hexagonal grid to square boundaries
- Cluster circles by radius (similar radii form regular patterns)

#### Strategy D: Multi-Shell Concentric Arrangement
- Inner shell: tight hexagonal packing around center
- Middle shell: adapt hexagonal to square edges
- Outer shell: fill remaining space with smaller circles

## Implementation Guidelines

### Positioning Heuristics
1. **Center-based**: Start from (0.5, 0.5) and build outward
2. **Grid-based**: Use triangular/hexagonal grid coordinates
3. **Layer-based**: Assign circles to shells by radius
4. **Gap-filling**: Place circles in local maxima of free space

### Radius Computation
- Each circle's radius is limited by:
  - Distance to square boundaries (x, y, 1-x, 1-y)
  - Distance to neighboring circles (sum of radii ≤ distance)
- Solve as a constrained optimization or iterative refinement

### Validation Checks
- All centers must be in [0, 1] × [0, 1]
- No overlaps: distance(i,j) ≥ r[i] + r[j] for all i ≠ j
- All circles inside square: r[i] ≤ min(x[i], y[i], 1-x[i], 1-y[i])

## Example Construction Pattern (26 circles)

```
Shell 0 (center): 1 circle (large)
Shell 1 (hexagonal): 6 circles
Shell 2: 10-12 circles (adapted to square)
Shell 3: 8-10 circles (edge filling)
Total: ~25-27 circles, adjust to exactly 26
```

## Common Pitfalls to Avoid
- Symmetric but suboptimal arrangements
- Not accounting for edge effects
- Using circular rings instead of hexagonal patterns
- Not iterating radius computation after position changes
- Ignoring that varied radii can pack better than uniform radii

## Search Direction
The executor should:
1. Replace the naive concentric ring layout with hexagonal packing
2. Use layered/shell-based construction
3. Implement iterative radius refinement
4. Consider multi-scale arrangements (large central circles + small edge fillers)
5. Explore asymmetric arrangements that exploit square geometry
