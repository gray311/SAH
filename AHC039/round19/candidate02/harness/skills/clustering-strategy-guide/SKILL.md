---
name: clustering-strategy-guide
description: Use mackerel clustering to build tight axis-aligned polygons around dense groups of mackerels. Avoid sardines by using minimal bounding boxes. Generate multiple diverse candidates per eval.
---

# Mackerel Clustering Strategy for Polygon Optimization

## Core Principle
Build TIGHT polygons around dense mackerel clusters, not loose ones that
include many sardines. Each polygon should maximize (mackerels - sardines).

## Step-by-Step Method

### Step 1: Input Parsing
- Read all mackerel coordinates from input
- Read all sardine coordinates from input
- Store as two separate lists

### Step 2: Cluster Identification
Find spatial clusters of mackerels:
- Use distance threshold of ~5000
- Points within threshold of each other form a cluster
- Use Union-Find or BFS to identify connected components

### Step 3: Bounding Box Construction
For each cluster:
- Find min_x, max_x, min_y, max_y
- Build minimal axis-aligned rectangle
- This is the "tightest" polygon around this cluster

### Step 4: Sardine Filtering
For each cluster's bounding box:
- Count sardines inside the box
- If sardines > mackerels, this cluster is NOT worth enclosing
- Prefer clusters where mackerels >> sardines

### Step 5: Diverse Generation
Generate multiple candidates:
- Individual cluster boxes (n of them)
- Combinations of 2-3 adjacent clusters
- Sometimes a large box covering many clusters

### Step 6: Ranking
- Score each candidate: mackerels - sardines + 1
- Use probe if available for fast approximate scoring
- Select top candidates for full evaluation

### Step 7: Output
- Output the best valid polygon
- Ensure: 4 <= vertices <= 1000, coordinates in [0, 100000]

## Key Success Factors
- Tighter polygons = fewer sardines inside
- Multiple clusters > single loose polygon
- Cluster-first approach beats grid-first approach
- Diversity: try different approaches, don't commit to one
