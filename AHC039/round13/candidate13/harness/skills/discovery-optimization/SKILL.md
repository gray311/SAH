---
name: discovery-optimization
description: "Shape-space exploration. Enumerate rectangles and simple polygons at grid positions, try multiple sizes, use spatial hashing for fast scoring, local edge refinement, 25+ diverse restarts."
---

# Shape-Space Exploration for Polygon Optimization

## Phase 1: Spatial Indexing
- Read all fish positions into memory
- Build spatial hash: bucket positions into 1000×1000 grid buckets
- Each bucket stores list of fish with coordinates
- For rectangle query: sum buckets that overlap with rectangle, then count exact fish

## Phase 2: Systematic Rectangle Enumeration
- Scan grid: x from 0 to 100000 step 1000, y from 0 to 100000 step 1000
- For each (x,y) position, try rectangle widths: 1000, 2000, 5000, 10000, 20000, 50000
- Similarly for heights: 1000, 2000, 5000, 10000, 20000, 50000
- Compute score = count_mackerel - count_sardine + 1
- Track best rectangle with its score

## Phase 3: Multi-Shape Exploration
- Try L-shapes: union of two rectangles sharing a corner
- Try horizontal bars: very wide, short rectangles
- Try vertical bars: very tall, narrow rectangles
- Try hollow rectangles: outer minus inner (as long as valid)

## Phase 4: Local Refinement
For top 5 candidates:
- For each of the 4 edges:
  * Try perturbations: ±100, ±500, ±1000, ±2000 units
  * Try adding/notching: insert extra vertex on edge
  * Try extending: grow edge outward by ±500, ±1000
- Keep improvement after each perturbation
- Limit refinement rounds to avoid TLE

## Phase 5: Diverse Restarts
- 25+ restarts with:
  * Different random seed for perturbation choices
  * Different starting rectangle dimensions
  * Different scan grid offset (add random 0-1000 to base positions)
- Output single best polygon

## Implementation Notes
- Use spatial hash for O(1) approximate scoring
- Pre-filter rectangles by perimeter constraint (≤400000)
- Coarse-to-fine: quick hash-based count, refine exact count only for promising candidates
- Avoid self-intersection by construction (axis-aligned rectangles and simple unions)
