---
name: variable-radius-packing
description: Alternative construction family for circle packing - hexagonal layering with adaptive radii, boundary-aware placement, and staggered rows. Use when simple concentric rings yield low scores.
---

# Variable-Radius Hexagonal Layer Construction

This skill teaches a fundamentally different construction family than simple concentric rings.

## Core Idea

Instead of uniform-radius rings with fixed angular spacing, use:
1. **Hexagonal close-packing pattern** - circles arranged in staggered rows
2. **Adaptive radii** - each circle's radius = min(distance_to_boundary, distance_to_neighbors/2)
3. **Boundary-aware placement** - reduce radii near edges to avoid clipping
4. **Layer-by-layer construction** - build from center outward in hexagonal shells

## Construction Steps

### Step 1: Central Circle
- Place one circle at (0.5, 0.5)
- Radius = min(0.5, 0.5) - 0.05 = 0.45 (constrained by boundary)

### Step 2: First Hexagonal Shell (6 circles)
- Arrange 6 circles around center in hexagonal pattern (60° spacing)
- Centers at distance r_shell from center
- For each circle: radius = min(distance_to_boundary, distance_to_center/2, distance_to_neighbors/2)
- Typical shell radius: 0.15-0.20

### Step 3: Second Hexagonal Shell (12 circles)
- Arrange 12 circles in next hexagonal layer
- Staggered rows: offset every other row by half the average diameter
- Radii shrink toward edges: r_edge = r_nominal * 0.85
- Typical shell radius: 0.35-0.40

### Step 4: Fill Remaining Space
- For n=26, we have: 1 + 6 + 12 = 19 circles
- Place 7 more circles in gaps between existing circles
- These are smaller circles with radii ~0.05-0.10
- Position them in triangular gaps formed by 3 adjacent circles

## Key Parameters

| Parameter | Typical Value | Range |
|-----------|---------------|-------|
| Central radius | 0.40-0.45 | 0.35-0.50 |
| Shell 1 radius | 0.15-0.20 | 0.12-0.25 |
| Shell 2 radius | 0.35-0.40 | 0.30-0.45 |
| Boundary reduction | 0.80-0.90 | 0.75-0.95 |
| Row offset | 0.5 * avg_diameter | 0.4-0.6 |

## Why This Works Better

1. **Higher density**: Hexagonal packing achieves ~0.9069 density vs ~0.785 for square packing
2. **Better edge utilization**: Adaptive radii fit circles into corner spaces
3. **Gap filling**: Smaller circles in triangular gaps add significant radius sum
4. **Reduced overlap**: Distance-based radius computation prevents overlaps

## Implementation Pattern

```python
# Pseudocode structure
centers = []
radii = []

# Central circle
centers.append([0.5, 0.5])
radii.append(min(0.5, 0.5) - 0.05)

# Hexagonal shells
for shell in range(num_shells):
    num_circles = 6 * (shell + 1)
    shell_radius = base_radius + shell * increment
    for i in range(num_circles):
        angle = 2*pi*i / num_circles + shell_offset
        x = 0.5 + shell_radius * cos(angle)
        y = 0.5 + shell_radius * sin(angle)
        r = compute_adaptive_radius(x, y, centers, radii, boundary_factor)
        centers.append([x, y])
        radii.append(r)

# Fill gaps with smaller circles
for gap in gap_positions:
    r = compute_gap_radius(gap, centers, radii)
    centers.append(gap)
    radii.append(r)
```

## When to Use

- When simple concentric rings yield scores < 0.4
- When you need to break out of a local optimum
- When boundary effects dominate the optimization
- When exploring fundamentally different construction families

## Expected Improvement

This construction family typically achieves scores 0.5-0.7 higher than simple ring constructions for n=26, with potential to approach or exceed the AlphaEvolve benchmark of 2.635.
