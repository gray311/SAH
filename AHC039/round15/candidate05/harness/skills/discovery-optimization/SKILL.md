---
name: discovery-optimization
description: "Direct coordinate-space search. Start with minimal polygon around a mackerel, expand edges outward while improving score, run multiple trials."
---

# Direct Coordinate-Space Polygon Search

## Phase 1: Parse and Index Fish
- Read all fish coordinates from input
- Separate into mackerels (type 1) and sardines (type -1)
- Sort by x-coordinate for efficient range queries
- Consider using 2D data structure or simple O(N log N) scanning

## Phase 2: Initialize Search
For each trial (5-8 trials):
- Pick a random mackerel as seed point
- Create minimal valid 4-vertex polygon around it:
  - Vertices: (x, y), (x+1, y), (x+1, y+1), (x, y+1)
  - This captures the seed mackerel
- Compute initial score

## Phase 3: Edge Expansion Search
For each edge in the polygon (up to 1000 iterations):
- Try extending each vertex outward in 4 cardinal directions
- For each candidate extension:
  - Build new polygon (check validity: perimeter, vertex count, bounds)
  - Count mackerels inside: iterate through sorted mackerel list, check if each is inside
  - Count sardines inside: same for sardines
  - Compute score = M - S + 1
  - Keep extension if score improves by at least 0.5

## Phase 4: Smart Termination
- Stop if: no improvement for 20 consecutive edge checks
- Or: polygon reaches 500 vertices
- Or: perimeter exceeds 400,000

## Phase 5: Select Best
- Track best score and corresponding polygon across all trials
- Output single best polygon in required format

## C++ Implementation Tips
- Use std::vector and std::sort for O(N log N) initialization
- Point-in-polygon for axis-aligned: check if point is inside bounding box
- For efficiency: sweep-line or simple O(M + S) per evaluation (M,S <= 5000)
- Total time target: < 2.0 seconds per evaluation
- Use fast I/O: ios::sync_with_stdio(false); cin.tie(nullptr);
