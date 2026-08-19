---
name: discovery-optimization
description: "Mathematically-grounded pattern discovery for C\u2082 maximization. Use pattern_searcher to analyze current patterns and propose new pattern classes (asymmetric multi-peaks, spline transitions, irregular configurations). Focus on discovering entirely new architectures rather than small parameter tweaks."
---

# C₂ Maximizer: Pattern Discovery Protocol

## Core Principle
The seed program's 13 step patterns are already locally optimized. Small mutations won't help. You MUST discover NEW pattern architectures.

## Phase 1: Structural Analysis (first iteration)
1. Call pattern_searcher to understand current best pattern's structure
2. Identify where ||f★f||∞ is maximized and ||f★f||₂² could be increased
3. Note: asymmetry, discontinuity locations, and relative heights affect C₂ differently

## Phase 2: Pattern Generation
Generate diverse new patterns by:

**New Pattern Classes to Explore**:
- **Asymmetric multi-peaks**: Unequal peak heights/positions (e.g., 0.6, 1.8, 0.3 heights)
- **Spline transitions**: Smoothly connect steps with quadratic/exponential transitions
- **Tailored asymmetry**: Shift the "center of mass" of the pattern
- **Multi-mode peaks**: 3+ peaks with varying separations
- **Truncated/power functions**: Instead of hard steps, use piecewise power-law decays

## Phase 3: Evaluation Strategy
- Each pattern proposal: call evaluate_solution ONCE (probe is unreliable on this delicate problem)
- Track which pattern CLASS improves, not just individual parameters
- If a class works: generate more variants in that class
- If all fail: go back to pattern_searcher for new directions

## Phase 4: Iteration
1. Analyze → 2. Generate diverse candidates → 3. Evaluate each → 4. Drill down or diversify

Key: Think mathematically about WHY a pattern should improve C₂, not just "try a different number."
