---
name: pattern-evolution-strategy
description: Systematic approach to discovering new C₂-optimizing patterns. Analyze current patterns, propose new architectures (asymmetric, multi-peak, smooth transitions), evaluate, and iterate.
---

# Pattern Evolution Strategy for C₂ Maximization

## Overview
The seed program's multi-level step patterns are locally optimized. Small tweaks won't help. You need to discover NEW pattern architectures.

## Phase 1: Analyze Current Pattern
1. Call pattern_searcher to understand the current best pattern's structure
2. Note key features: peak heights, spacing, symmetry, number of levels
3. Identify where the current pattern might be suboptimal

## Phase 2: Generate New Pattern Classes
Don't just tweak parameters - create NEW architectures:

**Exploration Direction 1: Asymmetric Multi-Peaks**
- Create 3-5 peaks with intentionally unequal heights
- Example pattern: [0.6h, 1.5h, 0.5h, 1.3h, 0.4h] where h = average height
- Rationale: Breaking symmetry may reduce the infinity norm of the convolution

**Exploration Direction 2: Smooth Transitions**
- Replace hard steps with piecewise exponential or quadratic transitions
- Example: use soft+ for transitions: f(x) = exp(-α|x - x₀|) scaled appropriately
- Rationale: Smooth functions may have better convolution properties

**Exploration Direction 3: Centered Dominant Peak**
- One tall central peak with smaller asymmetric side peaks
- Example: [0.4h, 1.6h, 0.3h, 1.4h, 0.3h]
- Rationale: Concentrating mass may optimize the ratio

**Exploration Direction 4: Irregular Spacing**
- Non-uniform interval placements
- Example: vary interval widths by 15-25%
- Rationale: Avoids constructive interference in convolution

## Phase 3: Evaluate and Iterate
1. For each new pattern class, generate 2-3 concrete implementations
2. Evaluate each with evaluate_solution (probe is unreliable)
3. If a class improves: generate more variants in that class
4. If all fail: analyze why and try a different architectural direction

## Key Principles
- Diversity > refinement: New architectures beat better parameters
- One eval at a time: Don't generate 10 variants; test one, learn, then try another
- Math matters: Understand WHY a pattern should work before implementing it
