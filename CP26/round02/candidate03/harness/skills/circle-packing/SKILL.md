---
name: circle-packing
description: Task-specific guidance for circle packing optimization in a unit square. Provides geometric construction strategies and heuristics for maximizing the sum of radii of 26 circles.
---

# Circle Packing Construction Strategies

## Objective
Maximize the sum of radii of 26 circles packed in a unit square. The score is `sum_of_radii` (higher is better).

## Key Geometric Principles

### 1. Hexagonal Packing Density
- Densest infinite packing has density π/(2√3) ≈ 0.9069
- Use hexagonal patterns in interior regions where possible
- Offset layers by half the distance between centers

### 2. Layered Construction
- Build circles in concentric layers or shells
- Each layer can have different spacing and radii
- Inner layers can have larger radii

### 3. Edge Effects
- Circles near edges have reduced maximum radius (distance to border)
- Consider asymmetric placements to utilize corners
- Corners can accommodate smaller circles that fill otherwise wasted space

### 4. Radius Optimization
- After placing centers, compute maximum valid radii
- Each circle's radius is limited by:
  - Distance to nearest square edge: min(x, y, 1-x, 1-y)
  - Distance to other circles: d/2 where d is distance to nearest neighbor

## Construction Strategies

### Strategy A: Hexagonal Layering
1. Place largest circle(s) in center
2. Add second layer with hexagonal offset (60° spacing)
3. Continue with larger hexagonal rings
4. Fill remaining space with smaller circles in corners

### Strategy B: Asymmetric Corner Filling
1. Place medium circles in each corner
2. Fill center with larger circle(s)
3. Use remaining space for medium/small circles
4. Exploit asymmetry to reduce wasted space

### Strategy C: Radial Concentric Rings
1. Place central circle with optimal radius
2. Add rings of circles at increasing radii
3. Use hexagonal packing within each ring
4. Adjust ring spacing to maximize radii

### Strategy D: Mixed Size Optimization
1. Use varied radii rather than uniform sizes
2. Larger circles in favorable positions (center)
3. Smaller circles in constrained positions (edges, corners)
4. Optimize each position independently

## Implementation Guidelines

### Center Placement
- Use analytical formulas for optimal positions
- Consider symmetry breaking for edge effects
- Place centers at rational coordinates for reproducibility

### Radius Computation
```python
# For each circle i:
#   r_i = min(
#       distance to nearest edge,
#       min_j(distance(i,j) - r_j) for all j != i
#   )
```

### Iterative Refinement
1. Start with a reasonable construction
2. Compute maximum valid radii
3. If score is low, modify center positions
4. Re-compute radii
5. Repeat with structural changes

## Common Pitfalls

- Assuming uniform radii is optimal
- Ignoring edge effects in square container
- Over-constraining with perfect symmetry
- Not exploiting corner space
- Using too coarse a grid for center positions

## Evaluation Feedback

If score is low (< 1.5):
- Try more aggressive center position changes
- Consider asymmetric layouts
- Use varied radii

If score is moderate (1.5-2.0):
- Refine center positions
- Optimize hexagonal layering
- Better utilize corners

If score is good (2.0-2.5):
- Fine-tune positions
- Try subtle symmetry breaking
- Optimize radii ratios

Target: > 2.635 (AlphaEvolve benchmark)
