---
name: circle-packing-strategies
description: Task-specific strategies for circle packing - hexagonal patterns, layered shells, spiral arrangements, and asymmetric clusterings. Use to guide pattern exploration.
---

# Circle Packing Strategies for n=26

## Why This Task is Hard
- Seed score: 0.364; current best: 0.561; target: ~2.6+ (AlphaEvolve)
- 26 circles is small enough to reason about explicitly
- Square container has strong edge effects breaking infinite packing optima

## Pattern 1: Hexagonal Lattice
Densest infinite packing is π/(2√3) ≈ 0.9069 density
- Place centers on triangular grid: angle = 2π * i / (sqrt(3) * ring)
- Rings have 1, 6, 12, 18, 25 circles for perfect hexagon
- For n=26: center + partial rings or irregular hexagon
- Scale ring radius to ~0.557 * ring_layer for optimal spacing

## Pattern 2: Layered Concentric Rings
- Center circle (r ~ 0.5)
- Ring 1: 6-8 circles at radius ~0.4-0.5
- Ring 2: 12-16 circles at radius ~0.6-0.7
- Outer ring: place in corners to use edge space
- Vary radii between rings to fill gaps

## Pattern 3: Spiral Arrangement
- Archimedean spiral: r(θ) = a + b*θ
- Place circles at θ = 2π*i/26 for i=0..25
- Tighten spiral (small b) for dense packing
- Can start off-center to use corners better

## Pattern 4: Asymmetric Clusters
- Break perfect symmetry by placing largest circles off-center
- Use corners of square: (0.1, 0.1), (0.9, 0.1), etc.
- Fill gaps between large corner circles with smaller central circles
- Often outperforms symmetric arrangements due to edge effects

## Implementation Tips
- Always clip centers to [0.01, 0.99] to stay in square
- Use compute_max_radii() to get valid non-overlapping radii
- Return (centers, radii, sum_radii) tuple
- For probe evaluations, keep computation under 10s
- Explicitly specify all 26 positions — no implicit generation
