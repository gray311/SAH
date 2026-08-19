---
name: discovery-optimization
description: "C\u2082 maximization via structural exploration. Prioritize discovering new function classes (splines, mixtures) over local step pattern refinement."
---

# C₂ Maximizer: Structural Exploration Protocol

## Phase 1: Quick Step Pattern Refinement (0-5 evals)
- If structural_explorer not yet called, try 1-2 small step mutations
- Goal: Establish baseline improvement from current patterns
- STOP if no improvement after 2-3 mutations

## Phase 2: New Function Class Discovery (PRIMARY FOCUS)
- Call structural_explorer to get 2-3 new function class candidates
- Implement each with edit_solution
- Evaluate each with evaluate_solution (4-6 evals)
- Keep the best, discard others

## Phase 3: Iterate
- If new class improves: refine it with small mutations (Phase 1 strategy)
- If current class stalls: call structural_explorer again for next class

## Function Classes to Explore (via structural_explorer):
- B-spline based functions
- Gaussian mixture models
- Smoothed step functions (sigmoid-based)
- Piecewise polynomial functions
- Multi-modal functions (multiple separated peaks)

## Budget Discipline:
- You have 30 evals - use ~6-10 for exploration, ~15-20 for refinement
- Call finish when you've explored 2-3 distinct function classes
- Don't obsess over 0.001 improvements - focus on finding better classes
