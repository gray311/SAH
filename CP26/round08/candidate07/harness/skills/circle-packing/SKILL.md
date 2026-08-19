---
name: circle-packing
description: Geometric strategies for circle packing in a unit square. Use when constructing circle arrangements to maximize sum of radii.
---

# Circle Packing Strategies

## Key Geometric Principles

1. **Hexagonal packing is densest**: In free space, circles pack most densely in a hexagonal lattice with density π/(2√3) ≈ 0.9069.

2. **Layered construction**: Build circles in concentric layers or shells from the center outward.

3. **Edge effects matter**: Circles near boundaries have less room, so smaller radii near edges often improve total sum.

4. **Variable radii help**: Using different radii for different positions can better fill irregular gaps than uniform radii.

5. **Symmetry breaking**: Perfect symmetry may not be optimal; perturbations can improve packing by exploiting edge irregularities.

## Concrete Construction Strategies

### Strategy A: Hexagonal Layering
- Place largest circle at center
- Add second layer with 6 circles in hexagonal pattern around center
- Add third layer with 12 circles
- Continue with layers of 18, 24, etc. circles
- Adjust radii to fit within square boundaries

### Strategy B: Grid-based with optimization
- Start with a regular grid of positions
- Perturb positions slightly to reduce overlaps
- Compute maximum radii for each position
- Iterate: reposition to reduce total overlap, recompute radii

### Strategy C: Edge-aware placement
- Place larger circles away from edges (where they have more room)
- Use smaller circles near boundaries
- Consider corner positions for small circles that can "tuck" into corners

### Strategy D: Clustering by size
- Group circles into clusters of similar radii
- Pack each cluster densely using hexagonal patterns
- Place clusters strategically to minimize inter-cluster gaps

## Implementation Tips

1. **Position first, radii second**: Optimize center positions, then compute maximum radii
2. **Iterative refinement**: Small perturbations of positions can unlock better radius configurations
3. **Boundary handling**: For a unit square, positions near 0 or 1 have reduced radius capacity
4. **Overlap checking**: Two circles at distance d can have radii r1, r2 only if r1 + r2 ≤ d
5. **Boundary constraints**: Each circle at (x, y) has max radius min(x, y, 1-x, 1-y)

## Score Interpretation

The combined_score is sum of all radii. Higher is better. The seed achieves ~0.364, which is very low. AlphaEvolve achieved 2.635. Focus on:
- Getting circles closer to the center (where they can be larger)
- Using more efficient packing patterns
- Allowing variable radii to better fit the square
