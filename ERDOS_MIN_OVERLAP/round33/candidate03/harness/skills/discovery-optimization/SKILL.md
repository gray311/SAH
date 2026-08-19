---
name: discovery-optimization
description: "Generate step functions from combinatorial templates, screen with probe_solution, evaluate promising candidates."
---

# Step Function Construction for Erdos C5

## Core Strategy: Direct Construction, Not Optimization

Do NOT use continuous latent-space optimization (too slow).
Instead, construct step functions directly from known combinatorial patterns.

## Template Library

### Template A: Uniform Partition
Divide [0,2] into N equal intervals, assign values 0/1 to each.
Adjust to satisfy integral(h)=1.

### Template B: Bipartite (Single Threshold)
h(x) = 1 if x < a, else 0.
Choose a to satisfy integral(h)=1 (a=0.5 for domain [0,2]).
Vary a slightly to explore.

### Template C: Tripartite (Two Thresholds)
h(x) = 1 if x < a or x > b, else 0.
Or: h(x) = 1 if a < x < b, else 0.
Tune a, b to satisfy integral(h)=1.

### Template D: Golomb Ruler
Place narrow peaks at positions 0, d, 2d, 3d...
Each peak has width w, height 1.
Total integral = (number_of_peaks) * w = 1.

### Template E: Peak Pattern
Place n peaks of width w at positions [x1, x2, ..., xn].
Each peak height = 1, width = w.
Total integral = n * w = 1, so w = 1/n.

## Construction & Screening Pipeline

1. CHOOSE a template and parameters.
2. CONSTRUCT the step function h (discrete array).
3. CALL probe_solution to get approximate c5_bound (cheap, 500 intervals).
4. If c5_bound < 0.382, CALL evaluate_solution for full score.
5. If combined_score > 1.0, finish.
6. Otherwise, try different template/parameters.

## Key Rules
- ALWAYS construct step functions directly from templates
- NEVER use continuous latent optimization
- PROBE before EVALUATE (use probe budget wisely)
- Try multiple templates: bipartite, tripartite, golomb, peaks
