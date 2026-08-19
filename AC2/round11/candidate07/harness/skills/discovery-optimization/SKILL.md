---
name: discovery-optimization
description: "Mathematically-grounded pattern discovery for C2 maximization with rapid exploration via cheap probing. Use pattern_searcher to analyze current patterns and propose new pattern classes (asymmetric multi-peaks, spline transitions, irregular configurations). Use c2_probe to quickly filter 10-20 variants before fully evaluating the top 2-3. Focus on discovering entirely new architectures rather than small parameter tweaks."
---

C2 Maximizer: Rapid Exploration with Cheap Probing

Core Principle

The seed program's 13 step patterns are already locally optimized. Small mutations won't help. You
MUST discover NEW pattern architectures, and you MUST use cheap probing to efficiently find them.

The Exploration Loop (Repeat until success)

1. Generate diversity: Create 10-15 variant patterns using:
   - pattern_searcher (call once early, then reuse its methodology)
   - Asymmetric multi-peaks with varying height ratios
   - Smooth transitions (exponential/quadratic blends)
   - Irregular spacing patterns

2. Probe rapidly: Call c2_probe on each variant. This is CHEAP (~10ms vs minutes).
   Each probe uses the separate 30-probe budget, NOT the 30 full-eval budget.

3. Select top candidates: Identify the 2-3 variants with highest probe scores.

4. Fully evaluate: Call evaluate_solution on the top 2-3 candidates.
   Only spend your precious full evaluations here.

5. Iterate: If progress, drill deeper into successful pattern class.
   If no progress after trying 5+ different architectural directions, restart with new directions.

Pattern Classes to Explore

Asymmetric Multi-Peaks: Create 3-5 peaks with intentionally unequal heights
Example pattern heights: [0.6h, 1.5h, 0.5h, 1.3h, 0.4h] where h = average height

Smooth Transitions: Replace hard steps with piecewise exponential or quadratic
Rationale: Smooth functions may have better convolution properties without increasing ||f★f||∞

Centered Dominant Peak: One tall central peak with smaller asymmetric side peaks
Example: [0.4h, 1.6h, 0.3h, 1.4h, 0.3h]

Irregular Spacing: Non-uniform interval placements
Vary interval widths by 15-25% to avoid constructive interference

Multi-mode Peaks: 3+ peaks with varying separations and heights

Key Principles

- Diversity over refinement: New architectures beat better parameters
- Probe first: Always use c2_probe to filter before full evaluation
- One full eval at a time: Don't generate 10 variants; test one direction, probe-filter, then evaluate
- Math matters: Understand WHY a pattern should work before implementing it
