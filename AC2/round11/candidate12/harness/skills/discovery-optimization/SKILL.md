---
name: discovery-optimization
description: "Iterative hill-climbing optimization: Mutate one parameter at a time, evaluate, continue on improvement. Start from proven seed patterns, add complexity gradually. Avoid radical redesigns."
---

# Iterative Hill-Climbing for C₂ Optimization

## Core Principle
Start from the 13 proven seed patterns. Make small, targeted mutations. Evaluate. Repeat on improvements.

## Phase 1: Initialize (iterations 1-2)
1. Pick pattern 6 (four-level: heights 0.70, 1.30, 1.70, 1.00) OR pattern 11 (pyramid)
2. Document its current heights and boundary positions

## Phase 2: Iterative Mutation (iterations 3-30)
For EACH evaluation:
- MUTATION A (height adjustment): Pick one height value and change by +0.05, +0.10, -0.05, or -0.10
- MUTATION B (boundary shift): Pick one boundary and shift by +2, +3, -2, or -3 intervals (num_intervals=450)
- MUTATION C (peak split): If a wide plateau exists, split it into two levels with a small gap

Rules:
- Change ONLY ONE parameter per edit
- Never create patterns with >5 levels in one step
- If C₂ improves: apply another small mutation to SAME pattern next
- If C₂ worsens: try a different mutation on SAME pattern (don't switch patterns yet)
- After 3 failed attempts on a pattern: pick a new pattern

## Phase 3: Escalation (only after 10+ evals on one pattern)
If stuck with high C₂:
- Split a plateau into 2-3 smaller levels
- Introduce asymmetry in a symmetric pattern
- Only then try completely new architectural features

## Key: Small steps. One change at a time. Learn from each evaluation before moving on.
