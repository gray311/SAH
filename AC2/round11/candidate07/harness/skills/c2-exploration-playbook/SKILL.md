---
name: c2-exploration-playbook
description: Systematic approach to discovering C2-optimizing patterns using cheap probing for rapid exploration.
---

C2 Exploration Playbook: Probe-First Strategy

Overview

Full evaluations are expensive (30 budget total). You cannot afford to evaluate every variant.
Use c2_probe to rapidly filter 10-20 variants, then evaluate only the top 2-3.

The Probe-First Loop

Step 1: Generate Diverse Candidates (10-15 variants)

Generate patterns from multiple architectural directions:
1. Asymmetric multi-peaks: 3-5 peaks with varying heights (e.g., [0.6, 1.5, 0.5, 1.3, 0.4] relative to avg height)
2. Smooth transitions: Blend steps with exponential/quadratic functions
3. Irregular spacing: Non-uniform interval placements (vary widths by 15-25%)
4. Centered dominant peak: Tall central peak with smaller asymmetric wings
5. Multi-mode peaks: 3+ peaks with varying separations

Step 2: Rapid Probing (3-5 probes per batch)

- Call c2_probe on each of your 10-15 variants
- This takes ~10ms per probe vs minutes for full evaluation
- You have 30 probes total - use them wisely

Step 3: Select and Evaluate

- Identify top 2-3 candidates by probe score
- Call evaluate_solution on those 2-3 (uses the precious 30-full-eval budget)
- The best full evaluation score determines your next iteration

Step 4: Iterate or Restart

- If progress: drill deeper into the successful pattern class
- If no progress after 3-4 different architectural directions: restart with new directions

Key Principles

- Probe before evaluate: Always filter with probes first
- Diversity over depth: Try many different architectures cheaply before refining
- One full evaluation at a time: Don't evaluate multiple candidates at once
- 30 probes = 30 opportunities: Use each probe to make progress
- Mathematical intuition: Understand why a pattern works before implementing
- c2_probe preserves ordering: Relative scores are reliable enough for filtering
