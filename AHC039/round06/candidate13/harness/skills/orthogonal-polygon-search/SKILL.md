---
name: orthogonal-polygon-search
description: Method for bounded internal search to construct orthogonal polygons. Combines distribution analysis with probe-based ranking.
---

# Orthogonal Polygon Construction via Bounded Internal Search

## Overview
This skill guides the executor to implement a systematic search inside EACH evaluation:
1. Analyze fish distribution once
2. Generate 3-5 candidate polygons using different strategies
3. Rank candidates with probe_solution (cheap, ~10s)
4. Evaluate best candidate (expensive, ~5-60s, consumes budget)
5. Refine winning strategy or try new approach

## Strategy Library

### A. Convex Hull of Dense Regions
1. Divide space into 100x100 grid cells
2. Count mackerels per cell
3. Select top 20 cells by mackerel count
4. Compute centroid of each selected cell
5. Build convex hull of centroids
6. Snap vertices to integers, ensure orthogonality (axis-aligned edges only)

### B. Grid-Based Sweeping
1. Define bounding box of all mackerels
2. Start with minimal rectangle enclosing 80% of mackerels
3. Expand/contract edges one unit at a time
4. At each step, use probe to check if delta score > 0
5. Accept only improvements

### C. Greedy Cluster Expansion
1. Find highest mackerel-density cell
2. Start minimal polygon around it
3. Find adjacent cells with net positive mackerel - sardine gain
4. Expand polygon to include such cells
5. Repeat until no beneficial expansion available

### D. Dual-Region Intersection
1. Build two separate rectangles: one for mackerels, one avoiding sardines
2. Compute their intersection
3. Refine intersection boundaries to capture more mackerels
4. Ensure orthogonality and vertex count <= 1000

## Execution Protocol

For each evaluation budget cycle:

1. CALL analyze_fish_distribution() ONCE
   - Store hotspot cells, density stats
   - This informs which strategy to prioritize

2. GENERATE 3-5 CANDIDATES
   - Implement ALL strategies in parallel (do not commit to one yet)
   - Use edit_solution to add/modify strategy functions
   - Keep candidates as separate data structures

3. RANK WITH probe_solution (x3-5 calls, FREE)
   - For each candidate, stage its code and call probe_solution
   - Record approximate scores
   - Discard bottom candidates

4. EVALUATE BEST WITH evaluate_solution (1 call)
   - Stage the probe-winner's code
   - Call evaluate_solution
   - Record actual score
   - This is your only "real" score per iteration

5. REFINE OR RESTART
   - If score improved: keep strategy, try refinements
   - If score regressed: revert to previous best strategy, try different approach
   - Never call evaluate_solution twice in a row without probing first

## Timing Budget
- Per evaluation: hard limit 1.95s (2.0s - 0.05s safety margin)
- Internal operations must complete WELL BEFORE this deadline
- Use efficient data structures (KD-tree, spatial hashing)
- Avoid O(N^2) loops; aim for O(N log N) or O(N)

## Pitfalls to Avoid
- Do NOT call analyze_fish_distribution more than once per eval (reads all input)
- Do NOT call evaluate_solution on unpromising candidates (wastes budget)
- Do NOT generate candidate code that causes runtime errors (validity=0)
- Do NOT exceed 1000 vertices or 400000 perimeter in output
- Remember: probe scores are approximate, use them for ranking only, not as truth
