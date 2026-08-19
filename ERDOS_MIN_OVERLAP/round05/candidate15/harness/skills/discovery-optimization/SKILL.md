---
name: discovery-optimization
description: "Optimize step function constructions for Erd\u0151s minimum overlap problem. Use structural search: vary discretization, try block/sine/triangle patterns, multi-restart strategies. Rank candidates cheaply with probe_solution, evaluate promising ones fully. Always maintain \u222bh=1 constraint."
---

# Erdős C5 Optimization Harness

Objective: Minimize max_k ∫ h(x)(1-h(x+k))dx for step function h: [0,2]→[0,1] with ∫h=1.
Score = 0.38092303510845016 / c5_bound; beat 0.999641 to improve.

## Search Strategy

The seed uses 800 intervals + Adam. To improve:
1. Try FEWER intervals (100-400) with stronger penalties - coarser step functions may suffice
2. Try MORE intervals (1000-2000) with adaptive learning rates - finer resolution captures better shapes
3. Modify _get_best_initialization: the 12 patterns work, but try new shapes:
   - Alternating blocks: h(x)=a for x in [0,a], 1-a for x in [a,2-a], a for x in [2-a,2]
   - Concentrated mass: put most h(x) near 1, rest near 0
   - Symmetric patterns around x=1
4. Adjust penalty_strength: too high (1370) may over-penalize, too low lets ∫h≠1

## Tools Workflow

1. edit_solution: Change ONE thing at a time - interval count, penalty, or initialization pattern
2. probe_solution: Fast check if ∫h≈1 and rough c5 score. If c5 > 0.4, likely not worth full eval
3. evaluate_solution: Only for promising variants (probe c5 < 0.38 or structured improvement)

## Concrete Ideas to Try

- Experiment 1: num_intervals=300, penalty_strength=2000 (coarser + stronger constraint)
- Experiment 2: Add a new initialization pattern: uniform block function [0,0.5],[0.5,1.5],[1.5,2]
- Experiment 3: Multi-start with 10 restarts, each with different random seeds
- Experiment 4: Try learning rate=0.01 instead of 0.0053
- Experiment 5: Reduce dx calculation impact by padding more conservatively

## Validation Checklist

Before each edit: Does ∫h=1 approximately? Is the edit a targeted diff? Is the change substantive?
After probe: Is c5 < 0.4? If not, skip full eval.
Success metric: combined_score > 0.999641 (c5 < 0.3809).
