---
name: union-rectangles-guide
description: Use union-of-rectangles to capture mackerel clusters. Build spatial histogram, generate bounding boxes, use probe_union_rects to guide rectangle adjustments (expand/shrink/merge/split), deep local search with 20-30 restarts.
---

# Union-of-Rectangles Strategy

## Core Idea
Construct the polygon as a union of axis-aligned rectangles to capture
mackerel-dense regions while excluding sardines. Use probe-guided local
search for efficient refinement.

## Step-by-Step Method

### Step 1: Spatial Histogram
- Build fine-grained histogram (1000x1000 or adaptive bins) over
  [0,100000]x[0,100000]
- Count mackerels (M) and sardines (S) per bin
- Compute density score = M - S
- Identify top regions with positive score

### Step 2: Bounding Box Generation
- For each top region, compute axis-aligned bounding box
- These boxes form initial candidate rectangles
- Ensure integer coordinates in [0, 100000]

### Step 3: Probe-Guided Local Search
For each candidate union-of-rectangles:
- EXPAND: For each rectangle, extend each side by +/-5, +/-10,
  +/-20, +/-50 units (if in bounds)
- SHRINK: Contract each side by same amounts to reduce sardine
  exposure
- MERGE: Combine adjacent/overlapping rectangles into one
- SPLIT: Divide large rectangles into smaller ones to avoid
  sardine-rich areas
- REMOVE: Eliminate rectangles with consistently negative contribution
- Use probe_union_rects to evaluate each change (cheap, fast)
- Repeat 5-8 refinement rounds

### Step 4: Multiple Restarts
- Run 20-30 restarts
- Each restart: random seed points -> bounding boxes -> refine
- Track best polygon

### Step 5: Validation and Output
- Convert union of rectangles to orthogonal polygon (vertex list)
- Ensure: 4 <= vertices <= 1000, integer coords, no self-intersection,
  perimeter <= 400,000
- Output: m vertices, then each coordinate pair

## Why This Works
- Fine-grained spatial analysis captures local distributions
- Union-of-rectangles naturally forms valid axis-aligned polygons
- Probe-based search enables rapid exploration without consuming
  evaluation budget
- Multiple restarts ensure diversity
