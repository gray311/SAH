---
name: discovery-optimization
description: "Geometric optimization for polygon construction. Uses probe_solution to rank variants cheaply\nbefore full evaluation. Applies targeted mutations: expand toward mackerels, prune sardine\npockets, refine edges, shift away from sardine clusters."
---

# Geometric Polygon Optimization

## Strategy

1. **Analyze**: Understand current polygon - where are mackerels? Where are sardine pockets?
   Use probe results to gauge score impact of different mutations.

2. **Mutate with ONE approach at a time**:
   - **Expand**: Extend edges outward toward mackerel-rich areas outside polygon
   - **Prune**: Cut out sardine-rich interior regions, creating holes
   - **Refine**: Add vertices along edges to capture boundary fish
   - **Shift**: Move polygon centroid toward mackerel clusters

3. **Validate pipeline**:
   - Edit code (targeted SEARCH/REPLACE)
   - Probe (approximate score, fast)
   - If probe improved, Evaluate (official score)
   - If worsened, try different mutation

4. **Iterate**: Track best score, try different mutations when stuck
   Combine carefully: expand then refine, or prune then expand.

## Key Insights for This Problem

- Dense mackerel clusters are valuable - build polygon around them
- Sardine-rich regions should be excluded (holes or avoidance)
- Small edge extensions often outperform full rewrites
- Monitor perimeter (<400,000) and vertex count (<1000)
- Internal search should use KD-tree or grid for fast fish counting
- Per-mutation cost < 0.5s allows many iterations

## Tool Usage

- probe_solution: Rank multiple mutation variants quickly (doesn't use eval budget)
- evaluate_solution: Confirm best variants officially
- Only one substantive edit per turn

## Time Management

- Per-evaluation timeout is 2.0s with safety margin
- Multiple internal mutations are allowed
- Use efficient data structures (KD-tree, grid buckets)
- Early termination on bad branches
