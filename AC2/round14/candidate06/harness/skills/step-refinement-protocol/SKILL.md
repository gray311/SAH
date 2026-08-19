---
name: step-refinement-protocol
description: Focused refinement of step-function architectures through systematic mutation, probing, and evaluation.
---

# Step-Function Refinement Protocol for C₂ Maximization

## Core Strategy

The current step-function designs are close to optimal. Break the record through PRECISE, mathematically-informed mutations, not wild exploration.

## The Loop (Repeat until improvement or exhaustion)

1. **Analyze**: Call analyze_convolution on the current best
2. **Mutate**: Generate ONE variant per mutation type (peak adjustment, width refinement, asymmetry, bump addition)
3. **Probe**: Call probe_solution for each variant to rank them
4. **Evaluate**: Call evaluate_solution on top 2-3 probe-ranked variants
5. **Iterate**: Use the best result as your new starting point

## Mutation Types (in order of priority)

### 1. Peak Height Optimization
- Increase central peak by 0.01-0.03, decrease sides by 0.01-0.02
- Expected effect: Adjusts L₂/∞ balance

### 2. Width Refinement  
- Expand high plateau by 2-5%, contract side regions by 2-5%
- Expected effect: Spreads convolution energy more evenly

### 3. Asymmetric Enhancement
- Make left and right steps slightly different (1.45 vs 1.40)
- Expected effect: Breaks symmetry, reduces interference peaks

### 4. Small Bump Addition
- Add bump (height 0.05-0.10, width 0.02n) in a low region
- Expected effect: Fills valleys in convolution, improves L₂

## Key Rules

- **SMALL mutations only**: heights ±0.01-0.05, widths ±2-5%
- **Probe before evaluate**: Use all 30 probes before spending evals
- **One variant per type**: Don't generate 10 variants of the same mutation
- **Stick with step functions**: Don't switch to smooth functions mid-process
- **Document mutations**: Note what you changed in the finish summary
