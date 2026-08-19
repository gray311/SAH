---
name: sardine-free-rectangle-builder
description: Build rectangles in sardine-free regions. Use empty_region_probe to find sardine-free x-bands, then construct simple rectangles that maximize mackerel capture while avoiding sardines.
---

# Sardine-Free Rectangle Building

## Step 1: Get Empty Regions

Call empty_region_probe to get sardine-free x-bands.

## Step 2: Build Rectangles

For each sardine-free band (min_x, max_x):

- Pick a vertical span (y1, y2) of 100-500 pixels in [0, 100000]
- Rectangle vertices: (min_x, y1), (max_x, y1), (max_x, y2), (min_x, y2)
- This creates a simple 4-vertex axis-aligned rectangle

## Step 3: Multiple Candidates

Generate 5-10 rectangles:
- Different y-ranges for each
- Different subsets of sardine-free bands
- Try rectangles that are wider (more area) vs taller

## Step 4: Quick Validation

For each candidate:
- Check perimeter = 2*((max_x-min_x) + (y2-y1)) < 400,000
- Check vertex count = 4, coordinates in [0, 100000]
- Check no sardines in x-range (from empty_region_probe)

## Step 5: Output Best

Submit the rectangle with most mackerels (estimated from mackerel density in x-range)
