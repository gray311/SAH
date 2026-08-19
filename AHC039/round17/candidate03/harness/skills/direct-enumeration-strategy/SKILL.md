---
name: direct-enumeration-strategy
description: Direct point-based enumeration instead of coarse grid. Try random rectangles, coordinate-aligned rectangles, and L-shapes from fish coordinates.
---

# Direct Enumeration Strategy for Axis-Aligned Polygon Optimization

## Why Grid-Based Fails
The previous grid-based approach (200x200 cells) scores 2.48436 — exactly the seed score.
This means no improvement was found. The grid is too coarse (500px cells) and misses
local fish density variations. Sardine awareness via coarse grid doesn't help.

## New Approach: Point-Based Enumeration
Instead of abstracting fish into grid cells, work directly with fish coordinates.

### Phase 1: Coordinate Extraction
- Parse all mackerel and sardine coordinates from input
- Collect unique x and y coordinates from fish positions
- Add boundary points (0 and 100000)

### Phase 2: Candidate Generation
2a. Random Rectangles (Quick Pass)
    - Generate 10-20 random axis-aligned rectangles
    - Use random x, y coordinates in [0, 100000]
    - Keep rectangles with reasonable size (100-1000 px sides)

2b. Coordinate-Aligned Rectangles (Deep Pass)
    - Enumerate rectangles aligned to fish coordinate grid
    - Use sorted unique x and y from fish to create candidate lines
    - Try all combinations of adjacent grid cells as rectangles

2c. L-Shapes
    - Combine two overlapping rectangles
    - L-shapes can capture fish in non-rectangular patterns

### Phase 3: Scoring
- For each candidate polygon, count fish inside using point-in-polygon test
- Score = max(0, mackerels - sardines + 1)

### Phase 4: Selection
- Keep best polygon from all candidates
- Ensure validity: 4-1000 vertices, perimeter ≤400,000, integer coords

### Phase 5: Output
- Output the best valid polygon
