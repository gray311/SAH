---
name: discovery-optimization
description: "Optimize geometric heuristic programs for rectilinear polygon construction tasks.\nUse scan_horizontal_regions to find high-density mackerel zones, then build and probe\npolygon variants covering those zones. Evaluate only the best variants to conserve budget."
---

# Geometric Heuristic Optimization for Rectilinear Polygon Scoring

## Objective
Maximize: mackerels_in - sardines_in + 1

## Key Insight
The score is purely additive per fish. We need polygons covering regions where
mackerel density >> sardine density. The axis-aligned constraint simplifies
polygon construction but requires careful perimeter budgeting.

## Strategy

1. **Use scan_horizontal_regions first**
   - This tool returns horizontal y-bands with their mackerel/sardine counts
   - Look for bands where mackerel_count >> sardine_count
   - Note the y-range and width of each promising band

2. **Build polygon variants from bands**
   - Simple rectangle: just use one high-value band's y-range with appropriate x-extent
   - Merged regions: combine adjacent bands with the same x-overlap
   - Consider: left/right bounds should cover as many fish as possible
   - Keep perimeter under 400,000: for a rectangle, 2*(width+height) < 400,000

3. **Probe before evaluating**
   - Generate 3-5 variants per iteration
   - Probe each (fast, ~10s, no budget cost)
   - Compare probe scores to identify winners
   - Run full evaluation on top 1-2 variants only

4. **Perimeter budgeting**
   - Typical good polygon: 8-16 vertices (allowing some complexity)
   - If using multiple horizontal bands, sum their widths and heights
   - Stay under 400,000 total perimeter

5. **When to pivot**
   - If all probes score low, expand the polygon
   - If too many sardines, shrink toward mackerel clusters
   - Try vertical strips if horizontal bands are sparse

## Edits
Each iteration: completely rewrite the EVOLVE-BLOCK with your best variant.
Keep the same main function signature and output format.
The best-scoring program is retained automatically.
