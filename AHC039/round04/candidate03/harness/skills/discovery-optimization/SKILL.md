---
name: discovery-optimization
description: "Construct a polygon solution for fish-capture maximization. Focus on complete, valid code that outputs m vertices. Use explore-edit-evaluate-refine cycle. Target 5000+ score per test case."
---

# Axis-Aligned Polygon Construction Strategy

## Objective
Build an axis-aligned polygon to maximize (mackerels inside - sardines inside + 1).

## Key Constraints
- Polygon edges must be parallel to x or y axes
- Max 1000 vertices, max perimeter 400000
- Coordinates 0 to 100000
- Output: m on first line, then m lines of "x y"

## Construction Pipeline

### Phase 1: Parse Input
- Read N (always 5000)
- Read N mackerel coordinates (x_i, y_i)
- Read N sardine coordinates (x_{N+i}, y_{N+i})

### Phase 2: Find Candidate Regions
- Group fish by coordinate buckets (e.g., 1000x1000 grid)
- Identify grid cells with many mackerels and few sardines
- Merge adjacent good cells to form a candidate "region"

### Phase 3: Build Polygon
- For each region, find its bounding box
- Expand the bounding box outward to include nearby mackerels
- Connect the expanded boxes with axis-parallel segments
- Ensure no self-intersection (keep regions separated)

### Phase 4: Validate
- Check vertex count <= 1000
- Check perimeter <= 400000
- Check coordinates in range [0, 100000]
- Output as: m \n x0 y0 \n x1 y1 \n ... \n x_{m-1} y_{m-1}

### Phase 5: Iterate
- Try multiple strategies: (a) one big polygon around best region, (b) multiple small polygons, (c) expanding rectangles
- Use evaluate_solution to score each approach
- Keep the highest scoring version

## Common Pitfalls
- DO NOT output empty or invalid polygons
- DO NOT exceed vertex limit
- DO NOT exceed perimeter limit
- Coordinates must be integers
- Adjacent edges must be perpendicular (not 180 turns)

## Example Output Format
8
0 0
10000 0
10000 5000
5000 5000
5000 10000
0 10000
0 5000
