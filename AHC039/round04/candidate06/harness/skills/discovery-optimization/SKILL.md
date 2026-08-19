---
name: discovery-optimization
description: "Geometric polygon optimization for axis-aligned shapes. Generate candidate polygons, use probe_solution for cheap ranking, then confirm with evaluate_solution. Budget-aware search that avoids wasting evals on poor variants."
---

# Geometric Polygon Optimization for Axis-Aligned Shapes

## Task Summary
Construct an axis-aligned polygon to maximize (mackerels_inside - sardines_inside + 1)
with constraints: vertices ≤ 1000, perimeter ≤ 400,000, coords 0-100,000.

## Critical Rules
- ALL 150 test cases must pass every evaluation. One failure = score 0 for all.
- Use probe_solution extensively: it's ~10x faster than evaluate_solution and FREE.
- Each full eval costs budget; each probe costs nothing. Rank many variants cheaply.
- Simple, robust polygons beat complex fragile ones.

## Strategy: Budget-Aware Geometric Search

### Phase 1: Probing (Free, Fast)
Generate 5-10 candidate polygon shapes and probe each:
- **Shape families to try**:
  1. Large rectangle covering the fish centroid
  2. Multiple smaller rectangles partitioning the space
  3. L-shaped or U-shaped regions targeting fish clusters
  4. Cross/plus shape for central coverage
  5. Triangle or trapezoid variants
  6. Expanding polygon from a seed point

### Phase 2: Selection (Cheap)
Compare probe scores and select top 1-3 candidates by:
- Raw probe score (mackerels - sardines + 1)
- Score per unit perimeter (efficiency metric)
- Conservative score (margin to constraint violations)

### Phase 3: Confirmation (Costly)
Call evaluate_solution for top candidates only:
- Verify full correctness (not just approximate)
- Ensure all 150 test cases pass
- Track the best valid score

### Phase 4: Iteration
If no improvement after 2-3 full evals:
- Try a completely different shape family
- Change construction parameters (center, size, orientation)
- Avoid incremental tweaks that compound errors

## Implementation Notes
- Perimeter = sum of |x_i - x_{i+1}| + |y_i - y_{i+1}| for all edges
- Max perimeter is 400,000; budget ~400 vertices average (since axis-aligned)
- For N=5000, you need significant coverage to beat random
- Centroid-based rectangle: rectangle around fish centroid with padded margin
- Multiple rectangles: cover different density regions

## Red Flags
- Complex nested loops inside main() = TLE risk
- Random-only approaches = high variance, unreliable
- Greedy construction without validation = may violate constraints
- Only one full eval is risky; plan ahead with probing
