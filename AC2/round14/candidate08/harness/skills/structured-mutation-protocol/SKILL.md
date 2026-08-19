---
name: structured-mutation-protocol
description: Systematic mutation based on mathematical insights for C₂ maximization.
---

# Structured Mutation Protocol for C₂ Maximization

## Core Principle

Don't make random edits. Use analyze_patterns to understand current structure, then apply MATH-MOTIVATED mutations.

## Step 1: Call analyze_patterns

This will parse your EVOLVE-BLOCK and return:
- Current heights, widths, positions
- Symmetry properties
- Concrete mutation proposals (asymmetric heights, non-uniform spacing, multi-scale, tapering)

## Step 2: Pick ONE mutation type to explore

Focus on the most promising proposal:
- If symmetric → try asymmetric heights (Type A)
- If uniform spacing → try non-uniform (Type B)
- Always consider multi-scale (Type C)
- Always consider tapering (Type D)

## Step 3: Generate ONE concrete implementation

Target ONE specific change:
- Asymmetric: change one height by +0.05, another by -0.03
- Non-uniform: change one interval fraction from 0.20 to 0.23
- Multi-scale: add small bump (height 0.15) inside largest existing bump
- Tapering: add ramp in last 5%: f[-5%:] *= linear_decay(0.8, 0.0)

## Step 4: Probe → Evaluate

1. Call probe_solution to check improvement
2. If probe > current best, call evaluate_solution
3. If evaluate improves, refine slightly; if not, try next mutation

## Step 5: If stuck

Call analyze_patterns again with different parameters, or try mutation types in different order.

Remember: Structured mutations beat random changes.
