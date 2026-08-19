---
name: discovery-optimization
description: "KD-tree based rectangle optimization. Use existing spatial index to find mackerel-dense regions, apply local rectangle shrinking, run 5-10 efficient restarts."
---

# KD-Tree Rectangle Optimization Strategy

## Phase 1: Region Analysis
- The seed program builds a KD-tree on all fish positions
- Query the KD-tree for fish in rectangular regions
- Find rectangles where mackerel_count > sardine_count

## Phase 2: Rectangle Optimization
For each candidate rectangle:
- Query KD-tree to get exact fish counts
- Compute score = mackerels - sardines + 1
- Try shrinking each edge by 100, 500, 1000, 2000, 5000 units
- Keep shrink that improves score
- Repeat 2-3 rounds of shrinking

## Phase 3: Multiple Restarts
- Run 5-10 restarts
- Each restart starts with a random subregion (e.g., 20000x20000)
- Apply rectangle shrinking optimization
- Track best rectangle

## Phase 4: Output
- Output the best rectangle as 4 vertices
- Ensure validity: perimeter <= 400,000, coords in range

## Key Implementation Details
- Use the existing KD-tree from the seed program
- Rectangle query on KD-tree is O(log N + k) where k = fish count
- Total time per evaluation: ~1.5s with careful implementation
- Simpler than grid-based approach: no grid building, no corridor tracking
