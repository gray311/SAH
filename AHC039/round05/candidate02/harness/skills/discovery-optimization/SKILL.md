---
name: discovery-optimization
description: "Build orthogonal polygons anchored to actual fish coordinates using analyze_fish_layout analysis."
---

# C++ Polygon Construction Strategy

## Overview
The task wants an orthogonal polygon maximizing (mackerels - sardines + 1).
Random search is ineffective. Use data-driven coordinate anchors.

## Step 1: Analysis (analyze_fish_layout)
- Call ONCE at the beginning
- Study the returned boxes: each has min_x, max_x, min_y, max_y
- These boxes enclose actual mackerels from the sample - excellent starting shapes!
- Note the perimeter estimates - ensure they stay ≤400000

## Step 2: Generate Candidates (in C++)
From each box [x1,x2]×[y1,y2]:
- Base polygon: vertices (x1,y1)→(x2,y1)→(x2,y2)→(x1,y2)
- Perimeter = 2*(x2-x1 + y2-y1) - must be ≤400000
- Try expanding: [x1-5,x2+5]×[y1-5,y2+5] to catch more mackerels

## Step 3: Multi-box strategies
- Combine left/right boxes horizontally: creates larger L-shape
- Check perimeter constraint when combining
- Consider vertical splits too

## Step 4: Evaluation workflow
- Use probe_solution for quick comparison of multiple candidates
- Each probe costs nothing - exhaustively test variants
- Only call evaluate_solution for the top 2-3 candidates per iteration
- Keep track of best score

## Step 5: Implementation tips
- Use fast coordinate hashing to count fish in O(1) per polygon
- Build a KD-tree or hash map of fish positions for O(log n) range queries
- Precompute all candidate boxes, then search within a tight time budget
