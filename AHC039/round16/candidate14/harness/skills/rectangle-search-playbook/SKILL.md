---
name: rectangle-search-playbook
description: Generate random rectangles from mackerel-dense grid cells, rank with probes, hill climb top 5, evaluate best of 30 restarts.
---

# Rectangle Search Playbook

## Overview
This strategy optimizes axis-aligned rectangles (4-vertex polygons) to maximize (mackerels - sardines + 1).

## Step 1: Grid-Based Density Analysis
- Create a 100x100 grid covering [0, 100000] x [0, 100000] (cell_size = 1000)
- Count mackerels and sardines in each cell by sampling the input
- Compute M-S score for each cell
- Identify the top 30 cells with the highest positive M-S scores

## Step 2: Rectangle Generation (30 restarts)
For each restart with a different random seed:
- Select 5 random seeds from the top 30 cells
- For each seed, generate 20 random rectangles:
  * Rectangle width: random integer in [200, 800]
  * Rectangle height: random integer in [200, 800]
  * Rectangle center: near the seed cell (±200 units random offset)
  * Clamp coordinates to [0, 100000]
- Total: 100 rectangles per restart

## Step 3: Probe-Based Ranking
- Use probe_solution to evaluate each rectangle (cheap, ~10 seconds)
- Probe scores are approximate but allow ranking many candidates
- Do NOT use evaluate_solution yet (saves evaluation budget)

## Step 4: Hill Climbing on Top 5
For the top 5 rectangles by probe score:
- Extract the 4 corner coordinates
- For each corner, generate shifted variants:
  * Shift each corner by ±5 units in x or y direction
  * Shift each corner by ±10 units in x or y direction
  * This generates up to 16 variants per rectangle (8 corners × 2 shift amounts)
- Use probe_solution to score all variants
- Select the best variant based on probe score

## Step 5: Full Evaluation
- Use evaluate_solution on the single best rectangle after hill climbing
- This consumes 1 evaluation credit and gives the exact score

## Step 6: Track and Output Best
- After 30 restarts, output the polygon (rectangle) with the highest evaluate_solution score
- Format: m=4 on first line, then 4 lines of x y coordinates

## Success Factors
- Probe first, evaluate last: use the 30 probe budget to rank many candidates
- Simple shapes work better: rectangles are easier to validate and faster to construct
- Hill climbing refines local optima: small edge shifts improve capture efficiency
- Many restarts ensure diversity: 30 restarts explore the search space thoroughly
