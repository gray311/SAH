---
name: step-mutation-playbook
description: Mutate the 12 seed step-function patterns with height tweaks, position shifts, and novel constructions. Always probe before full eval.
---

# Step-Function Mutation Playbook for C2 Optimization

## Strategy Overview
The seed has 12 step patterns. Mutate them with THREE OPERATIONS, always probe first.

## Operation 1: Height Scaling (Reliable)
- Multiply ALL heights by 1.05-1.20
- Example: pattern 3 heights (0.90, 1.90, 0.90) -> (1.00, 2.10, 1.00)
- Why: Adjusts peak-to-base ratio for better L2/inf

## Operation 2: Position Shifting (High Impact)
- Shift all intervals by +/- 5% of total width
- Pattern 0 (0.25-0.75) -> (0.20-0.70) or (0.30-0.80)
- Why: Changes convolution support region

## Operation 3: Novel Construction (Creative)
- Double peaks: two high regions separated by low region
- Plateau+spike: wide base (1.0) with narrow high peak (2.5-3.0)
- Asymmetric: left heights != right heights
- Why: May escape local optimum by new architecture

## Probing-First Workflow (MUST FOLLOW)
1. Generate 3-5 mutations from current best
2. Call probe_solution (compute_c2_coarse tool) on ALL variants
3. Rank by c2_approx, skip probe < 1.0
4. Call evaluate_solution on TOP 1-2 only
5. If neither beats record: try different operation type

## Phase Guidelines
- Iterations 1-15: Diverse operations (try all 3 types)
- Iterations 16-30: Fine-tune best architecture with small changes
- If stuck at iteration 10+: switch to novel construction
