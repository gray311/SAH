---
name: discovery-optimization
description: "Math optimization with diverse initializations and adaptive strategies for non-convex objectives."
---

# Erdos Minimum Overlap Optimization

## Problem
Minimize max_k integral h(x)(1 - h(x+k)) dx for step function h: [0,2]->[0,1] with integral h = 1.
Current best: C5 <= 0.380923 (combined_score > 1.0 is success).

## Why Single Initialization Fails
The seed program uses one random Gaussian initialization. This often lands in poor local minima.

## Solution: Diverse Initializations + Smart Search

### Use init_diverse_construct()
Call this tool FIRST to get 3-5 diverse latent vectors:
- 'bimodal': Two concentrated regions (mass at positions a and b)
- 'uniform': Flat start with gradient descent to sculpt
- 'alternating': High-low pattern with specific period
- 'bimodal_offset': Bimodal but shifted to different region
- 'concentrated': Single concentrated region that spreads

### Optimization Workflow
1. Generate 3-5 initializations from init_diverse_construct()
2. For each, run ErdosOptimizer with:
   - Phase 1: 10000 steps, lr=0.01, penalty=1000
   - Phase 2: 10000 steps, lr=0.005, penalty=10000
3. Extract final h = sigmoid(latent) and compute c5_bound
4. Use probe_solution to rank candidates cheaply
5. Evaluate top 1-2 with evaluate_solution

### Key Design Principles
- Integral constraint must be exact: use moderate penalty (1000-10000), not 1M
- Adaptive learning: larger lr early for exploration, smaller late for refinement
- Diverse starts: different construction styles to avoid systematic bias
- Save best program across iterations

## Tool Guide
- init_diverse_construct: Returns dict with keys like 'bimodal', 'uniform', etc.
- edit_solution: Modify EVOLVE-BLOCK to add initialization selection and two-phase optimizer
- probe_solution: Quick score comparison before final eval
- evaluate_solution: True score; MAXIMIZE combined_score
- finish: End session when best score cannot be improved

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.38092303510845016)
- validity = 1.0 (integral exactly 1)
- Budget: 20 evaluations
