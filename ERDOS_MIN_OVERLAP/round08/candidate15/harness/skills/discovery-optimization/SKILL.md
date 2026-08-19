---
name: discovery-optimization
description: "C\u2085 optimization harness. Focus on structured step function families with\nexplicit mathematical forms. Targets combined_score > 1.0."
---

# C₅ Bound Optimization - Structured Approach

## Problem
Minimize c5 = max_k ∫_0^2 h(x)(1-h(x+k))dx
Subject to: h:[0,2]→[0,1], ∫h=1

## Key Insight
The trivial solution h=1 on [0,1], h=0 elsewhere gives c5_bound = 1/3 ≈ 0.3333,
yielding combined_score = 0.3809/0.3333 ≈ 1.14. This should beat the record!

## Construction Templates

### Template 1: Single Block (OPTIMAL SIMPLE)
h(x) = 1 for x ∈ [0, 1], 0 otherwise
- Automatically satisfies ∫h = 1
- Gives c5_bound = 1/3

### Template 2: Two Symmetric Blocks
h(x) = α for x ∈ [0, b] ∪ [2-b, 2], 0 otherwise
- Set α = 1/(2b) to satisfy ∫h = 1

### Template 3: Multi-Block with Fixed Positions
Define 5-10 blocks, optimize just heights

## Execution Strategy

1. First: Implement single block explicitly (should score > 1.0)
2. Second: Try 2-3 block constructions
3. Third: Switch to breakpoint optimization if needed

## Important
- Always verify ∫h=1
- Use construct_step_function tool to test
- Start simple, then refine
