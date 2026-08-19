---
name: discovery-optimization
description: "Iteratively optimize a C++ geometric optimization program under a fixed evaluation budget.\nUse for combinatorial/heuristic search tasks where internal exploration matters."
---

# Combinatorial Geometric Search for Polygon Optimization

This is an NP-hard problem. The seed program contains a KD-tree for fast fish counting.
YOUR JOB: Replace "one-shot construction" with "internal search loop".

## Search Loop Pattern (to implement in the EVOLVE-BLOCK):

1. Initialize candidate polygons from different strategies:
   - Rectangular hull (bounding box of mackerels)
   - Stair-step expansion (grow L-shaped poly around clusters)
   - Multi-axis partition (dividing plane into quadrants, selecting high-yield zones)
   - Spiral/helix pattern (expanding outward from high-density mackerel areas)

2. For each candidate:
   - Use the KD-tree (if available) or grid-based counting to estimate fish counts
   - Compute score = mackerels - sardines + 1
   - Track the best candidate

3. Refinement steps:
   - For each polygon, try moving vertices inward (exclude sardines) and outward (include mackerels)
   - Try merging adjacent high-yield regions
   - Try splitting low-yield regions

4. Budget management:
   - Track time elapsed; stop searching if approaching the safety margin
   - Prioritize promising regions first
   - If time is tight, output the best found
 
## Validation checklist before edit:
- Does this change enable internal search (not just one-shot)?
- Is the KD-tree being used efficiently?
- Are perimeter/vertex constraints respected?
- Is the search diverse enough to escape local optima?

## Tool usage:
- Call `edit_solution` to stage ONE concrete change (add a new strategy, refine search, improve a pattern)
- Call `evaluate_solution` to see if it improves
- If stuck, change the search diversity (add new polygon generation method)
- Never output the same code twice

## What NOT to do:
- Do not use `probe_solution` — scores aren't comparable to full evals for this task
- Do not try cosmetic changes; every edit must enable more/combinatorial search
