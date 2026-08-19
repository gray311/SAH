---
name: rectilinear-polygon-strategy
description: Guide the solver to optimize rectilinear polygon construction by using density probing to identify high-value regions before full evaluation.
---

# Rectilinear Polygon Optimization Playbook

## Understanding the Problem
- You're building an axis-parallel rectilinear polygon to maximize: mackerels_inside - sardines_inside + 1
- Key constraint: polygon edges must be horizontal or vertical only
- Time limit is tight (~2 seconds for full optimization across 150 test cases)

## Core Strategy: Probe Before Commit

### Phase 1: Generate a Baseline
Start with a simple rectangle or L-shape that covers a reasonable area.
Make it valid: 4+ vertices, perimeter < 400,000, no self-intersection.

### Phase 2: Use density_probe to Explore
After each edit to the polygon:
1. Call density_probe to get net_density estimate
2. Check if your edit improved net_density compared to baseline
3. If improved: keep editing in the same direction
4. If decreased: try a different modification direction

### Phase 3: Multi-Variant Ranking
When you have multiple ideas (expand here, indent there, shift box):
1. Make all candidate edits
2. Call density_probe on each variant
3. Rank by net_density
4. Call evaluate_solution ONLY on the top 1-2 candidates

### Phase 4: Targeted Refinement
Based on probe results:
- High mackerel density region → expand the polygon into it
- High sardine density region → contract or add an indent to exclude it
- Low overall density → shift entire polygon to a different area

### Phase 5: Budget Management
- Use density_probe freely (~30 calls allowed)
- Use evaluate_solution sparingly (only 20 total budget)
- Confirm only your best candidates with full evaluation

## Common Patterns That Work
1. Start with a rectangle covering the center, then refine
2. Try covering dense clusters of mackerels with separate polygons (output only the best one)
3. Use indentations to "bite out" sardine clusters from a larger polygon
4. Systematically try different bounding box sizes and positions

## When to Call Each Tool
- edit_solution: After forming a geometric hypothesis
- density_probe: Immediately after edit_solution, before evaluate_solution
- evaluate_solution: Only when probe consistently shows improvement
- finish: When budget is low or you've exhausted promising directions

## Red Flags
- Time limit exceeded: simplify your optimization, use greedy approximations
- Invalid polygon: check vertex count, perimeter, self-intersection
- Low scores: your polygon isn't covering high-density mackerel regions
- Probe says improvement but eval says worse: probe has noise, trust the eval
