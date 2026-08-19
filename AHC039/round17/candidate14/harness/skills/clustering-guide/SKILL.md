---
name: clustering-guide
description: Cluster mackerels by proximity (threshold=500), compute bounding boxes, try 4-8 vertex polygons with optional sardine notches, run 10-15 searches.
---

# Mackerel Clustering Strategy

## Core Idea

Directly cluster mackerels by coordinate proximity and build bounding boxes around dense regions.

## Step-by-Step Method

### Step 1: Parse Fish Coordinates

- Read all 2N coordinates from input
- First N lines: mackerels
- Next N lines: sardines

### Step 2: Cluster Mackerels

- Two mackerels are "connected" if they're within 500 units in both x and y
- Use union-find or BFS to find connected components
- Track each cluster's size and bounding box

### Step 3: Build Candidate Polygons

For each cluster:
- Compute bounding box: [min_x, max_x] × [min_y, max_y]
- Try polygon variations:
  * Tight 4-vertex rectangle
  * Expanded 4-vertex rectangle (+50 to +150 units in each direction)
  * 6-8 vertex polygon with "notches" to exclude nearby sardines

### Step 4: Score and Select

- For each polygon, count exact mackerels and sardines inside using point-in-rectangle test
- Compute score = max(0, mackerels - sardines + 1)
- Keep the best polygon across all candidates

### Step 5: Output

- Output format: m (vertices), then m lines of "x y"
- Ensure: 4 ≤ m ≤ 1000, all coordinates in [0, 100000], axis-aligned edges
- Run 10-15 independent searches for diversity

## Key Success Factors

- Direct coordinate parsing (no grid approximation)
- Tight clustering to avoid including sardines
- Multiple polygon variations per cluster
- Multiple searches to explore different cluster combinations
