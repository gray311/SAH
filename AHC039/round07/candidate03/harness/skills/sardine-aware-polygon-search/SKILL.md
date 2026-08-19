---
name: sardine-aware-polygon-search
description: Search strategy for axis-aligned fish-capture - identify excludable sardines, build shapes around dense mackerel clusters, use probe_solution for rapid variant ranking, and iteratively refine toward maximum (mackerels minus sardines plus 1) score.
---

# Sardine-Aware Polygon Search Method

## Core Principle
The score is mackerels_inside - sardines_inside + 1. Every sardine inside reduces your
score. The optimal strategy is to capture dense mackerel regions while EXCLUDING sardine
clusters. Focus on sardines near polygon boundaries (easy to exclude) vs. deep inside
mackerel clusters (hard to exclude).

## Search Pipeline

### Step 1: Analyze Fish Distribution
- Compute mackerel bounding box [min_x, max_x] times [min_y, max_y]
- Identify "easy exclude" sardines: those within 300 to 500 units of bbox edges
- Identify sardine clusters (3 or more sardines within 800 units): one shape can exclude all
- Determine recommended polygon shape:
  - Many boundary sardines (greater than 30 percent) -> L-shape polygons
  - Multiple sardine clusters (greater than 3) -> Multi-rectangle with gaps
  - Dense mackerels (greater than 3000) -> Stepped/staircase polygons
  - Otherwise -> Simple bounding box

### Step 2: Generate Candidate Shapes
- Bounding box variants: simple bbox, shrunk bbox, expanded bbox
- L-shaped polygons: capture corner, cut off sardine-heavy region
- Stepped polygons: staircase following mackerel density contours
- Multi-rectangle union: capture separate clusters with gaps for sardines

### Step 3: Probe-Guided Ranking
- Generate 5 to 10 candidate shapes (2 to 3 per type)
- Use probe_solution to test all (approximate score in approximately 10 seconds each)
- Rank by probe score, keep top 3
- Use evaluate_solution for top 3 to get exact scores
- Pick best, continue to refinement

### Step 4: Iterative Refinement
- From best polygon, try edge perturbations plus/minus 1 to 20 units
- Check validity (perimeter at most 400,000, non-self-intersecting)
- Count fish using spatial index (O(1) with grid)
- Keep modifications that improve score
- Run multiple random restarts (3 to 5 different seed shapes)
- Early termination: if no improvement for 0.15 seconds, finalize
- Continue until 1.8 seconds elapsed (0.1 second safety margin)

### Step 5: Final Output
- Output valid polygon: m on first line, then m lines of (x y)
- Ensure: m at most 1000, perimeter at most 400,000, axis-aligned, non-self-intersecting
- If multiple solutions, last one wins

## Key Tips
- Use grid-based spatial indexing (CELL_SIZE=500) for O(1) fish counting
- Always validate perimeter constraint after construction
- Sardines near polygon edges are your best target for exclusion
- Do not over-complexify: bbox plus smart refinements often win
- Use probe_solution to filter variants before full evaluation
- Log intermediate results with ctx.log() for debugging
