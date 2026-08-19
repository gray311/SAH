---
name: rectangle-search-playbook
description: Brute-force small axis-aligned rectangles around mackerels, expand successful ones, combine multiple rectangles.
---

# Rectangle Search Playbook for Fish Capture Optimization

## Core Strategy
- The optimal solution likely uses small, tight rectangles around dense mackerel clusters
- Avoid large rectangles that capture many sardines

## Step 1: Try Small Rectangles (1x1 to 3x3)
For each mackerel position (mx, my):
- Try rectangles with bottom-left corners offset by -size+1 to +size in each direction
- For each candidate, use count_rect tool to get (M, S)
- Score = M - S + 1 (only consider M >= S)
- Track the best rectangle found

## Step 2: Expand Best Rectangles
For each promising rectangle (M >= S):
- Try expanding right by 1 unit: x2_new = x2 + 1
- Try expanding left by 1 unit: x1_new = x1 - 1
- Try expanding up by 1 unit: y2_new = y2 + 1
- Try expanding down by 1 unit: y1_new = y1 - 1
- Use count_rect to score each expansion
- Keep expansions that improve score

## Step 3: Combine Multiple Rectangles
- If you found 2+ non-overlapping rectangles with good scores
- Try combining them into one polygon
- Total score = sum of individual scores

## Step 4: Fallback Large Rectangle
- If no small rectangle beats the seed
- Sample 100 random points in [0, 100000]
- For each, try rectangles of size up to 50x50
- Pick the best one

## Step 5: Output Valid Polygon
- Convert rectangle(s) to polygon vertices
- Ensure: 4 <= vertices <= 1000, perimeter <= 400,000, coords in [0, 100000]
- Output in format: m then m lines of "x y"

## Key Success Factors
- Small rectangles = fewer sardines captured
- Focus on mackerel-rich regions first
- Use count_rect for fast scoring (O(log N) via KD-tree)
- Limit total search time to < 2.0 seconds
