---
name: discovery-optimization
description: "Multi-shape global polygon search. Generate diverse polygon topologies (rectangle, L-shape, frame, multi-rectangle) at random locations, hill climb edges, and output best. Use 200x200 grid for O(1) fish counting."
---

# Multi-Shape Global Polygon Search

## Strategy: 1. Random Seeds → 2. Shape Variation → 3. Hill Climb → 4. Best Output

### Phase 1: Generate Random Seeds
- Create 20-30 random points uniformly in [0,100000]x[0,100000]
- Each seed becomes a potential polygon center

### Phase 2: Generate Diverse Shapes
For each seed, generate 4-5 candidate polygons:

**Shape A: Random Rectangle**
- Pick 4 random mackerels near the seed
- Compute their bounding box (minX, maxX, minY, maxY)
- Output this rectangle (4 vertices)

**Shape B: L-Shape (Corner Capture)**
- Pick 4 random mackerels near the seed
- Two in top-left, two in bottom-right
- Create L-shape: capture top-left corner, exclude bottom-right
- Output 6 vertices

**Shape C: Frame (Hollow Rectangle)**
- Pick 4 random mackerels near the seed
- Compute their bounding box
- Create inner margin (100-200 units) to exclude sardines on edges
- Output 8 vertices (outer rectangle + inner rectangle)

**Shape D: Multi-Rectangle (Union)**
- Pick 6 random mackerels near the seed
- Form 2-3 overlapping rectangles
- Output union as single polygon (may have up to 12 vertices)

### Phase 3: Hill Climb Refinement
For each candidate polygon:
- For each edge (4-12 edges):
  - Try shifting edge inward by ±5, ±10, ±20, ±30, ±40, ±50 units
  - Use grid lookup to count mackerels/sardines after each shift
  - Keep shift that maximizes (mackerels - sardines)
- Repeat up to 2 refinement rounds

### Phase 4: Random Restarts
- Run Phases 1-3 with 10 different random seed sets
- Track the best polygon across all runs
- Output that single best polygon

## C++ Implementation Notes
- Use a 200x200 grid for O(1) fish counting per cell
- Pre-compute grid at startup
- Rectangle/shape query = sum of grid cells covering the shape
- Total time per evaluation: < 1.5s with efficient grid operations
