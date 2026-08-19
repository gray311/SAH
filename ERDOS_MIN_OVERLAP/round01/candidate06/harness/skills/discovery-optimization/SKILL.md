---
name: discovery-optimization
description: "Direct optimization over step function parameters for the Erdos minimum overlap problem, using internal bounded search instead of pure gradient descent."
---

# Direct Step Function Optimization for Erdos C5

## Problem
Find h: [0,2] -> [0,1] with integral(h) = 1 that minimizes max_k integral(h(x)(1-h(x+k)))dx.

## Strategy
The gradient-based approach struggles. Instead:
1. DIRECT OPTIMIZATION: Optimize h[i] in [0,1] directly for each interval
2. MULTIPLE STRATEGIES: Try uniform, alternating, random, and structured patterns
3. BOUNDED INTERNAL SEARCH: Within each evaluation, run several configurations and pick the best
4. EXPLICIT CONSTRUCTIONS: Consider step functions with alternating heights or specific patterns

## Key Changes from Seed
- Remove sigmoid relaxation; work directly with h values in [0,1]
- Replace gradient descent with a bounded internal optimization loop
- Try multiple initial configurations per evaluation
- Use a simpler optimization method (e.g., coordinate descent, golden section, or exhaustive grid search on reduced space)

## Implementation Tips
- Use numpy arrays directly (no JAX/transformed space)
- Clamp values to [0,1] explicitly
- Normalize to satisfy integral constraint after optimization
- Keep computation under 5-10 seconds per evaluation
- Save and compare multiple configurations, report best
