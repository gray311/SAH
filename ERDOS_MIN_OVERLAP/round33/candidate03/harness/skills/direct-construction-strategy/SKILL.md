---
name: direct-construction-strategy
description: Build step functions from combinatorial templates, screen with probe, evaluate best.
---

# Direct Construction Strategy for Erdos C5

## Core Principle
Build step functions directly from combinatorial patterns. Do NOT use continuous latent optimization.

## Construction Templates

### Bipartite (Single Threshold)
h(x) = 1 if x < a, else 0
For integral(h)=1 on [0,2]: a = 0.5

### Tripartite (Two Thresholds)
Option 1: h(x) = 1 if x < a or x > b
Option 2: h(x) = 1 if a < x < b
Tune a, b to explore different structures.

### Golomb Ruler
Narrow peaks at positions 0, d, 2d, 3d...
Each peak has width w, total integral = n_peaks * w = 1.

### Peak Pattern
Place n peaks of equal width w = 1/n at positions x1, x2, ..., xn.

## Workflow

1. CHOOSE a template (bipartite, tripartite, golomb, peaks).
2. CALL step_function_generator with template and parameters.
3. CALL probe_solution on the generated step function.
4. If c5_bound < 0.382, CALL evaluate_solution.
5. If combined_score > 1.0, finish.
6. Otherwise, try a different template/parameters.

## Key Rules
- ALWAYS use step_function_generator (not latent optimization)
- PROBE before EVALUATE
- Try multiple templates
- Keep candidates with c5_bound < 0.382
