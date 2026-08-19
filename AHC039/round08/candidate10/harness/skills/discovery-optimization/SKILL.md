---
name: discovery-optimization
description: "Sardine-first exclusion polygon optimization. Construct polygon cutouts around sardine clusters before expanding to include mackerels. Use aggressive edge shifts (\u00b150..200) to escape local optima. Generate multiple notch placement variants and run hill climbing on each."
---

# Sardine-First Exclusion Polygon Strategy

## Core Idea
Instead of finding mackerel-dense regions and trying to avoid sardines, we proactively:
1. Group sardines into clusters
2. Build exclusion zones (notches/cutouts) around each cluster
3. Construct the polygon by taking the mackerel bounding box and carving out these exclusion zones
4. Expand intelligently in directions away from sardines

## Phase 1: Fish Analysis
- Parse all fish into mackerels (type=1) and sardines (type=-1)
- For sardines: use clustering with threshold 300 units
- For each sardine cluster, compute min/max x and y
- Compute the union bounding box of all sardine clusters

## Phase 2: Exclusion Zone Construction
For each sardine cluster:
- Determine which edges of the mackerel bounding box face the cluster
- Create a 150x150 exclusion notch extending from the mackerel box toward the sardines
- Use axis-aligned steps: move edge inward, create 3 new vertices forming a rectangular cutout

## Phase 3: Variant Generation
Generate 5-8 polygon variants:
- Base variant: one large exclusion zone
- Split variants: 2-3 smaller exclusion zones for same clusters
- Corner variants: expand mackerel box by 100-300 units in NW, NE, SW, SE corners (away from sardines)
- Rotation variants: rotate notch placement by 90 degrees

## Phase 4: Aggressive Hill Climbing
For each variant:
- For each of 10-20 edges:
  - Try shifts: -200, -100, -50, 50, 100, 200 units
  - Recompute score using grid query
  - Keep shift with best score
- Repeat 2-3 rounds
- Track best polygon

## Phase 5: Multiple Random Restarts
- Run Phases 1-4 with 3 different random seeds for sardine cluster selection
- Track global best

## Implementation Notes
- Use a 100x100 grid for fast fish counting (finer than previous 200x200)
- Pre-compute grid at startup
- Rectangle query = sum of grid cells covering rectangle
- Time per evaluation: < 1.5s for search, < 0.5s for validation
- Always output exactly m, then m lines of vertices
