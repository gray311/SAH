---
name: fast-rectangle-strategy
description: Use simple rectangles around mackerel clusters instead of complex grid searches.
---

# Fast Rectangle Strategy for Fish Capture

## Why This Works
The seed program already finds good solutions using some strategy.
Our goal is to find slightly better polygons with less computation.

## Method

1. **Identify Mackerel Clusters**: Find groups of mackerels within 5000 units

2. **Generate Rectangles**: For each cluster center, create a rectangle by expanding ±100-500 units

3. **Limit Candidates**: Try only 3-5 rectangles per run (not 15-20 restarts)

4. **Minimal Refinement**: Optionally try edge shifts of ±10 or ±20 units

5. **Output Best**: Return the single best valid rectangle

## Advantages
- Much faster than grid-based corridor expansion
- Simpler code, less chance of bugs
- Focuses on tight mackerel clusters (maximizes mackerels, minimizes area = fewer sardines)

## Key Parameters
- Expansion range: 100-500 units
- Candidates per run: 3-5
- Edge shift refinement: ±10, ±20 units only
