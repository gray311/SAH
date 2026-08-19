---
name: corridor-search-method
description: Multi-cluster corridor strategy finds disjoint clusters and connects them profitably.
---

# Multi-Cluster Corridor Search

## Core Idea
Connect isolated high-density mackerel regions if corridor has enough mackerels.

## Algorithm
1. Build 200x200 grid with 500-unit cells
2. Score cells as mackerels - sardines
3. Find top 20, group into super-clusters
4. For each pair of top 10 clusters, test corridor connection
   net_score = mackerels - sardines - 0.001*2*distance
5. Keep if net_score > 0.1
6. Hill climb with +/- 5, +/- 10, +/- 15 steps
7. Run 3 restarts, keep best

## Why This Works
Single-cluster approach misses multiple cluster opportunities.
