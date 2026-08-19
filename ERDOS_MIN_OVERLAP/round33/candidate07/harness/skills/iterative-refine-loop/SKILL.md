---
name: iterative-refine-loop
description: Iteratively refine a candidate by analyzing correlations and applying localized edits.
---

# Iterative Refinement Loop for C5 Optimization

## Core Idea
Instead of generating random new candidates, take a candidate and IMPROVE IT ITERATIVELY:

1. ANALYZE: Call correlation_analyzer on current candidate to find top 3-5 problematic shifts k.
2. EDIT: Apply localized mutation to reduce overlap at these k values. Modify h(x) only in regions that affect those shifts.
3. REANALYZE: Call correlation_analyzer again. Did the max overlap improve?
4. REPEAT: If yes, repeat steps 2-3 for 1-2 more rounds. If no, move to a different candidate.

## Practical Tips
- LOCALIZED mutations: change h in small contiguous regions (e.g., 50-200 intervals).
- Target the WORST k values first (highest overlap).
- After 2-3 refinement rounds, CALL probe_solution to check improvement.
- If probe_score < 0.382, CALL evaluate_solution.
- If no improvement after 3 rounds, ABORT refinement and try a new candidate.

## When to Use
- When you have a candidate that scored ~1.0 (no improvement yet).
- When you want to exploit a promising structure instead of searching blindly.
- When probe_solution indicates potential improvement but full evaluation is too costly.
