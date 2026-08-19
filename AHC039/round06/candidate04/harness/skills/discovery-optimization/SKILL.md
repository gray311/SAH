---
name: discovery-optimization
description: "Iteratively optimize a C++ program's EVOLVE-BLOCK to maximize the score (mackerels - sardines + 1) for an orthogonal polygon construction task. The program constructs polygons to enclose high-density mackerel regions while avoiding sardines. Use analyze_fish_clusters first to identify promising regions, then construct/bound polygons accordingly. Under a fixed evaluation budget."
---

# Orthogonal Polygon Optimization for Fish Separation

## Task Understanding
- Maximize: score = max(0, mackerels_inside - sardines_inside + 1)
- N = 5000 mackerels, N = 5000 sardines
- Construct an orthogonal polygon (axis-aligned edges)

## Core Strategy: Cluster-Based Construction

### Step 1: Analyze Fish Distribution (USE ANALYZE_FISH_CLUSTERS)
- Call analyze_fish_clusters at the start
- This tool returns high-density mackerel regions (centroid, bbox) and sardine-exclusion zones
- Note which regions have high mackerel density and low sardine density
- These are your TARGET regions for the polygon

### Step 2: Initial Polygon Construction
- Start with a 4-vertex rectangle around the highest-density mackerel cluster
- If sardines are nearby, consider expanding to avoid them OR contracting to exclude them
- Check that the rectangle's perimeter ≤ 400,000 and has ≤ 1000 vertices

### Step 3: Refinement
- If the score is low, try:
  - Adding more vertices to better follow mackerel cluster boundaries
  - Shifting the polygon to exclude high-density sardine regions
  - Merging multiple mackerel clusters with one polygon
- Each refinement should be SUBSTANTIAL (change multiple vertices or the shape significantly)

### Step 4: Evaluation Strategy
- After editing, call evaluate_solution to score the new polygon
- If valid but low score: try a different construction based on analyze_fish_clusters
- If invalid (perimeter too large, too many vertices, self-intersecting): fix that specific constraint
- If program times out: reduce internal search iterations or simplify the construction

### Common Pitfalls
- **Perimeter too large**: Reduce the polygon size or use fewer vertices
- **Too many vertices**: Start with 4 vertices and add only if needed
- **Self-intersection**: Use simple axis-aligned rectangles initially
- **Timeout**: The C++ program must finish within ~1.9 seconds. Don't do exhaustive search in the EVOLVE-BLOCK.
- **Invalid coordinates**: Keep all coordinates in [0, 100000]

## Tool Discipline
- **ONE tool per turn**: edit_solution → evaluate_solution → analyze for new edit
- analyze_fish_clusters: call once at start, then only when stuck
- edit_solution: targeted changes or complete rewrites when fundamentally changing approach
- evaluate_solution: call after each edit to get real score
- finish: when budget exhausted or no improvement possible

## Sample Construction Pattern
1. analyze_fish_clusters → get clusters
2. edit_solution → create rectangle around top cluster
3. evaluate_solution → check score
4. If low: edit_solution → add vertices to include more mackerels
5. evaluate_solution → check score
6. Repeat or finish
