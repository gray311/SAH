---
name: rapid-prototype-strategy
description: Use analyze_h_structure for quick screening. Generate many coarse prototypes, screen with analytical c5, then run ONE expensive full eval on the best.
---

# Rapid Prototype Strategy

## Problem
Full optimization takes 59000+ steps. We have only 30 evals total.
Cannot train many candidates.

## Solution
Use analyze_h_structure tool to quickly prototype structures.
Each prototype takes ~3-5s and gives analytical c5 bound.

## Workflow
1. CALL analyze_h_structure(max_c5_threshold=0.375)
2. Check returned c5_bound:
   - If c5_bound < 0.375: PROMISING, proceed to evaluate_solution
   - If c5_bound >= 0.375: REJECT, try different structure
3. Before evaluate_solution, EDIT program for faster training:
   - num_intervals=400, num_steps=15000, penalty_strength=15, num_restarts=8
4. CALL evaluate_solution on the edited program
5. If no improvement, return to step 1 with different structure

## Why This Works
- analyze_h_structure is O(10 steps on 50 intervals) vs O(59000 steps on 800 intervals)
- Can screen 10+ structures in time for 1 full eval
- Find better initializations, not just hyperparameters
- Save eval budget for promising candidates only
