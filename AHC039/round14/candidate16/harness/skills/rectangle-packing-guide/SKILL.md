---
name: rectangle-packing-guide
description: Use coordinate-focused rectangle packing. Find dense mackerel cells, generate axis-aligned rectangles, combine multiple rectangles, local search refinement.
---

# Rectangle Packing Guide for Polygon Optimization

## Core Idea

Instead of grid-based corridor expansion, use coordinate-focused rectangle packing:
- Parse actual fish coordinates
- Build spatial index for fast region queries
- Generate axis-aligned rectangles around mackerel-dense regions
- Combine multiple rectangles into valid polygons

## Step-by-Step Method

### Step 1: Input Parsing and Spatial Indexing
- Extract all mackerel and sardine coordinates from input
- Build grid with cell_size=100 (or quadtree for sparse data)
- Count M and S in each cell
- Identify high-density mackerel cells (M >= 3, S <= 1 ideal)

### Step 2: Rectangle Candidate Generation
For each high-density cell:
- Generate rectangles of varying sizes (1x1 to 5x5 cells)
- Rectangle boundaries align to cell grid lines (multiples of 100)
- Calculate estimated score: M - S in the rectangle
- Prefer rectangles with high M and low S
- Filter by perimeter constraint (<= 400,000)

### Step 3: Multi-Rectangle Combination
Combine 2-10 rectangles:
- Option A: Union into complex axis-aligned polygon
- Option B: Create single enclosing rectangle
- Option C: Multi-holed polygon (outer + inner boundaries for sardines)
- Ensure no self-intersections and valid vertex count (4-1000)

### Step 4: Local Search Refinement
For each candidate polygon:
- Shift entire polygon by small amounts (±50, ±100 units)
- Expand/contract individual edges by multiples of 100
- Try splitting large polygons into smaller rectangles
- Try merging nearby rectangles
- Use spatial index for fast scoring

### Step 5: Multiple Restarts
- Run 20-30 restarts with different random seeds
- Each restart: generate 50-100 rectangle candidates
- Evaluate top 10-20 per restart using full evaluation
- Track global best

## Key Success Factors
- Fine-grained: Work at fish-coordinate level, not coarse grid cells
- Rectangle-focused: Axis-aligned rectangles are natural for this problem
- Combinatorial: Try combining multiple small rectangles
- Efficient: Use spatial index for O(1) scoring during search
- Diverse: Many restarts to explore different packings
