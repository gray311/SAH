---
name: discovery-optimization
description: "Combinatorial step function search for Erdos minimum overlap optimization."
---

# Erdos Minimum Overlap - Combinatorial Search Strategy

## Problem
Minimize max_k integral h(x)(1 - h(x+k)) dx subject to integral(h)=1 and h in [0,1].

## Why Combinatorial Search Works
The seed optimizer uses gradient descent on a latent space, which struggles with step function landscapes.
Instead, generate candidate step functions DIRECTLY (as binary/multistep functions) and search over their structure.

## Strategy

### Phase 1: Generate Structured Step Functions
Generate step functions with specific mathematical structures:
- Single/multiple peaks of fixed width
- Periodic patterns (2-period, 3-period, etc.)
- Golomb ruler-inspired placements
- Triangular/dual-peak configurations

### Phase 2: Screen with Probe
Use probe_solution to quickly rank candidates. Reject those with integral != 1 or c5_bound > 0.381.

### Phase 3: Full Evaluation
Evaluate top 5-10 candidates with evaluate_solution.

### Phase 4: Structural Refinement
For promising candidates:
- Merge adjacent regions
- Split wide regions into narrower ones
- Shift peaks to reduce overlap
- Try different peak placements (0.2-0.8 range)

### Key Insight
The optimal step function likely has a simple STRUCTURE (e.g., two peaks at specific locations). Find that structure through combinatorial search, not gradient descent.
