---
name: discovery-optimization
description: "Coarse binary step function optimization for Erdos minimum overlap using extreme hyperparameters."
---

# Erdős C5 - Coarse Binary Step Functions

## Key Insight
The optimal solution is likely a SIMPLE BINARY step function (values 0 or 1 only), NOT a smooth sigmoid curve. The seed program's 800 intervals and sigmoid smoothing prevents finding such solutions.

## Strategy: Coarse, Extreme
1. Use few intervals: 100-200 (not 800) - this creates larger steps
2. Extreme penalties: 20000-50000 to enforce integral=1 hard
3. Binary initialization: Create explicit step patterns
4. Coarse patterns to try:
   - Two narrow peaks at positions 0.25, 0.75
   - One peak at 0.5
   - Three-level patterns with jumps

## Workflow
1. Call generate_binary_constructions() with different interval counts
2. For each, run 2-3 hyperparameter variations
3. Probe to rank, evaluate top 2

## Patterns that work for step functions:
- Bimodal: high on [0.2-0.3] and [0.7-0.8], zero elsewhere
- Central: high on [0.35-0.65], zero elsewhere
- Tri-modal: three narrow peaks at 1/6, 1/2, 5/6
