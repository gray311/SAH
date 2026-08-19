---
name: discovery-optimization
description: "Coordinate-based rectangle construction. Extract unique coordinates from fish, build fine-grained grid, construct rectangles from positive-score cells, simple hill climbing \u00b11..3, 8-12 restarts."
---

# Coordinate-Based Rectangle Construction Strategy

## Phase 1: Coordinate Extraction and Grid Building
- Read all fish positions (mackerels and sardines)
- Extract unique x coordinates and unique y coordinates
- Sort them to build a coordinate grid
- Each grid cell is a rectangle bounded by consecutive unique coordinates

## Phase 2: Cell Score Computation
For each grid cell rectangle:
- Count mackerels and sardines strictly inside the rectangle
- Compute cell score = M - S
- Store cells with positive score (M > S) in a priority queue

## Phase 3: Rectangle Construction
For each positive-score cell:
- Try to extend in all 4 directions to adjacent positive cells
- Build rectangles of various sizes (2x2, 3x3, 4x4, etc. in terms of cells)
- Convert to polygon vertices (corners of the rectangle)
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0,100000]

## Phase 4: Simple Hill Climbing
For each candidate rectangle:
- For each of the 4 edges (top, bottom, left, right):
  * Try expanding outward by +1, +2, +3 units
  * Check if expansion includes more positive cells
  * Keep expansion that improves M-S count
- Limit to 2 refinement rounds
- Total edge modifications: <= 8 per rectangle

## Phase 5: Multiple Restarts (8-12)
- For each restart:
  * Randomly perturb coordinate selection (±1 to ±5 units)
  * Select 2-3 adjacent positive cells
  * Build rectangle(s) from selected cells
  * Apply simple hill climbing
- Track best polygon across all restarts
- Output single best polygon

## C++ Implementation Notes
- Use std::vector for coordinate lists
- Build grid in O(N log N) time for sorting
- Cell traversal is O(number of positive cells)
- Rectangle construction is O(number of candidate rectangles)
- Total time per evaluation: < 2.0s
- No complex grid structures needed - work directly with fish coordinates
- Use simple perimeter validation (no KVH needed for axis-aligned rectangles)
