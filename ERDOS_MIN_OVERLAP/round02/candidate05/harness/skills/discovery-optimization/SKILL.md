---
name: discovery-optimization
description: "Multi-start optimization with probe-guided selection for non-convex mathematical problems."
---

# Erdos C5 Optimization - Multi-Start Strategy

## Problem
Minimize max_k integral h(x)(1 - h(x+k)) dx for h: [0,2]->[0,1] with integral h = 1.
Current best: C5 <= 0.380923.

## Why Single Initialization Fails
The seed program runs ONE optimization from ONE random Gaussian. This almost always finds the same local minimum (C5 approx 0.3809).

## The Winning Strategy: Multi-Start + Probe Selection

### Architecture
Instead of one long run, run MANY short runs, then pick the best:
1. Generate 5-10 diverse initializations
2. Run 5000-step optimization on each
3. Probe top 3 (fast, no eval budget cost)
4. Full optimize best probe with 20000+ steps
5. Evaluate

### Initialization Patterns
These work well for C5 optimization:
- Bimodal: h = sigmoid(k * x) or h = sigmoid(-k * (x - 1))
  - Concentrates mass at one end
  - Use k = 5-15 for sharp mass
- Uniform Start + Shape: h = sigmoid(small + noise)
  - Let gradient descent sculpt from flat start
- Alternating: h = (sin(2*pi*x) + 2)/3
  - Wave patterns that spread mass evenly
- Shifted Concentration: h = sigmoid(k * (x - offset))
  - Try different offsets (0.1, 0.3, 0.5, 0.7, 0.9, 1.1)

### Parameter Tuning
- num_intervals: 800 (seed value, do not change)
- Probe phase steps: 5000 per candidate (fast enough to do 5-10)
- Final phase steps: 20000-30000 (enough to refine)
- penalty_strength: 1000-2000 (moderate, allows exploration)
- learning_rate: Start 0.01, decay to 0.001 over iterations
- Early stopping: If loss plateaus, start fresh with different pattern

### Implementation Steps
1. Add a function generate_variants() that returns list of latent arrays
2. For each variant: short optimize -> probe result
3. Rank by probe score
4. Full optimize top 1-2
5. Evaluate and finish

### Why This Works
- Diversity: 10+ starting points hit different regions of parameter space
- Efficiency: Short runs fit in eval budget
- Probe guidance: Avoid wasting full evals on bad starts
- Proven patterns: Mathematical constructions known to work for overlap problems
