---
name: discovery-optimization
description: "Beam search over polygon vertices. Start with 3-5 diverse polygons, explore vertex-level mutations (\u00b110, \u00b120, \u00b150 shifts, add/remove vertices at fish locations), use ray-casting for exact scoring, beam search (3-5 branches \u00d7 3-4 iterations), output best valid polygon."
---

# Beam Search for Axis-Aligned Polygon Optimization

## Overview
This strategy uses beam search (3-5 parallel branches) with vertex-level mutations to optimize polygon shape for fish capture.

## Phase 1: Initial Polygon Generation
Create 3-5 diverse initial polygons:
1. Large bounding box: cover entire [0,100000]×[0,100000] range
2. Center rectangle: cover central region
3. Top-left rectangle
4. Bottom-right rectangle  
5. Centered rectangle around coordinate mean

For each, verify: 4-1000 vertices, integer coords, perimeter constraint, no self-intersection.

## Phase 2: Beam Search Iteration (3-4 rounds)
For each polygon in the beam (keep top 5 across all parents):

Generate variants through:

A. Edge Shifts (primary):
   - For each edge, compute normal vector pointing outward
   - Try shifts: +10, +20, +50 units
   - For inward shifts: -10, -20, -50 (to exclude sardines)
   - Create new polygon with shifted vertices
   - Validate constraint compliance

B. Vertex Operations:
   - Add vertex: at midpoint of long edges, or at mackerel positions
   - Remove vertex: where three consecutive vertices form ~180° angle
   - Merge collinear vertices

C. Region-based:
   - If perimeter < 400,000, try expanding bounding area
   - If many sardines inside, contract edges toward center

Score each variant using exact ray-casting point-in-polygon test:
- For each of 5000 mackerels: count if inside polygon
- For each of 5000 sardines: count if inside polygon  
- Score = max(0, mackerels - sardines + 1)

Keep top 5 variants for next iteration.

## Phase 3: Final Validation
- Check 4 <= m <= 1000 vertices
- All coordinates: 0 <= x,y <= 100000
- Perimeter <= 400,000
- No self-intersection (test all non-adjacent edge pairs)
- All vertices have distinct coordinates

## Phase 4: Output
Return single best valid polygon (m vertices followed by coordinates)
