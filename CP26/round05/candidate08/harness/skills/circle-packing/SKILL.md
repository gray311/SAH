---
name: circle-packing
description: Circle packing construction strategies for maximizing sum of radii in a unit square.
---

# Circle Packing Construction Strategies

## Objective
Maximize the sum of radii of 26 circles packed in a unit square. Target: ~2.635.

## Key Strategies

### 1. Layered Construction
Instead of concentric rings, use layered placement:
- Place circles in horizontal or diagonal layers
- Each layer can have different radii
- Optimize spacing between layers for maximum density

### 2. Hexagonal Packing Regions
- Dense regions should follow hexagonal lattice patterns
- Hexagonal packing achieves ~90.69% density (theoretical maximum)
- In a square, arrange circles in staggered rows
- Row offset = radius of circles in that row

### 3. Variable Radii Strategy
- Don't assume all circles have similar radii
- Smaller circles fill gaps between larger ones
- Use the constraint: r_i + r_j <= distance(centers_i, centers_j)

### 4. Known Optimal Patterns
For n=26, consider:
- A central cluster of small circles
- Larger circles at strategic positions (corners, edges)
- Use symmetry breaking to exploit edge effects

### 5. Iterative Construction with Validation
- Build positions first, compute max radii
- Ensure all circles stay within [0.01, 0.99] bounds
- Validate no overlaps before computing radii

## Implementation Template

```python
# Strategy: Place circles in optimized positions, then compute max radii
# 1. Define positions using geometric patterns (hexagonal, layered, etc.)
# 2. Compute max radius for each circle based on:
#    - Distance to square boundaries
#    - Distance to all other circles (no overlap constraint)
# 3. Sum all radii and return
```

## Specific Heuristics

### Hexagonal Layer Approach
- Layer 0: 1 circle at center
- Layer 1: 6 circles around center (hexagonal)
- Layer 2: 12 circles in outer hexagonal ring
- Layer 3: 7 circles filling remaining space
- Total: 1 + 6 + 12 + 7 = 26 circles

### Corner-Focused Approach
- Place larger circles near corners (more room)
- Use smaller circles in center and edge gaps
- Exploit that corner regions allow larger radii

### Radial Growth with Optimization
- Start with central circle
- Add circles in rings but optimize radii per circle
- Allow different radii per position for gap filling

## Evaluation Tips
- Each evaluation counts - make edits substantial
- Target score improvements of 0.05+ per iteration
- Use full evaluation (not probe) for final confirmation
- When stuck, try completely different construction strategy
