---
name: discovery-optimization
description: "Optimize orthogonal polygon construction for a fish-capture problem. Generate candidate polygons, use probe to rank them cheaply, then evaluate the best candidates fully. Focus on exploring diverse shapes rather than one long search."
---

# Orthogonal Polygon Optimization for Fish Capture

## Objective
Maximize: mackerels inside - sardines inside + 1 (clamped at 0)

## Strategy Overview
1. **Generate diverse candidate polygons**: Try multiple shapes quickly
   - Simple rectangles
   - Rectangles with one or two "cuts" (removing sub-rectangles)
   - L-shaped or U-shaped polygons
   - Multi-lobed polygons if budget allows

2. **Use probe_solution aggressively**: 
   - Call probe on each candidate BEFORE evaluate
   - Probe uses ~10s on subsampled data and doesn't count against evaluation budget
   - Filter out poor candidates early
   - Only run full evaluate on top 3-5 candidates

3. **Iterative refinement**:
   - After finding a working polygon, try small modifications
   - Move boundaries by 50-200 units
   - Add/remove single cuts
   - Try merging nearby regions

4. **Exploration vs exploitation**:
   - First 5-7 evals: explore diverse shapes (rectangles of different sizes/positions)
   - Middle evals: refine the best shape found
   - Last evals: try completely different approaches if plateaued

5. **Time budget**: You have 2 seconds per full evaluation. Build your polygon generation to complete well within this limit. If generating polygons takes >1 second, simplify your approach.

## Concrete Implementation Steps

Step A: Rectangle enumeration
- Try centering on dense mackerel regions
- Try corners of the coordinate space
- Vary size: small (100x100), medium (500x500), large (2000x2000)

Step B: Adding cuts
- If a rectangle catches many sardines, try cutting out a sub-rectangle where sardines cluster
- Use probe to quickly test if a cut improves score

Step C: Multi-region polygons
- If single rectangle fails, try disconnected regions (output as one polygon by connecting with thin corridors)
- Focus on regions with high mackerel-to-sardine ratio

## Red Flags
- If score hasn't improved after 3 full evaluations: try a fundamentally different shape
- If probe scores are very low (< 50): something is wrong with your polygon generation
- If you run out of evaluations: submit your best score even if not optimal
