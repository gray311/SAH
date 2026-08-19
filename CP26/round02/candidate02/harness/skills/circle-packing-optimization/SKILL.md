---
name: circle-packing-optimization
description: Geometric strategies for maximizing sum of radii in circle packing.
---

# Circle Packing Optimization

## Objective
Maximize the sum of radii of 26 circles packed in a unit square.

## Key Strategies

### 1. Hexagonal Layer Packing
- Densest packing uses hexagonal lattice with 60° angles
- Each layer offset from the previous
- Layer spacing: vertical distance = radius * sqrt(3)
- Start with a central circle, build outward in hexagonal shells

### 2. Multi-Shell Construction
- Inner shell: small circles around a central circle
- Middle shell: medium circles filling gaps
- Outer shell: larger circles near edges
- Use different radii in different shells for better space utilization

### 3. Edge-Optimized Placement
- Circles near edges can be larger (less constrained by neighbors)
- Circles in center must be smaller to avoid overlap
- Place largest circles strategically near corners/edges
- Balance edge utilization with interior packing density

### 4. Iterative Refinement Pattern
- Start with a rough geometric layout
- Compute maximum valid radii for positions
- Adjust positions to increase radii
- Repeat until convergence

### 5. Specific Pattern for n=26
- 1 central circle
- 6 circles in first hexagonal shell (touching center)
- 12 circles in second shell
- 7 circles in third shell (or alternative distribution)
- Total: 1 + 6 + 12 + 7 = 26

## Implementation Guidance

1. Define circle positions explicitly using geometric formulas
2. Use hexagonal coordinates or polar coordinates with offsets
3. Compute radii by:
   - Distance to square boundaries
   - Distance to all other circle centers
   - Take minimum of all constraints
4. Optimize positions to maximize sum of radii
5. Consider symmetry breaking for edge effects

## Example Position Strategy
```
Layer 0: 1 circle at (0.5, 0.5)
Layer 1: 6 circles at distance r0 from center, 60° apart
Layer 2: 12 circles filling gaps between layer 1 circles
Layer 3: 7 circles in remaining space, optimized for edge placement
```

## Performance Target
- AlphaEvolve achieved 2.635
- Focus on hexagonal patterns and edge optimization
