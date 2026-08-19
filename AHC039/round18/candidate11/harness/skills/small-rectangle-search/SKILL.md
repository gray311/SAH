---
name: small-rectangle-search
description: Focus on small tight rectangles around mackerel clusters, use cluster_probe for fast filtering, minimal hill climbing.
---

# Small Rectangle Search Strategy

## Core Idea
Instead of large corridors, enumerate small axis-aligned rectangles (10-150 units) around dense mackerel clusters.

## Step 1: Cluster Mackerels
- Read fish positions from program
- Group mackerels within 200 units of each other into clusters
- Each cluster becomes a candidate region center

## Step 2: Fast Probing with cluster_probe
- For each cluster, define candidate rectangle boundaries
- Call cluster_probe to get approximate mackerel/sardine count
- Skip regions with negative score

## Step 3: Build Small Rectangles
- For promising clusters, create rectangles with:
  * Width/height between 10 and 150 units
  * Centered on cluster centroid or covering cluster bounds
- Generate 3-5 variations per cluster

## Step 4: Minimal Hill Climbing
- For each candidate polygon:
  * Try edge shifts of ±10 units only
  * ONE refinement round
  * Keep best variant

## Step 5: Final Selection
- Pick top 3 polygons by approximate score
- Output the single best one

## Key Success Factors
- Small rectangles avoid sardine penalty edges
- Fast probing filters unpromising regions
- Minimal hill climbing saves time for more candidate generation
leverage the seed's KD-tree if available
