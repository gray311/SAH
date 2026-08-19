---
name: geometric-search-strategy
description: A playbook for constructing search algorithms that build optimal axis-aligned polygons for the mackerel-sardine packing problem. Use when the current solution is a fixed polygon or simple heuristic.
---

Geometric Search Strategy for Polygon Optimization
Understanding the Problem: We need to construct an axis-aligned polygon that maximizes: (mackerels inside) - (sardines inside) + 1.
Key constraints: - Max 1000 vertices, perimeter <=400000 - Integer coordinates in [0, 100000]^2 - Edges must be axis-aligned (horizontal or vertical) - No self-intersections
Search Algorithm Design:
Approach 1: Greedy Expansion from Seed Start with a minimal polygon (e.g., bounding box of first mackerel). Iteratively expand in cardinal directions: For each iteration, try expanding N/S/E/W. Keep the expansion that adds the most net fish. Stop when no expansion is beneficial or perimeter budget reached.
Approach 2: Density-Based Regional Selection Divide the space into a grid (e.g., 200x200 cells, each 500x500). For each cell, count mackerels (m) and sardines (s) inside. Decision: include in polygon if m - s > threshold (e.g., 10). Then extract the union of included cells as a polygon.
Approach 3: Rectangular Union Find all maximal rectangles that contain more mackerels than sardines. Merge overlapping rectangles into a simple polygon.
Approach 4: KD-Tree Guided Construction Use KD-tree of mackerels to find dense clusters. For each cluster, build a local polygon. Combine local polygons with union or concatenation.
Implementation Tips: - Use integer coordinates throughout to avoid precision issues - Compute perimeter AFTER polygon construction to ensure budget compliance - Check self-intersection by verifying all internal angles are 90 or 270 degrees - For union of polygons, use a sweep-line or grid-based approach - Precompute fish positions in O(N) once, then query in O(1) per rectangle
Common Pitfalls: 1. Fixed polygons: Always construct the polygon from input data, never hardcode. 2. Too complex search: Keep internal search O(N log N) or better. 3. Perimeter overflow: Check perimeter constraint at each expansion step. 4. Self-intersection: Use grid-based union to avoid this. 5. Missing vertices: Polygon must have >=4 vertices.
Evaluation Workflow: 1. Try Algorithm 1 (greedy expansion) -> probe 2. Try Algorithm 2 (density grid) -> probe 3. Compare probe scores, run full eval on winner 4. If score < seed, try Algorithm 3 (rectangular union) 5. If score improves, refine the winning algorithm with parameters
