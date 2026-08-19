---
name: rectangle-search-playbook
description: Rectangle and union-of-rectangles search using KD-tree. Generate candidates, score with exact queries, refine edges.
---

# Rectangle Search Using KD-Tree

## Why This Works

The KD-tree provides O(log N) rectangle queries. Instead of grid approximations that lose precision, use exact counting.

## Method

### Step 1: Generate Candidate Rectangles
- Sample random corner pairs (x1,y1), (x2,y2)
- Constraint: x1≤x2, y1≤y2, perimeter=2*(width+height)≤400,000
- Generate 100-200 candidates per restart

### Step 2: Score with KD-Tree
- Query each rectangle: get (m, s) counts
- Score = m - s
- Track best rectangle

### Step 3: Union of Rectangles (Optional)
- Generate 2-4 rectangles
- Merge carefully, handling overlaps
- Use inclusion-exclusion for fish counts
- Can capture disjoint clusters

### Step 4: Edge Refinement
- For best rectangle, try edge shifts ±5, ±10, ±20, ±50
- Query each variant with KD-tree
- Keep improvements
- 2-3 refinement rounds

### Step 5: Random Polygon Variants
- Generate L-shapes, U-shapes from best rectangle
- Build by cutting/expanding rectangle
- Validate all constraints

### Step 6: Multiple Restarts
- 20-30 restarts with fresh random seeds
- Track global best across all

## Key Points
- NEVER use grid approximations - KD-tree is exact and fast
- Rectangle is the simplest valid polygon; master this first
- Unions enable capturing multiple clusters
- Edge refinement gets incremental gains
- Always validate constraints
