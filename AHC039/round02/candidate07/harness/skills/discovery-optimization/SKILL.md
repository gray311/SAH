---
name: discovery-optimization
description: "Geometric optimization for axis-aligned polygons. Load this skill to understand fish distribution,\nconstruct initial polygons with perimeter constraints, then use probing to guide iterative improvement.\nProbes are cheap (2000-point sample) and do not consume the evaluation budget."
---

# Geometric Optimization Method

## Phase 1: Analyze the input
- Call analyze_points immediately to see fish density patterns
- Identify clusters of mackerels vs sardines
- Note the bounding box and coordinate ranges

## Phase 2: Construct initial polygon
- Start with a simple rectangle covering mackerel-rich areas
- Ensure all edges are axis-aligned (horizontal or vertical only)
- Check perimeter <=400,000 and vertices <=1000
- Avoid including sardine clusters

## Phase 3: Probing-based improvement
- Make small edits: extend one edge inward, cut off a corner, shift a boundary
- Call probe_solution after each edit to rank variants cheaply
- Keep top 3 by probe score
- Full-evaluate only those 3

## Phase 4: Iterative refinement
- For each promising variant, try different mutations:
  - Extend edges toward mackerel clusters
  - Cut off sardine-heavy regions
  - Adjust corners to capture more mackerels
- Use probe to quickly eliminate bad directions
- Cycle through probing until time limit or no improvement

## Phase 5: Final submission
- Ensure the best variant meets all constraints
- Output the vertex coordinates in order
- Call finish with a brief summary

## Critical rules
- ALWAYS use axis-aligned edges (no diagonal edges)
- Keep perimeter under 400,000
- Use probe_solution FIRST before evaluate_solution
- Implement a search loop, not a static construction
- Make edits that change the score, not cosmetic changes
