---
name: discovery-optimization
description: "Cluster-based polygon construction. Parse fish coords, identify mackerel clusters via hash map, build axis-aligned polygons around clusters, refine edges by coordinate-based fish counting, multiple restarts."
---

# Cluster-Based Polygon Construction

## Phase 1: Spatial Analysis
- Parse all fish coordinates from input
- Build hash map: position -> fish type (1 for mackerel, -1 for sardine)
- Identify mackerel clusters by finding positions with multiple mackerels nearby
- For each cluster, compute: center, bounding box, mackerel count, radius

## Phase 2: Cluster-Centric Expansion
From each mackerel cluster:
- Start with cluster bounding box as initial polygon
- Extend in 4 cardinal directions (N,S,E,W)
- At each step, check if extending captures more mackerels and/or avoids sardines
- Stop when: perimeter > 400,000, or extending captures sardines with M-S ratio drops
- Use coordinate-based counting: for new region, count fish at positions inside

## Phase 3: Multi-Cluster Strategy
- Identify 3-5 separate high-density mackerel clusters
- Build separate small polygons for each (4-lobed structure)
- Total perimeter must stay under 400,000

## Phase 4: Edge Refinement
For each edge of candidate polygon:
- Try parallel shifts: ±1, ±2, ±3, ±4, ±5, ±10 units
- For each shift, compute delta in mackerels captured (hash map lookup)
- Compute delta in sardines captured
- Keep shift that maximizes net change in (mackerels - sardines)
- Repeat 2-3 refinement rounds

## Phase 5: Multiple Restarts
- Run 10-15 restarts
- Each restart: randomly pick starting cluster (or random mackerel position)
- Build polygon from that seed, refine, track best

## C++ Implementation Notes
- Use std::unordered_map<Point, int> for O(1) fish lookup
- For coordinate shifts: count affected fish by checking positions in shifted region
- Build polygon vertices as integer coordinates
- Validate: 4 <= vertices <= 1000, perimeter <= 400000, coords in [0,100000]
- Output format: m followed by m lines of "x y"
