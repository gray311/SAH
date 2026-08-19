---
name: discovery-optimization
description: "Cluster-based bounding box optimization. Detect mackerel clusters, create tight bounding boxes, avoid sardines through precise coordinate selection."
---

# Cluster-Based Bounding Box Optimization Strategy

## Core Strategy
Instead of complex corridor expansion, use simple tight bounding boxes around mackerel clusters. Small boxes maximize mackerel capture while minimizing sardine overlap.

## Implementation Steps

### Step 1: Input Parsing
- Read N (always 5000)
- Read 5000 mackerel coordinates into vector mackerels
- Read 5000 sardine coordinates into vector sardines
- Store for fast lookup or sorted structure

### Step 2: Cluster Detection
- Scan mackerel coordinates to find dense regions
- Group nearby mackerels within approximately 500 units in both x and y
- For each cluster, compute bounding box: (min_x, min_y, max_x, max_y)

### Step 3: Bounding Box Evaluation
For each candidate box (xmin, ymin, xmax, ymax):
- Count mackerels inside: x in [xmin, xmax] AND y in [ymin, ymax]
- Count sardines inside: same condition
- Score = mackerel_count - sardine_count
- Only accept boxes with score > 0 (or score >= -1 for growth)

### Step 4: Refinement Loop
For each promising box:
- Try expanding edges by +10, +20, +30 units
- Try shrinking edges by -10, -20 units (if score improves)
- Try shifting entire box by small amounts
- Use binary search on boundaries to find optimal extent

### Step 5: Multi-Box Combination
- Start with top 5-10 individual boxes
- Check if combining adjacent boxes creates better score
- Combine only if perimeter constraint (<=400000) still satisfied

### Step 6: Polygon Construction
- Convert boxes to vertex sequences
- For single box: 4 vertices (min_x,min_y), (max_x,min_y), (max_x,max_y), (min_x,max_y)
- For combined boxes: trace boundary carefully to avoid self-intersection
- Ensure 4 <= vertices <= 1000
- Validate with simple point-in-polygon check

### Step 7: Output
- Output vertex count m
- Output m lines of "x y" coordinates
- Ensure clockwise or counter-clockwise order

## C++ Optimization Tips
- Use arrays/vectors not std::map for coordinate storage
- Implement simple range counting with iteration (N=5000 is small enough)
- Use early termination in counting loops
- Pre-sort coordinates if doing many queries
- Keep search loop simple: 10-20 variants per evaluation
