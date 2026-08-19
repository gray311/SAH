---
name: circle-packing
description: Hexagonal layer construction for maximizing circle packing sum of radii.
---

# Circle Packing Skill: Hexagonal Layer Construction

## When to use this skill
Use this skill when constructing circle packings for n=26 circles in a unit square. The goal is to maximize the sum of radii, with AlphaEvolve achieving 2.635.

## Why the seed program fails
The seed uses a simple 2-ring construction (1+8+16) with uniform angular spacing. This is suboptimal because:
1. It doesn't exploit hexagonal packing density (~0.9069 vs square packing ~0.785)
2. Equal angular spacing doesn't account for edge effects
3. All circles are initialized with similar radii, but optimal packing needs varying radii
4. The outer ring circles don't interlock optimally with inner rings

## Construction strategy

### Step 1: Hexagonal lattice placement
Instead of concentric rings with equal angles, use a hexagonal grid:
- **Layer 0**: 1 circle at (0.5, 0.5) - the largest
- **Layer 1**: 6 circles around center at distance d1, forming a hexagon
- **Layer 2**: 12 circles in a hexagonal ring around layer 1
- Total: 1 + 6 + 12 = 19 circles (need 7 more)

For 26 circles, consider:
- **Option A**: 1 + 6 + 12 + 7 (irregular outer layer)
- **Option B**: 1 + 8 + 17 with hexagonal spacing in rings
- **Option C**: 4 corner circles + center + 21 surrounding (staggered rows)

### Step 2: Hexagonal ring formulas
For a hexagonal arrangement:
- **6-circle ring**: Centers at (0.5 + r*cos(θ), 0.5 + r*sin(θ)) where θ = k*π/3 for k=0..5
- **12-circle ring**: Two interleaved hexagons, or use θ = k*π/6 with alternating offsets
- **Spacing**: In hexagonal packing, adjacent circles touch when center distance = 2r

### Step 3: Radius computation
After placing centers:
1. For each circle i, compute max radius from borders: r_i = min(x_i, y_i, 1-x_i, 1-y_i)
2. For each pair (i,j), ensure r_i + r_j ≤ distance(i,j)
3. Iteratively scale radii down to satisfy all constraints

### Step 4: Key parameter to optimize
The **inner ring radius** (distance from center to layer 1 centers) is critical:
- Too small: wasted space in the middle
- Too large: outer ring can't fit or circles overlap
- Optimal: inner ring circles touch the center circle AND each other

For hexagonal packing: if center circle has radius R, inner ring circles should have radius R (touching), and the center-to-center distance should be 2R.

### Step 5: Explicit construction example
```python
# Start with center circle at (0.5, 0.5)
# Layer 1 (6 circles): radius = 0.1667, centers at distance 0.3333 from center
# Layer 2 (12 circles): staggered, filling gaps between layer 1
# Layer 3 (7 circles): outer boundary, optimized for square edges
```

## Implementation guidance

1. **Don't clip centers first**: Compute radii from the exact positions, then adjust positions if needed
2. **Try multiple ring configurations**: Test 1+6+12+7, 1+8+17, and 4-corner+center patterns
3. **Vary radii explicitly**: Don't assume all circles in a ring have equal radii
4. **Consider row-based construction**: 7 rows with 1,3,5,7,5,3,1 circles (total 25, add 1 more)
5. **Use the pairwise constraint solver**: The seed's compute_max_radii is correct; focus on better center placement

## Expected improvement
A proper hexagonal construction should achieve 2.4-2.6 sum of radii, compared to the seed's ~0.7.

Key success factors:
- Correct hexagonal geometry (60° angles, not 45° or 90°)
- Optimal ring radius selection
- Proper radius computation from pairwise constraints
- Edge-aware placement for the outermost circles
