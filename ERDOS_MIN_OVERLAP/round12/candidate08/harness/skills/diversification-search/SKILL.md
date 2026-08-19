---
name: diversification-search
description: For Erdos minimum overlap, the optimizer gets stuck in local optima. Use diverse step function constructions. Don't tune hyperparameters - try completely different initialization patterns.
---

# Diversification Search for Erdos Minimum Overlap

## Why Diversity Matters
The seed optimizer uses gradient descent with 12 initialization patterns, but this is still a local search.
To find the global optimum, you need to try fundamentally DIFFERENT step function constructions.

## Concrete Constructions to Try (edit _get_best_initialization):

### 1. Bimodal Constructions
h(x) = sigmoid(A * exp(-((x-a)/bw1)^2) + B * exp(-((x-b)/bw2)^2))
Vary: a, b, bw1, bw2 in [0.1, 0.9]
Best when: C5 bound requires separation of mass

### 2. Multi-level Step Functions
Divide [0,2] into 3-4 regions, assign different heights
Example: h(x) = [0.2 if x<0.5, 0.8 if 0.5<=x<1.0, 0.2 if x>=1.0]
Scale to satisfy integral(h)=1

### 3. Golomb Ruler Inspired
Use optimal spacing marks: [0, 0.25, 0.625, 0.9375, 1.0]
Construct Gaussian-like peaks at these marks
Best when: Minimizing overlap between h and h shifted by k

### 4. Optimal Transport Inspired
For target measure with 3 peaks at positions p1, p2, p3
Construct h(x) = 1 / (1 + exp(-lambda(x-p_i))) for regions

### 5. Wave Combinations
h(x) = sigmoid(a*sin(2*pi*x) + b*sin(4*pi*x) + c*cos(2*pi*x) + d)
Vary coefficients to create asymmetric patterns

## Screening Strategy
1. Generate 5-10 diverse constructions
2. Use probe_solution to quickly check integral constraint and c5_bound
3. Keep those with integral close to 1 and lowest c5_bound
4. Full evaluate only on top 2-3

## When to Stop Diversity Search
After using ~15 probes and ~5 full evaluations:
- If best score > 1.0: SUCCESS
- If stuck: Try replacing optimizer with coordinate ascent or greedy construction
