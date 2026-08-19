---
name: discovery-optimization
description: "Fast rectangle-based polygon search around mackerel clusters with limited random expansion and minimal hill climbing."
---

# Fast Rectangle-Based Polygon Search

## Core Strategy
Instead of complex grid analysis, directly construct simple axis-aligned rectangles around mackerel clusters.

## Step 1: Cluster Detection
- Parse input to find all mackerel coordinates
- Group mackerels by proximity (within 5000 units)

## Step 2: Rectangle Generation
- For each cluster, pick a central mackerel
- Create rectangle by expanding ±R where R is random (100-500)
- Ensure: 4 vertices, all coords in [0,100000], no self-intersection

## Step 3: Limited Refinement
- Try 3-5 rectangles per run
- For each, optionally try edge shifts ±10, ±20
- Validate perimeter <= 400,000

## Step 4: Output Best
- Return single best valid polygon
- Prioritize speed over exhaustive search
