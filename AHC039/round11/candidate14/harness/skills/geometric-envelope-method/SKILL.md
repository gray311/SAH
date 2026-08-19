---
name: geometric-envelope-method
description: Build polygons by enumerating axis-aligned rectangles based on fish coordinates. Test bounding box, percentile-based rectangles, and edge-refined variants.
---

# Geometric Envelope Method for Fish Optimization

## Core Principle
Work DIRECTLY with fish coordinates. Find extreme points and test rectangles
formed by coordinate combinations. No grid abstraction.

## Step 1: Parse and Collect Coordinates
- Extract all mackerel (x_i, y_i) coordinates
- Extract all sardine coordinates separately
- Store in lists for quick access

## Step 2: Find Coordinate Extremes
- min_x, max_x = min/max of mackerel x-coordinates
- min_y, max_y = min/max of mackerel y-coordinates
- These define the initial bounding box

## Step 3: Test Bounding Box
- Count mackerels and sardines inside [min_x, max_x] × [min_y, max_y]
- Score = m - s + 1
- If score >= target, this may be optimal or near-optimal

## Step 4: Percentile-Based Rectangles
- Sort mackerel x-coordinates, pick top 50th, 60th, 70th percentiles
- Sort mackerel y-coordinates, pick top 50th, 60th, 70th percentiles
- Test combinations: [x_50, x_max] × [y_50, y_max], etc.
- Smaller rectangles may exclude sardines while keeping many mackerels

## Step 5: Edge Refinement
- For promising rectangle, shift each edge by small amounts (±1, ±2, ±5 units)
- Test each shifted boundary with test_rectangle tool
- Keep shifts that increase score
- Repeat for up to 3 refinement rounds

## Step 6: Multi-Rectangle Strategy
- If single rectangle score is poor, try 2-3 adjacent rectangles
- Find gaps between mackerel clusters
- Create thin rectangles connecting dense regions
- Ensure no self-intersection (axis-aligned rectangles don't intersect if properly ordered)

## Step 7: Output
- Convert rectangle(s) to polygon vertex list
- Ensure 4-1000 vertices, integer coords [0,100000]
- Perimeter <= 400,000
- Output in required format: m\nv1 v2\nv3 v4\n...

## Key Success Factors
- Direct coordinate work, not grid abstraction
- Test many rectangle combinations (enumerate, don't guess)
- Use both mackerel extremes and percentiles for boundaries
- Refine edges incrementally
- Combine rectangles only if beneficial
