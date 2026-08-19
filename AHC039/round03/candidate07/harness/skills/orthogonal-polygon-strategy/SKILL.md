---
name: orthogonal-polygon-strategy
description: A playbook for constructing orthogonal polygons on fish distributions. Use grid-cell density analysis to identify promising regions, then build perimeter-constrained polygons that hug high-density clusters. Prioritize simple shapes (rectangles, L-shapes) that can be efficiently constructed in C++.
---

# Orthogonal Polygon Construction Strategy

## Phase 1: Understand the data
- Read fish coordinates and their types (mackerel=+1, sardine=-1)
- Use grid cells of 5000x5000 to approximate density regions
- Compute net score per cell (mackerels - sardines)

## Phase 2: Identify promising regions
- Sort cells by net score descending
- Take top 50 cells as hotspots
- Find connected hotspots to form candidate regions

## Phase 3: Construct polygon
- Start from origin or boundary of hotspots
- Expand in orthogonal directions (only horizontal or vertical edges)
- Keep track of perimeter and vertex count
- Stop when perimeter exceeds 400,000 or vertices exceed 1000

## Phase 4: Refine
- Try local expansions into nearby cells
- Try cutting out low-score regions from interior
- Always re-check perimeter and vertex constraints

## Phase 5: Evaluate
- Use probe_solution to quickly score candidates
- Use evaluate_solution only on top 1-2 candidates
- Track best score and generate new variants

## Tips
- Simple rectangles and L-shapes are easiest to construct in C++
- Start with perimeter ~150,000 to leave room for refinements
- Never exceed vertex limit of 1000
- The 2.0s time limit per test case is strict
