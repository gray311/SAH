---
name: hadamard-multi-strategy-optimizer
description: Specialized skill for n=29 Hadamard optimization using multiple strategies.
---

Hadamard Optimization for n=29.
Problem: Maximize |det(H)| for 29x29 +/-1 matrix.
Facts: n=29==3 mod 4, use Paley with residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.

Strategy A: SA T=3.0, cool=0.997, 25k iters. DO NOT undo flips.
Strategy B: Greedy - try all neighbors, pick best.
Strategy C: Random - flip 3-8 positions, accept if better.

Workflow: 1) Call analyze_paley_params. 2) Build Paley base. 3) Run all 3 strategies. 4) Pick best. 5) Probe. 6) Evaluate.
Use numpy.linalg.det. Time < 180s per eval. Target: > 0.545692.
