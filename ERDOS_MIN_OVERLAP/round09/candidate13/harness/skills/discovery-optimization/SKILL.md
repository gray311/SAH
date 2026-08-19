---
name: discovery-optimization
description: "Hyperparameter tuning for Erdos optimizer with fixed core structure."
---

# Erdos Minimum Overlap - Structured Initialization

## Problem
Minimize max_k integral h(x)(1 - h(x+k)) dx for h: [0,2]->[0,1] with integral(h)=1.

## Why Structured Constructions Work
The Erdos problem has known good constructions from combinatorial design theory.
Random initialization often misses these structured optima.

## Use construct_structured_init()
Call this tool FIRST to get 3-4 diverse, mathematically principled initializations:

### Types of Constructions:
1. **bimodal_tight**: Two narrow peaks at positions 1/4 and 3/4 with equal mass
2. **triangular_3step**: Linear ramps creating 3-level step function
3. **periodic_2**: Alternating pattern with period 1 (high on [0,0.5], low on [0.5,1])
4. **Golomb_5**: Construction inspired by Golomb ruler optimal spacing

### Optimization Workflow:
1. Generate 3-4 constructions from construct_structured_init()
2. For each, run optimization with:
   - Phase 1: 15000 steps, lr=0.02, penalty=5000
   - Phase 2: 20000 steps, lr=0.003, penalty=15000
3. Extract final h and compute c5_bound
4. Use probe_solution to rank candidates
5. Evaluate top 2 with evaluate_solution

## Key Principles
- Use structure, not randomness, for initialization
- Intensity of peaks should be balanced for integral=1 constraint
- Periodicity in the domain [0,2] matters for the correlation integral
- Save best program across iterations
