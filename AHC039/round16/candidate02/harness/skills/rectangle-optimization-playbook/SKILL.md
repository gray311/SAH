---
name: rectangle-optimization-playbook
description: Form one large rectangle from bounding box of top cells, expand edges by 20-100 units, 25 restarts.
---

# Rectangle Optimization Playbook

## Core Strategy

Instead of building multiple tiny rectangles, build ONE large rectangle that covers multiple mackerel clusters.

## Step-by-Step Method

### Step 1: Grid Construction

- Build 200x200 grid over [0,100000]x[0,100000] (cell_size = 500)
- Count mackerels (M) and sardines (S) in each cell
- Compute cell score = M - S

### Step 2: Find Top Cells

- Identify top 10 cells with highest positive score (M - S > 0)
- These are your seed points

### Step 3: Directional Expansion

For each top cell, expand in ALL 4 cardinal directions:

- North: decrease y until M < 0 or S > M + 2 or boundary
- South: increase y until M < 0 or S > M + 2 or boundary  
- East: increase x until M < 0 or S > M + 2 or boundary
- West: decrease x until M < 0 or S > M + 2 or boundary

Track the minimum x, maximum x, minimum y, maximum y of all expanded cells.

### Step 4: Form Bounding Box

- Create a single rectangle from (min_x, min_y) to (max_x, max_y)
- This rectangle should cover all the expanded cells

### Step 5: Edge Expansion

For each of the 4 edges, try expanding outward by 20, 40, 60, 80, 100 units:

- Compute score delta using grid prefix sums
- If delta > 0 and perimeter still <= 400,000, keep the expansion
- Greedily expand each edge in the best direction

### Step 6: Multiple Restarts

- Run 25 restarts with different random seeds
- Each restart: 
  * Randomly perturb top cell selection (±50 units to coordinates)
  * Build bounding box from perturbed seeds
  * Apply edge expansions

### Step 7: Validation

- Output: m (number of vertices = 4), then 4 vertices
- Ensure all coordinates in [0, 100000]
- Ensure perimeter <= 400,000
- Rectangle by definition has no self-intersection

## Key Success Factors

- One large rectangle > multiple tiny ones (simpler = more robust)
- Edge expansion adds coverage without violating constraints
- 25 restarts ensure good exploration
- Grid-based scoring enables fast, efficient search
