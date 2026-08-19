---
name: discovery-optimization
description: "C5 bound optimization via combinatorial step function search.\nFocus on structured constructions with few breakpoints. Use construction_prober\nto internally test 50-200 designs before evaluation."
---

# C₅ Bound Optimization

Goal: Achieve combined_score > 1.0 by finding c5_bound < 0.38092303510845016

## The Problem

Minimize: max_k ∫_0^2 h(x)(1-h(x+k))dx
subject to: h:[0,2]→[0,1], ∫h=1

## Why We're Stuck

The seed's multi-restart Adam optimizer finds good local optima but gets trapped there.
It needs fundamentally different starting strategies or optimization approaches.

## Proven Strategies to Try

### Strategy 1: Coarse-to-Fine
- Use num_intervals=100, optimize briefly, then upgrade to 500, 800, 1000
- This escapes local optima by finding global structure first

### Strategy 2: Strategic Initializations
Replace seed's patterns with targeted constructions:
- Single step: h=1 on [0,1], h=0 elsewhere (need to adjust for integral=1)
- Double step: h=0.5 on [0,0.5] and [1.5,2], h=0 elsewhere
- Symmetric wave: sin-based patterns centered at x=1

### Strategy 3: Direct Construction
- Manually construct piecewise constant functions
- Use few breakpoints, optimize just those values
- Less flexible but can find high-quality solutions

## Execution Plan

1. Evaluate seed to establish baseline (~1 eval)
2. Try coarse discretization: num_intervals=100, simple optimizer (~1 eval)
3. Try strategic initialization: single/double step patterns (~1 eval)
4. Refine promising directions: increase intervals, tune hyperparameters
5. Once combined_score > 1.0, it's a record!

## Important

- **COMPLETE REWRITES ARE PREFERRED** for major strategy changes
- **Think in terms of mathematical strategies, not code patches**
- **Each evaluation is precious** (~30 total)
- **Constraints matter**: h∈[0,1], ∫h=1 over [0,2]
- **If error occurs, diagnose and fix specifically**
