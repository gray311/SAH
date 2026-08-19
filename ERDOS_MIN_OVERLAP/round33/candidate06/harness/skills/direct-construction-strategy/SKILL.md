---
name: direct-construction-strategy
description: Construct step functions directly from mathematical families. Don't analyze and perturb - create better solutions from scratch.
---

# Direct Construction for Erdos C5

## Core Principle
Optimal solutions are simple step functions. Construct candidates directly instead of analyzing and mutating the current solution.

## Strategy 1: Threshold Function
- Single step at position p: h(x)=1 for x<p, 0 otherwise
- Scale to integral=1: h(x)=1/p for x<p
- Try p in [0.3, 1.7] to explore different cutoffs

## Strategy 2: Two-Threshold (Plateau)
- High on [0,a] and [b,2], low on [a,b]
- Scale to integral=1
- Try different plateau widths and positions

## Strategy 3: Symmetric
- Symmetric around x=1.0
- h(x)=1 on [0,a] and [2-a,2]
- Try different half-widths a in [0.2, 0.8]

## Strategy 4: Multi-Peak
- Multiple narrow peaks separated by zeros
- Good for reducing overlap at specific shifts
- Try 2-3 peaks at strategic positions

## Workflow
1. Call construct_step_function with different strategies
2. Probe each candidate
3. Evaluate the best
4. Refine promising candidates

## Rules
- Always use construct_step_function for complete programs
- Focus on direct construction, not analysis-based mutation
- Use probe_solution to screen before full evaluation
