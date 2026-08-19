---
name: corridor-expansion-guide
description: Use corridor expansion to grow from mackerel-dense cells through sardine-free paths. Expand in 4 directions, avoid regions with S > M + 2, combine corridors into polygons.
---

# Corridor Expansion Guide for Polygon Optimization

## Core Idea
Instead of building polygons around isolated clusters, expand through sardine-free corridors
to connect mackerel-rich regions and create multi-lobed structures.

## Step-by-Step Method

### Step 1: Grid Analysis
- Build 200x200 grid over [0,100000]x[0,100000] (cell_size=500)
- Count mackerels (M) and sardines (S) in each cell
- Compute cell score = M - S
- Identify top 15 cells with positive score

### Step 2: Directional Expansion
For each top cell, try expanding in each cardinal direction:
- North: decrease row index
- South: increase row index
- East: increase column index
- West: decrease column index

For each direction:
- Start from seed cell and move outward step by step
- At each step, check the new cell's M, S counts
- Continue if: cell is in bounds AND (M >= S OR S < M + 2)
- Stop if: out of bounds, M - S < 0, or S > M + 2
- Record all cells in the corridor

### Step 3: Polygon Formation
Convert corridor(s) into polygon:
- Single corridor: create rectangular boundary around corridor cells
- Multiple corridors from same seed: combine into L-shape or multi-lobed structure
- Ensure: 4 <= vertices <= 1000, integer coordinates, no self-intersection

### Step 4: Hill Climbing
For each polygon candidate:
- For each edge, try shifts ±5, ±10, ±15, ±20, ±25 units
- Use grid-based rectangle query for fast scoring
- Keep shift that improves M - S
- Repeat 3 refinement rounds

### Step 5: Multiple Restarts
- Run 15-20 restarts with different random seeds
- Each restart: perturb top cell selection, build 3-5 corridors, combine, hill climb
- Output best polygon across all restarts

## Key Success Factors
- Avoid sardine-dense regions (S > M + 2) to minimize penalties
- Use corridor expansion to create extended polygons that capture multiple clusters
- Deep hill climbing to fine-tune edge positions
- Many restarts to explore diverse polygon shapes
