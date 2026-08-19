---
name: discovery-optimization
description: "Optimize orthogonal polygon construction for NP-hard heuristic problem. Use analyze_fish_distribution, probe for cheap scoring, then evaluate best variant. Bounded internal search inside each eval."
---

# Orthogonal Polygon Optimization for NP-hard Heuristic Problem

## Problem Understanding
- Maximize: max(0, mackerels - sardines + 1)
- Build orthogonal polygon (edges parallel to x/y axis)
- Constraints: <=1000 vertices, <=400000 perimeter, coords 0-100000

## Bounded Internal Search Strategy

Within EACH evaluation, run a systematic search:

### Step 1: Analyze Distribution
Call analyze_fish_distribution() ONCE to get:
- Count of mackerels/sardines per grid region
- Density hotspots
- Spread statistics

### Step 2: Generate Candidates
Implement 3-5 different polygon construction strategies:

Strategy A: Convex Hull of Dense Regions
- Identify top 20 dense mackerel clusters (20x20 grid cells)
- Compute convex hull of cluster centers
- Snap to integer coords, ensure orthogonality

Strategy B: Grid Sweeping
- Sweep a rectangle from min_x to max_x, min_y to max_y
- Iteratively refine edges to capture mackerels, avoid sardines
- Use orthogonal divisions

Strategy C: Greedy Expansion
- Start with minimal valid polygon
- Expand edges one unit at a time
- Accept expansion if delta score > 0 (use probe to check)

### Step 3: Probe-Based Ranking
For each candidate:
- Use probe_solution to get approximate score
- Track which strategy wins
- Keep best 3 by probe score

### Step 4: Full Evaluation
Call evaluate_solution ONCE on the probe-best candidate

### Step 5: Strategy Refinement
If score improves:
- Preserve the winning strategy
- Try refinements (edge tuning, region merging)
- If fails: revert to last good strategy, try different approach

## Critical Constraints
- KEEP program valid at every step
- Use SEARCH/REPLACE diffs for small changes
- Time limit: 1.95s per eval (internal search must complete well before)
- Safety margin: 0.05s

## Tool Call Sequence Example
1. analyze_fish_distribution() -> store results
2. edit_solution() -> add/modify Strategy A
3. probe_solution() -> score candidates
4. edit_solution() -> keep best, refine
5. probe_solution() -> verify refinement
6. evaluate_solution() -> full score
7. Repeat from step 2 or 3-6 until plateau
