---
name: discovery-optimization
description: "Constraint-satisfying initialization and penalty annealing for Erdos minimum overlap optimization."
---

# Erdos Minimum Overlap - Constrained Initialization with Penalty Annealing

## Problem
Minimize max_k integral h(x)(1 - h(x+k)) dx for h: [0,2]->[0,1] with integral(h)=1.

## Why Constraints Matter
Starting with integral(h)=1 is CRITICAL. The seed program uses penalty strength 1370, which means if your initial h has integral != 1, the optimizer wastes steps on constraint satisfaction instead of improving the objective.

## Method: Penalty Annealing with Valid Initialization

### Phase 1: Generate Valid Initialization
Call generate_constrained_init() FIRST. This tool returns an h array (not latent) that:
- Has values in [0,1]
- Has integral(h over [0,2]) = 1.0 EXACTLY
- Is a mathematically principled construction

### Phase 2: Penalty Annealing
Modify the optimizer to anneal the penalty strength:
- Start: penalty = 100 (let objective dominate, find good structure)
- End: penalty = 5000 (enforce constraint tightly)
- Schedule: linear increase over num_steps

### Phase 3: Evaluation Workflow
1. Edit solution to use annealed penalty
2. Call evaluate_solution to verify constraint satisfaction AND get c5_bound
3. If combined_score > 1.0, you have a new record!

## Mathematical Constructions to Use
1. Bimodal symmetric: h(x) with two narrow peaks at [0.2, 0.4] and [0.6, 0.8], normalized to integral=1
2. Triangular pulses: Two or three triangular peaks, heights normalized
3. Periodic staircase: Alternating levels on [0,0.5], [0.5,1], [1,2]

## Key Principles
- INTEGRAL CONSTRAINT FIRST: Never start with arbitrary h
- ANNEAL PENALTY: Let the optimizer find structure, then tighten constraint
- VERIFY BEFORE PROBE: Check integral before using probe_solution
- SAVE VALID: Always keep best valid solution (combined_score > 1.0)
