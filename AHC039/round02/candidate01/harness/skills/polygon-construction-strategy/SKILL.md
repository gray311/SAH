---
name: polygon-construction-strategy
description: Task-specific playbook for constructing orthogonal polygons to maximize (mackerels - sardines + 1). Use when stuck or starting fresh.
---

# Polygon Construction Strategy for Mackerel-Sardine Problem

## Core Idea
Build an orthogonal polygon that covers mackerel clusters while excluding
sardine clusters. The polygon must be rectilinear (all edges axis-aligned).

## Step 1: Analyze Fish Distribution
- Use analyze_fish_distribution to understand where mackerels and sardines cluster
- Note the coordinate ranges and centroids of each type
- Identify regions with high mackerel density and low sardine density

## Step 2: Choose Construction Approach
- **Bounding Box Approach**: Create a simple rectangle covering most mackerels
  but try to exclude sardine-dense regions by cutting out notches
- **Convex Hull with Holes**: Construct a polygon that follows mackerel positions
  while keeping sardines outside
- **Grid-Based**: Divide the plane into grid cells, select cells with high mackerel/sardine ratio

## Step 3: Refine Vertices
- Start with a coarse polygon (few vertices)
- Add vertices at mackerel positions to capture more points
- Round coordinates to grid points (integers)
- Check perimeter constraint (<=4e5) and vertex count (<=1000)

## Step 4: Validate Constraints
- Ensure no self-intersections
- Verify all edges are axis-aligned
- Check that coordinates are in [0, 100000]
- Ensure polygon is simple (non-self-intersecting)

## Step 5: Iterative Improvement
- Use probe_solution to test multiple variants quickly
- Try expanding vertices outward, then contracting to exclude sardines
- Use KD-tree to efficiently find fish inside/outside the polygon

## Key Heuristics
- Mackerels and sardines are placed adversarially
- The optimal polygon often has many vertices (up to 1000)
- Corner cases: all fish on one side, sardines intermingled with mackerels
- Time budget: 2s per test case - keep construction O(N log N) or O(N)
- Use the seed program's structure but improve the search strategy
