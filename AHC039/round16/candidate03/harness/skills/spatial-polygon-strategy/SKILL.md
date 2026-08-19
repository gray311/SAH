---
name: spatial-polygon-strategy
description: Use spatial clustering on exact fish coordinates, build tight rectangles around dense mackerel groups, use KD-tree for efficient scoring, fewer but smarter restarts.
---

# Spatial Polygon Optimization Strategy

## Core Principles

1. **Precision over approximation**: Work with exact fish coordinates, not coarse grids
2. **Local optimization**: Build small, tight rectangles around dense clusters
3. **Efficient evaluation**: Use spatial indexing (KD-tree) for O(log N) scoring
4. **Strategic search**: Fewer, smarter restarts rather than many shallow ones

## Step-by-Step Method

### Step 1: Input Analysis
- Parse all fish coordinates from input
- Build spatial index (KD-tree or simple sorted structure)
- Compute density at key locations

### Step 2: Cluster Detection
- Use distance-based clustering (threshold ~1000-2000 pixels)
- Group nearby mackerels together
- For each cluster, compute bounding rectangle

### Step 3: Initial Rectangle Construction
- For each cluster, create minimal bounding rectangle
- Include all fish in cluster within rectangle bounds
- Compute exact score using spatial queries

### Step 4: Rectangle Refinement
- Try expanding edges by ±10, ±20, ±30 units
- Use spatial index to count fish in expanded rectangles
- Keep expansions that improve score (M increase > S increase)

### Step 5: Combination and Merging
- If clusters are close (distance < 1000), consider merging rectangles
- Union of adjacent rectangles may create better overall score
- Compute score for merged polygon

### Step 6: Hill Climbing
- For each polygon:
  * For each of 4 edges, try shifts ±10, ±20, ±30 units
  * Evaluate each variant using spatial queries
  * Keep best shift for each edge
- Repeat up to 50 iterations

### Step 7: Strategic Restarts
- Run 8-10 restarts with different seed selections
- Each restart focuses on a different region of the search space
- Track best polygon across all restarts

### Step 8: Validation and Output
- Ensure 4-1000 vertices
- Check perimeter ≤ 400,000
- Verify coordinates in [0, 100000]
- Output in correct format: vertex count followed by coordinates

## Key Success Factors

- Use exact coordinates, not grid approximations
- Leverage spatial indexing for fast evaluation
- Build tight rectangles around actual fish clusters
- Focus search on high-density mackerel regions
- Avoid large rectangles that capture many sardines
