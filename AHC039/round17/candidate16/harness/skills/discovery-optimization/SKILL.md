---
name: discovery-optimization
description: "Axis-aligned rectangle brute-force search. Try all small rectangles around mackerels, expand successful ones, combine multiple rectangles."
---

# Rectangle Search Strategy for Polygon Optimization

## Problem Understanding
- We need axis-aligned polygons (edges parallel to x or y axes)
- Score = (mackerels inside) - (sardines inside) + 1
- Maximum 1000 vertices, perimeter <= 400,000

## Strategy: Small Rectangle Brute Force

### Phase 1: Try 1x1, 1x2, 2x1, 2x2 Rectangles
For each mackerel position (x, y):
- Try rectangles with bottom-left corners at (x, y), (x-1, y), (x, y-1), (x-1, y-1)
- For each rectangle, count fish inside using KD-tree (O(log N) per rectangle)
- Keep rectangles where M >= S

### Phase 2: Expand Successful Rectangles
For each rectangle with score > 0:
- Try expanding right by 1 unit
- Try expanding left by 1 unit  
- Try expanding up by 1 unit
- Try expanding down by 1 unit
- Keep expansions that improve score

### Phase 3: Combine Multiple Rectangles
- Try pairing non-overlapping rectangles
- Total score = sum of individual scores
- Convert union to polygon vertices

### Phase 4: Fallback Large Rectangle
- If no small rectangle beats seed, sample 100 random points
- For each, try rectangle of size up to 100x100
- Pick best

### Phase 5: Output
- Ensure valid polygon format (4-1000 vertices)
- Integer coordinates in [0, 100000]
- Perimeter <= 400,000

## C++ Implementation Notes
- Use KD-tree for O(log N) rectangle counting
- Prioritize small rectangles (most likely to be optimal)
- Total evaluations < 2.0 seconds
