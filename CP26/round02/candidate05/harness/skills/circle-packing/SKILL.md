---
name: circle-packing
description: Guidance for constructing efficient circle packings in a unit square to maximize sum of radii.
---

# Circle Packing Construction Guidance

## Objective
Maximize the sum of radii of 26 circles packed in a unit square. The seed achieves 0.364; target is 2.635 (AlphaEvolve).

## Key Principles

1. **Hexagonal packing is densest**: Arrange circles in staggered rows where each circle fits in the "pockets" of the row below.

2. **Layered construction**: Build from the center outward or in horizontal/vertical layers.

3. **Size variation**: Use different radii to fill gaps; smaller circles fit in remaining spaces.

4. **Edge optimization**: Circles near corners should have smaller radii to stay within bounds.

5. **Symmetry breaking**: Perfect symmetry often isn't optimal; consider asymmetric placements.

## Recommended Construction Strategy

### Option A: Horizontal Layers
- Divide the square into 4-5 horizontal strips
- In each strip, pack circles side-by-side
- Stagger adjacent strips (hexagonal pattern)
- Adjust radii per circle to maximize fit

### Option B: Concentric Rings (Improved)
- Center circle with radius ~0.2-0.25
- Inner ring: 6-8 circles tangent to center
- Outer ring: remaining circles, possibly with varied radii
- Optimize radii using iterative refinement

### Option C: Corner-to-Corner Diagonal
- Place large circles in corners
- Fill remaining space with progressively smaller circles
- Use diagonal symmetry

## Implementation Tips

1. **Start with fixed centers, optimize radii**: Place centers first, then compute maximum non-overlapping radii.

2. **Use distance constraints**: For circles at distance d, radii must satisfy r_i + r_j ≤ d.

3. **Boundary constraints**: Each circle i must have r_i ≤ min(x_i, y_i, 1-x_i, 1-y_i).

4. **Iterative refinement**: After initial placement, try small perturbations to improve packing.

5. **Validate before evaluating**: Ensure all circles are within [0,1]×[0,1] and non-overlapping.

## Common Mistakes to Avoid

- Using uniform radii (wastes space)
- Not considering edge effects
- Overlapping circles due to poor center placement
- Ignoring the boundary constraints
- Using too many circles in one region

## Evaluation Budget

You have 20 evaluations. Use them wisely:
- First 3-5: Test different high-level constructions
- Next 10: Refine promising approaches
- Last 5: Fine-tune and confirm best solution
