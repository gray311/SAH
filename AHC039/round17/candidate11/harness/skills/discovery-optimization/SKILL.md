---
name: discovery-optimization
description: "Cluster-based local search. Build minimal rectangles from mackerel pairs, then locally refine edges via simple expansion/shrinkage. Fast, avoids complex structures."
---

# Cluster-Based Local Search Strategy

## Core Idea

Instead of complex grid analysis or multi-lobed structures, focus on simple rectangles around mackerel clusters with local edge refinement.

## Step-by-Step

### Step 1: Generate Seed Rectangles

- Pick 8-12 pairs of mackerels randomly
- For each pair, build minimal axis-aligned rectangle containing both
- Add padding of 100-200 units to each side for flexibility

### Step 2: Local Edge Search

For each seed rectangle (up to 8 vertices after padding):

- Current perimeter must be <= 400,000

- For each of 4 sides (left, right, top, bottom):
  * Try expanding outward by d in {50, 100, 200, 300, 500}
  * Try shrinking inward by d in {10, 20, 50, 100} (if still within bounds and non-negative width/height)
  * Evaluate each candidate
  * Keep best improvement

- Do 8-10 such rounds of improvement

### Step 3: Validation

- Ensure 4 <= vertices <= 1000
- Integer coordinates in [0, 100000]
- No self-intersection (axis-aligned rects are simple)
- Perimeter <= 400,000

### Step 4: Best Selection

- Track score for each candidate
- Output single best valid polygon

## Key Success Factors

- Simple rectangles are easier to validate and faster to compute
- Local search makes steady improvements without expensive lookahead
- Multiple seeds increase chance of finding good starting point
- Avoid complex structures that exceed time limit
