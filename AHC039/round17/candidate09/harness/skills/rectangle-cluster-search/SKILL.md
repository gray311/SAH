---
name: rectangle-cluster-search
description: Fast rectangle-based polygon optimization. Use coarse grid, generate rectangles centered on high-score cells, combine nearby clusters, local hill climbing.
---

# Rectangle-Based Cluster Search Strategy

## Core Idea

Instead of complex corridor expansion, use simple axis-aligned rectangles centered on fish-dense cells for faster execution and better coverage.

## Step-by-Step Method

### Step 1: Coarse Grid Analysis

- Build 100x100 grid over [0,100000]x[0,100000] (cell_size=1000)

- Count mackerels (M) and sardines (S) in each cell

- Compute cell score = M - S

- Identify top 10 cells with highest positive score


### Step 2: Rectangle Generation

For each top cell, generate rectangles centered on it:

- Try sizes: 50x50, 100x100, 150x150, 200x200, 250x250 units

- For each rectangle, compute score by summing grid cells inside

- Calculate efficiency: score / perimeter

- Keep top candidates


### Step 3: Cluster Combination

- Group nearby rectangles (centers within 300 units)

- For each group, compute combined bounding box or union

- Output valid polygon with 4-1000 vertices

- Ensure: integer coordinates, no self-intersection, perimeter <= 400,000


### Step 4: Local Hill Climbing

For each candidate polygon:

- For each edge, try shifts ±10, ±20 units

- Use grid-based rectangle query for fast scoring

- Keep shifts that improve M - S

- Repeat once more if improvement


### Step 5: Few Restarts

- Run 5-8 restarts with different random seeds

- Each restart:
  * Randomly perturb top cell selection (±200 units)
  * Pick 3-4 perturbed top cells
  * Build 2-3 rectangles per cell
  * Combine and hill climb

- Output best polygon across all restarts


## Key Success Factors

- Use coarse grid for speed (100x100 vs 200x200)
- Simple rectangles are faster to evaluate than complex corridors
- Fewer restarts (5-8) save time while still exploring diversity
- Local hill climbing refines edge positions efficiently
- Focus on high M-S regions to maximize score
