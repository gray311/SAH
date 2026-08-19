---
name: geometric-refinement-playbook
description: A step-by-step method for refining axis-aligned polygons to maximize mackerel capture while avoiding sardines. Uses probe-driven iteration and bounding-box strategies.
---

# Geometric Refinement Playbook for Fish Packing

## Core Principle
Start with a simple polygon (bounding box), then iteratively refine by cutting off low-value corners and expanding high-value regions.

## Step 1: Initial Construction
1. Compute the bounding box of all mackerels.
2. If perimeter ≤ 400,000, use this as initial polygon.
3. If too large, find a subset of dense mackerel regions.

## Step 2: Evaluate Baseline
Use probe_solution to score the initial polygon on subsampled data.

## Step 3: Corner Analysis
For each corner of the polygon:
1. Check if it contains sardines but few mackerels.
2. If so, try cutting the corner inward.
3. Probe the modified polygon to compare scores.

## Step 4: Expansion Opportunities
1. Find regions adjacent to the polygon with high mackerel density.
2. Try extending the polygon into these regions (staying within perimeter budget).
3. Probe each extension variant.

## Step 5: Iteration
1. After each modification, use probe_solution to rank 3-5 variants.
2. Confirm top 1-2 with evaluate_solution.
3. Keep the best, repeat.

## Tips
- Always stay within vertex count (≤ 1000) and perimeter (≤ 400,000) constraints.
- Use C++ KD-tree structures if available for fast point-in-polygon queries.
- When time is tight, use simpler constructions (single rectangle, L-shape).
- Probe before full evaluation: 30 probes = many quick comparisons at zero eval cost.
