---
name: discovery-optimization
description: "Sardine-avoidance via empty_region_probe. First scan to find sardine-free zones, then build simple rectangles that stay clear of sardines while reaching mackerels. Use 5-10 restarts and minimal refinement."
---

# Sardine-Avoidance Strategy with Empty Region Detection

## Core Innovation: Empty Region Probe

Instead of complex grid-based corridor expansion, first probe the input to find EMPTY REGIONS - areas with no sardines.

## Step 1: Empty Region Detection

- Parse all fish coordinates from input
- Sort sardines by x-coordinate into bins (e.g., 5000 bins of size 20)
- Identify x-ranges with NO sardines
- For each sardine, mark x-ranges it occupies
- Build a list of "sardine-free x-bands"

## Step 2: Mackerel Analysis

- Similarly, bin mackerels by x-coordinate
- Find x-ranges with high mackerel density
- Look for overlaps between mackerel-rich and sardine-free regions

## Step 3: Rectangle Construction

For each promising region, build a simple rectangle:
- Choose a row range (y1, y2) with no sardines
- Extend left/right to reach mackerels, stopping at sardine boundaries
- Ensure 4-1000 vertices, perimeter < 400,000
- Coordinates in [0, 100000]

## Step 4: Multiple Restarts

- Run 5-10 restarts with different random seeds
- Each restart: pick different sardine-free bands, build different rectangles
- No complex hill climbing - focus on quantity of diverse attempts

## Step 5: Validation

- Ensure polygon is valid: 4+ vertices, axis-aligned, no self-intersection
- Output best rectangle found

## C++ Implementation Notes

- Use simple array-based approach, no KD-tree overhead
- Pre-compute sardine x-bins at startup
- Rectangle perimeter = 2 * ((x2-x1) + (y2-y1))
- Total time per evaluation: < 2.0 seconds
- Focus on SPEED: simple binned analysis, no complex geometric structures
