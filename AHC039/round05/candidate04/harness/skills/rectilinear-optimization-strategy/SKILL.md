---
name: rectilinear-optimization-strategy
description: Step-by-step playbook for optimizing rectilinear polygons to maximize mackerel capture minus sardine catch. Focus on bounding box strategies, cluster analysis, and constraint-aware construction.
---

# Rectilinear Polygon Optimization Strategy
## Core Idea Construct orthogonal polygons that enclose mackerel clusters while avoiding sardines.
## Strategy A: Bounding Box of Mackerel Subset 1. Select k mackerel points (k in [100, 500]) to represent clusters 2. Compute their bounding box 3. Count mackerels inside (use KD-tree or grid) 4. Count sardines inside 5. Score = mackerels - sardines + 1 6. Vary k and seed selection
## Strategy B: Cluster-Based Polygon 1. Cluster mackerels (simple: by x-coordinate bands or y-coordinate bands) 2. For each cluster, build a tight bounding box 3. Merge boxes into one orthogonal polygon (chain them) 4. Compute score
## Strategy C: Sardine-Avoidance Expansion 1. Start with mackerel cluster bounding box 2. Expand each edge outward 3. Stop when hitting a sardine point or perimeter limit 4. This excludes sardines from interior
## Strategy D: Grid-Fill Approach 1. Create 100x100 grid over 0-100000 space 2. For each cell, count mackerels and sardines 3. Fill cells with mackerel:sardine ratio > threshold (e.g., > 2:1) 4. Extract filled cells as orthogonal polygon
## Parameter Variations to Try - Subset size: [100, 200, 400, 800, 1000] - Grid resolution: [50x50, 100x100, 200x200] - Ratio threshold: [1.5, 2.0, 3.0] - Expansion amount: [0, 500, 1000, 2000]
## C++ Implementation Tips - Pre-sort/cluster mackerels using coordinate bands - Use KD-tree for fast point-in-polygon queries - Maintain per-test-case best score - Avoid O(N^2) operations; use spatial data structures - Output valid rectilinear polygon format
## Example C++ Pattern # Select k mackerels with smallest y-coordinates # Sort mackerels by y # Take first k # Compute bounding box # Output 4 vertices
