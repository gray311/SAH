---
name: cluster-wrapping-guide
description: Identify mackerel-dense clusters by coordinate proximity, build rectangles avoiding sardines, combine top clusters.
---

# Cluster-Wrapping Guide for Polygon Optimization

## Core Idea

Directly identify clusters of mackerels by their x or y coordinates, then wrap them with rectangles
that avoid sardine-heavy regions.

## Step-by-Step Method

### Step 1: Parse Fish Positions

- Extract all mackerel and sardine coordinates from input
- Build spatial hash map for O(1) lookups
- Organize fish by x and y coordinates

### Step 2: Cluster Identification

- Group mackerels by x-coordinate (within ±100 units)
- Group mackerels by y-coordinate (within ±100 units)
- For each group, compute:
  * Bounding box: (min_x, min_y, max_x, max_y)
  * Mackerel count
  * Sardine count (points inside bounding box)
  * Score = mackerel_count - sardine_count

### Step 3: Select Top Clusters

- Sort clusters by score descending
- Select top 3-5 clusters with positive score
- Prefer clusters with high mackerel density

### Step 4: Rectangle Construction

- For each selected cluster, create axis-aligned rectangle
- Rectangle vertices: (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)
- Ensure integer coordinates within [0, 100000]

### Step 5: Iterative Expansion

- For each rectangle, try expanding sides by ±50, ±100 units
- For each expansion, count new mackerels and sardines
- Keep expansion if (new_mackerels - new_sardines) > 0
- Repeat 2-3 refinement rounds

### Step 6: Combine and Output

- Union top rectangles into single polygon
- Output vertices in order (4-1000 vertices)
- Ensure perimeter ≤ 400,000

## Key Success Factors

- Focus on clusters with high mackerel density
- Avoid expanding into sardine-heavy regions
- Use iterative expansion to fine-tune rectangles
- Combine multiple rectangles for larger coverage
