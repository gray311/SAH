---
name: circle-packing
description: Specialized skill for optimizing circle packing constructions in a unit square. Use for problems where you construct explicit circle arrangements to maximize sum of radii.
---

# Circle Packing Optimization

## Objective
Maximize the sum of radii of 26 circles placed in a unit square such that:
- All circles are fully contained within the square (0 ≤ x, y ≤ 1 for all circles)
- No two circles overlap (distance between centers ≥ sum of their radii)

## Known Optimal Reference
The AlphaEvolve paper achieved sum_radii = 2.635 for n=26. This is the target to beat.

## Key Geometric Principles

### 1. Hexagonal Packing Density
- Infinite hexagonal packing achieves density π/(2√3) ≈ 0.9069
- This is the theoretical maximum for circle packing
- In finite square containers, edge effects reduce achievable density

### 2. Layer-Based Construction
- Place circles in concentric layers or shells
- Inner layer: small circles around a central point
- Outer layers: progressively larger circles filling remaining space
- Use triangular/hexagonal lattice patterns within layers

### 3. Size Variation Strategy
- Use varied radii to fill gaps efficiently
- Smaller circles can fit in spaces between larger circles
- Don't assume all circles should be similar size

### 4. Edge Utilization
- Place some circles near corners and edges
- Circles near edges can be smaller to fit
- Consider asymmetric arrangements that exploit corner space

### 5. Iterative Refinement Approach
1. Start with a base pattern (e.g., hexagonal lattice subset)
2. Compute maximum valid radii for fixed positions
3. Slightly perturb positions to improve radii
4. Repeat refinement cycles

## Construction Patterns to Explore

### Pattern A: Hexagonal Lattice Subset
- Arrange circles in a hexagonal/triangular lattice
- Select a subset of 26 positions from a larger lattice
- Compute optimal radii for these positions

### Pattern B: Concentric Shells
- Central circle (possibly large)
- First shell: 6 circles around center (hexagonal)
- Second shell: 12 circles
- Third shell: remaining circles
- Adjust shell radii to fit 26 circles

### Pattern C: Corner-Focused
- Place circles in corners (4 corners)
- Place circles along edges
- Fill interior with remaining circles
- Use smaller radii for edge/corner circles

### Pattern D: Mixed Strategy
- Combine hexagonal packing in interior
- Use edge-adapted circles on boundaries
- Allow some irregularity for better fit

## Implementation Guidelines

### Position Selection
```python
# Example: hexagonal lattice positions
# Row i, position j in a triangular grid
x = j * spacing + i * (spacing / 2)
y = i * (spacing * sqrt(3) / 2)
```

### Radius Computation
For fixed positions, compute maximum valid radii:
1. Distance to square boundaries: min(x, y, 1-x, 1-y)
2. Distance to other circles: (dist(i,j) - r[i] - r[j]) ≥ 0
3. Solve the system to find maximum radii

### Refinement Strategy
1. Compute initial radii for a position set
2. Calculate gradient: how does small position change affect sum_radii?
3. Move positions in direction of improvement
4. Re-compute radii after position changes
5. Repeat until convergence or budget exhausted

## Evaluation Tips

- Use `probe_solution` for quick validation of position validity
- Use `evaluate_solution` to get actual sum_radii score
- Track best score across iterations
- Don't exceed evaluation budget (typically 20-30 evaluations)

## Common Pitfalls

1. **Overlapping circles**: Ensure distance between centers ≥ r[i] + r[j]
2. **Circles outside square**: Ensure 0 ≤ x-r, x+r ≤ 1 and 0 ≤ y-r, y+r ≤ 1
3. **Too many evaluations**: Use probe_solution first, evaluate only promising candidates
4. **Local optima**: Try multiple initial patterns, not just one

## Sample Starting Point

Begin with a hexagonal lattice-based arrangement:
- Generate a triangular grid of candidate positions
- Select 26 positions that best utilize the square
- Compute maximum valid radii
- Refine positions iteratively
