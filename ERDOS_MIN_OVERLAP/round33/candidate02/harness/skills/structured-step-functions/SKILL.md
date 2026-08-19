---
name: structured-step-functions
description: Generate structured step functions (bipartite, multi-peak, Golomb) instead of random latents. Normalize to integral=1. Use probe to screen.
---

# Structured Step Function Strategy for Erdos C5

## Why Random Latents Fail

The seed program uses random latent vectors passed through sigmoid.
This produces smooth, non-structured functions that don't minimize overlap.

## Better Approach: Combinatorial Step Functions

Step functions with specific structures may achieve lower C5:

### 1. Bipartite Functions
h(x) = 1 for x < 0.5, 0 otherwise
- Simple, symmetric
- Integral = 1 by construction
- May not be optimal but good baseline

### 2. Multi-Peak Functions
Create 2-4 narrow peaks positioned to minimize overlap
- Equal mass per peak ensures integral = 1
- Peak positions matter: space them to reduce h(x)(1-h(x+k))

### 3. Golomb Ruler-like
Sparse marks at positions like [0, 0.4, 0.8, 1.2, 1.6]
- These positions are known to minimize pairwise distances
- May reduce overlap for small k values

## Workflow

1. Generate candidates with step_function_generator for each pattern
2. Call probe_solution on each
3. Keep candidates with c5_bound < 0.378
4. Evaluate best candidates fully
5. If no improvement, vary parameters (num_peaks, peak_width, threshold)

## Key Insight

Combinatorial structures may outperform random initialization for this problem.
Focus on step functions, not smooth sigmoid outputs.
