---
name: structured-construction-playbook
description: Build step functions with specific structures (bipartite, multi-modal, sparse) that satisfy integral=1.
---

# Structured Step Function Construction

## Why Structure Matters
Random sigmoid-based functions don't naturally satisfy integral=1 and may have suboptimal correlation structure.
Piecewise constant step functions with few intervals are analytically tractable and may achieve better C5 bounds.

## Construction Guide

### Step 1: Choose a Structure
- **Bipartite**: Single threshold. h=1 on [0, t), h=0 on [t, 2]. Integral = t*1 = t, so set t=1.
  Example: h(x) = 1 for x < 1, h(x) = 0 for x >= 1.

- **Bimodal**: Two peaks. Total width of peaks = 1.
  Example: peaks at [0.3, 1.7] with widths [0.4, 0.4], gap = 1.2.
  h = 1 on [0.3, 0.7] and [1.3, 1.7], h = 0 elsewhere.

- **Trimodal**: Three peaks. Total width = 1.
  Example: peaks at [0.33, 1.0, 1.67] with widths [0.2, 0.3, 0.2], sum = 0.7, scale to 1.
  Or: three equal peaks of width 1/3 each.

- **Sparse**: Non-zero on very small total width (e.g., 0.3-0.5).
  Example: three narrow peaks of width 0.1 each at [0.5, 1.0, 1.5].

### Step 2: Ensure Integral = 1
For height=1 regions: sum of widths must equal 1.
For varying heights: sum of (height * width) must equal 1.

### Step 3: Use construct_step_function Tool
Call: construct_step_function(structure="bimodal", params={"peak_positions": [0.3, 1.7], "peak_widths": [0.2, 0.2]})

This tool returns a discretized h array with integral = 1.

### Step 4: Evaluate with probe
Use probe_solution to quickly screen candidates. Keep those with c5_bound < 0.375.

### Step 5: Full evaluation
Evaluate promising candidates. Target combined_score > 1.0.

## Key Insight
Simple structures (2-4 intervals) are easier to optimize and may outperform complex random functions.
Start with 2-3 interval structures, then refine.
