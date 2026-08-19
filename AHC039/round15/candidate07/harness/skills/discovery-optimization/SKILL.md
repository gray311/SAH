---
name: discovery-optimization
description: "Direct fish-coordinate bounding box expansion with multi-candidate diversity and precise containment checking."
---

# Direct Fish-Coordinate Bounding Box Expansion

## Phase 1: Direct Fish Coordinate Loading
- Parse input to extract mackerel and sardine coordinates directly
- Store in separate vectors for O(1) containment testing
- Do NOT use grid abstraction - lose precision

## Phase 2: Bounding Box Expansion
For each candidate:
- Find bounding box of all mackerels: (min_x, min_y, max_x, max_y)
- Start with minimal enclosing rectangle
- Expand outward in 4 directions (N, S, E, W):
  * Try expansion distances: +10, +20, +50, +100, +200 units
  * After each expansion, count exact mackerels and sardines inside
  * Track score = M - S + 1
  * Continue expanding if score improves or remains positive

## Phase 3: Multi-Candidate Generation
Generate 5-10 diverse candidates per evaluation:
- Seed selection: Random mackerel pair, or random quadrant of coordinate space
- Expansion strategy: uniform, aggressive, or conservative
- Each candidate gets unique random seed for perturbation

## Phase 4: Precise Score Calculation
For each candidate polygon:
- Use coordinate-based containment test: point is inside if x between left/right and y between bottom/top
- Count exact mackerels and sardines inside
- Score = mackerels_in - sardines_in + 1
- Discard if score <= 0

## Phase 5: Polygon Refinement
For top candidates:
- Try small edge perturbations (±5, ±10 units)
- Keep perturbations that improve score
- Repeat until no improvement or time expires

## Phase 6: Output
- Select highest-scoring valid polygon
- Ensure: 4 <= vertices <= 1000, perimeter <= 400000, coords in [0, 100000], axis-aligned
- Output in format: m \n x0 y0 \n x1 y1 \n ...

## Why This Works
- Direct coordinates preserve spatial precision needed to distinguish adjacent mackerel/sardine positions
- Bounding box expansion efficiently explores the solution space
- Multiple candidates ensure escaping local optima
