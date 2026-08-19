---
name: discovery-optimization
description: "Fast 4-corner search with sardine exclusion. Find mackerel-dense corners of bounding box, construct corner-specific polygons, exclude nearby sardines, perturb edges, run 3 restarts. O(N) counting."
---

# Fast 4-Corner Polygon Optimization

## Strategy: Corner-Focused Search with Sardine Exclusion

### Phase 1: Parse and Compute Bounding Box
- Separate fish into mackerels and sardines
- Compute global mackerel bounding box (minX, maxX, minY, maxY)
- This gives us the overall search region

### Phase 2: 4 Corner Candidates
For each corner (top-left, top-right, bottom-left, bottom-right):
- Extract the corner region (e.g., top-left: [minX, maxX/2] × [minY, maxY/2])
- Check for sardines in a 100-unit buffer around the corner
- If sardines present, shift the corner region inward to exclude them
- Create a rectangle or L-shape polygon for that corner
- Count mackerels and sardines in O(N) time

### Phase 3: Edge Perturbations
For the best corner candidate:
- Try shifting each edge by ±50, ±100, ±150, ±200 units
- Keep shifts that maintain validity and improve score
- Generate 3-5 perturbed variants

### Phase 4: 3 Random Restarts
- Repeat Phases 2-3 with 3 different random perturbations of the initial bounding box
- Each restart picks a random corner to focus on
- Track the best polygon across all restarts

### Phase 5: Output Best
- Output the single best valid polygon (max mackerels - sardines + 1)

## C++ Implementation Notes
- Use std::vector<Point> for mackerels and sardines
- Simple loops for O(N) counting
- No complex data structures (KD-trees, grids)
- Total time: <1.5s with 15 candidates
- Use fast I/O: ios::sync_with_stdio(false); cin.tie(nullptr);
