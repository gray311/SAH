---
name: regional-rectangle-guide
description: Use coarse regional analysis to identify mackerel-dense areas and build large rectangles. Expand in 4 directions, avoid sardine-dense regions, combine rectangles, refine with large shifts.
---

# Regional Rectangle Strategy for Polygon Optimization

## Core Idea

Use coarse 50x50 grid (cell_size=2000) to identify broad mackerel-dense regions and build large axis-aligned rectangles that capture multiple clusters while minimizing sardine penalties.

## Step-by-Step Method

### Step 1: Coarse Grid Analysis

- Build 50x50 grid over [0,100000]x[0,100000] (cell_size=2000)
- Count mackerels (M) and sardines (S) in each cell
- Compute cell score = M - S
- Identify top 20 cells with highest positive score

### Step 2: Rectangle Construction

For each top cell:
- Start from cell center
- Expand in each cardinal direction (N, S, E, W)
- Continue expanding as long as:
  * Cell score >= 0
  * Perimeter < 400,000
  * Sardine density is not too high (S < M * 3)
- Track the best rectangle (highest M - S score)

### Step 3: Multi-Rectangle Combination

- Select 2-5 best rectangles
- Compute their union (merge overlapping regions)
- Convert to single polygon with no self-intersection
- Can form L-shapes, multi-lobed structures

### Step 4: Edge Position Refinement

For each candidate polygon:
- For each edge, try shifts: ±100, ±200, ±300 units
- Use rectangular score estimation for fast evaluation
- Keep shift that maximizes M - S
- Repeat 2 refinement rounds

### Step 5: Regional Diversity Search

- Run 25-30 restarts with different random seeds
- Each restart:
  * Randomly perturb top cell selection
  * Pick random subset of 3-5 top cells
  * Build rectangles, combine, refine
- Output single best polygon

## Key Success Factors

- Use coarse grid to capture broad patterns
- Build large rectangles to maximize coverage
- Use large edge shifts (±100..300) for effective refinement
- Many restarts to explore diverse configurations
