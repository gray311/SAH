---
name: discovery-optimization
description: "Line-scanning with hole-filling. Extract rich axis-aligned lines from mackerel data, connect them into orthogonal polygons, optimize locally, run 25+ restarts."
---

# Line-Scanning with Hole-Filling Strategy

## Why This Works

The seed's grid-based approach fails because it discretizes space into 500x500 cells,
losing information about individual points. Mackerels may be scattered such that no single
500x500 cell contains many of them, but multiple sparse lines can still form a large polygon.

## Core Algorithm

### Phase 1: Data Preparation
- Parse mackerel coordinates into two sets: X_coords and Y_coords.
- Parse sardine coordinates for O(1) existence checking.
- Sort X_coords and Y_coords for efficient iteration.

### Phase 2: Line Scanning
- For each X in X_coords:
  - Find all mackerels on this vertical line (same X, varying Y).
  - For each consecutive pair of mackerel Y-coordinates (Y_i, Y_{i+1}):
    - Count mackerels in the segment [Y_i, Y_{i+1}] at this X.
    - Count sardines in the same segment.
    - If (mackerels - sardines) > 0, mark this vertical segment as "rich".

- For each Y in Y_coords:
  - Find all mackerels on this horizontal line (same Y, varying X).
  - For each consecutive pair of mackerel X-coordinates (X_i, X_{i+1}):
    - Count mackerels and sardines in the segment [X_i, X_{i+1}] at this Y.
    - If (mackerels - sardines) > 0, mark this horizontal segment as "rich".

### Phase 3: Polygon Formation
- Build a graph where nodes are rich segments.
- Edges connect segments that are perpendicular and adjacent (share an endpoint).
- Find cycles in this graph (using DFS or Union-Find).
- Each cycle represents a candidate polygon.
- Extract vertices from the cycle and ensure they form a simple orthogonal polygon.

### Phase 4: Validation
- Check: 4 <= vertices <= 1000
- Check: all coordinates in [0, 100000]
- Check: perimeter <= 400000
- Check: no self-intersection (use ray-casting or winding number)
- If invalid, discard and try next candidate.

### Phase 5: Local Optimization
- For each edge of the candidate polygon:
  - Try expanding/shrinking by ±10, ±20, ±30, ±40, ±50.
  - For each variant, count mackerels and sardines inside.
  - Keep the variant with the highest score.
- Repeat 3 refinement rounds.

### Phase 6: Multiple Restarts
- Run 25 restarts with different random thresholds for "richness".
- In each restart, randomly perturb which segments are considered rich.
- Track the best polygon across all restarts.

## Implementation Notes

- Use std::set for O(log N) coordinate lookups.
- Pre-sort coordinates for O(N log N) scanning.
- Total time per evaluation: < 2.0 seconds.
- Use a simple ray-casting algorithm for self-intersection detection.
- Always output valid format: m followed by m vertex pairs.
