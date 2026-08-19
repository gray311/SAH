---
name: bounding-box-guide
description: Build tight bounding boxes around mackerel clusters. Evaluate boxes by counting fish inside. Refine boundaries to maximize mackerel gain versus sardine cost.
---

# Bounding Box Optimization Guide

## Core Idea
Use tight axis-aligned bounding boxes around mackerel clusters. Small boxes capture dense mackerel regions while avoiding sardine penalties.

## Step-by-Step Method

### Step 1: Input Setup
- Read N=5000 (always fixed)
- Store mackerel coordinates in a vector (indices 0 to N-1)
- Store sardine coordinates in a separate vector (indices N to 2N-1)

### Step 2: Cluster Detection
Scan through mackerel coordinates to find dense regions:
- Start from first unprocessed mackerel
- Find all mackerels within approximately 500 units in both x and y (the cluster)
- Mark these as processed
- Repeat until all mackerels are grouped

For each cluster, compute the bounding box:
- min_x = minimum x in cluster
- min_y = minimum y in cluster
- max_x = maximum x in cluster
- max_y = maximum y in cluster

### Step 3: Box Evaluation
For each bounding box (xmin, ymin, xmax, ymax):
- Count mackerels inside: iterate through all mackerels, check if xmin <= x <= xmax AND ymin <= y <= ymax
- Count sardines inside: same check for sardines
- Compute score = mackerel_count - sardine_count
- Track boxes with score > 0 (preferably score >= 2 for safety)

### Step 4: Boundary Refinement
For each promising box, try refinements:
- Expand: try (xmin-10, ymin-10, xmax+10, ymax+10), then (xmin-20, ymin-20, xmax+20, ymax+20)
- Shrink: try (xmin+10, ymin+10, xmax-10, ymax-10) if it improves score (tighter box)
- Shift: try moving entire box by (+10,+10), (+20,+20), etc.
- Use the refinement with highest score

### Step 5: Combination Strategy
- Take top 5-10 individual boxes
- Check if two adjacent boxes can be merged (share a common boundary)
- If merged, new box perimeter should still be <= 400000
- Recalculate score for combined box

### Step 6: Polygon Output
- For single box: output 4 vertices: (xmin,ymin), (xmax,ymin), (xmax,maxy), (xmin,maxy)
- For combined boxes: trace outer boundary (more complex, ensure no self-intersection)
- Ensure vertex count is between 4 and 1000
- All coordinates must be integers in [0, 100000]

### Step 7: Validation
- Check perimeter <= 400000
- Check all coords in valid range
- Output vertex count followed by coordinates

## Key Success Factors
- Tight boxes are better than large boxes (avoid sardine dilution)
- Multiple small boxes can beat one large box
- Focus on regions with high mackerel density
- Always check sardine cost before accepting a box
