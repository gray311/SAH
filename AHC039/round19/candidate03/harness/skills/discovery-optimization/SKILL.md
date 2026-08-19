---
name: discovery-optimization
description: "Geometric square optimization for fish capture. Parse fish coordinates, target each mackerel with a 400x400 square, use binary search to find optimal half-width, count fish inside squares, output top 3 polygons as 4-vertex axis-aligned rectangles."
---

# Geometric Square Optimization for Fish Capture

## Core Strategy

Instead of complex grid-based corridor expansion, directly target individual mackerels with optimal squares.

## Step 1: Parse Fish Coordinates

- Read N mackerels and N sardines from input files or program
- Store in separate vectors with (x, y) coordinates
- Sort both vectors by (x, y)

## Step 2: Build Candidate Squares

For each mackerel (m_i at position P_i):

- Consider a square with center P_i and side length L
- Start with L = 400 (400x400 square)
- This is a reasonable target size

## Step 3: Binary Search for Optimal Size

For each candidate square:

- Perform binary search on half-width h in [0, 250]
- For each half-width:
  - Define square boundaries: [cx-h, cx+h] x [cy-h, cy+h]
  - Count mackerels and sardines inside (inclusive of edges)
  - Calculate score = mackerels_in_square - sardines_in_square + 1
- Keep the half-width that maximizes this score

## Step 4: Select Top Squares

- Keep up to 3 squares with highest scores
- Tie-break by perimeter

## Step 5: Construct Polygons

For each selected square:

- If half-width h >= 250, clamp to 250
- Create 4 vertices:
  - (cx - h, cy - h)
  - (cx + h, cy + h)
  - (cx + h, cy - h)
  - (cx - h, cy + h)

## Step 6: Output

Output the best polygon:

m
x1 y1
x2 y2
x3 y3
x4 y4

where m = 4.

## Key Implementation Details

- Use binary search (O(log 250) ≈ 8 steps per square)
- For counting: iterate over all 2N = 10000 fish or use spatial grid
- With 5000 mackerels × 8 binary search steps × 10000 fish checks, this is 400M ops per eval
- Use spatial hashing (e.g., 100x100 grid, cell=1000) to speed up:
  - Build grid in O(2N)
  - For each square, sum grid cells intersected: O(grid_size) ≈ O(100) per binary search step
  - Total: 5000 × 8 × 100 = 4M ops per eval (acceptable)

## Time Complexity

- Naive: O(N × 5000 × 8) = 400M per evaluation (may be slow)
- With 100x100 grid: O(5000 × 8 × 100) = 4M per evaluation (acceptable)

## C++ Implementation

- Use 100x100 grid for O(1) fish counting
- For each mackerel, binary search on square size
- Build 3-5 candidate squares
- Output the best one
