---
name: discovery-optimization
description: "Step-function pattern mutation with coarse probing. Mutate the 12 seed patterns (heights, positions, level counts), probe all variants on coarse grids, then full-eval top candidates. Escape local optimum by exploring NEW pattern classes."
---

# C2 Optimizer: Step-Function Pattern Mutation Protocol

## Understanding the Seed Patterns
The seed provides 12 step-function patterns (EVOLVE-BLOCK). Each is piecewise-constant with specific heights and positions:
- Patterns 0-2: Single-level steps (heights 1.40, 1.50, 1.60)
- Patterns 3-7: Multi-level asymmetric steps (2-5 levels)
- Patterns 8-11: Novel asymmetric designs

## Mutation Strategy

### Type A: Height Perturbations
- Change all heights by +0.05 to +0.20 (keep proportional)
- Example: pattern 3 (0.90, 1.90, 0.90) -> (1.00, 2.10, 1.00)

### Type B: Position Shifts
- Shift interval boundaries by +/- 5%
- Example: pattern 0 (start=150, end=450 for n=600) -> (135, 495)

### Type C: Level Splitting
- Split one level into two with different heights
- Example: pattern 0 single level -> two levels at 0.70, 2.10

### Type D: Novel Pattern Construction
- Double peaks: two separated high regions
- Plateau with spike: wide base with narrow high peak
- Asymmetric multi-level: left/right sides different heights

## Probing Workflow (CRITICAL)

1. Generate 3-5 mutations from current best
2. Call probe_solution on ALL of them (cost: 3-5 probes)
3. Call evaluate_solution on TOP 1-2 by probe score
4. If neither beats record: Generate NEW pattern class
5. Repeat until iteration 15

## Phase 1: Exploration (iterations 1-15)
- Focus on diverse mutation types
- If current is single-level, try multi-level
- If current is symmetric, try asymmetric
- If current has 3 levels, try 2 or 4 levels

## Phase 2: Refinement (iterations 16-30)
- If beat record: fine-tune best architecture
- Small changes: +/- 0.02 height, +/- 3% position
- Try 3 variants, probe all, eval top 1

## Common Mistakes to Avoid
- Random noise mutations (add Gaussian noise) - DON'T DO THIS
- Calling evaluate without probing - WASTES BUDGET
- Staying in same pattern class for 5+ iterations
- Over-complicating (10+ levels) - SIMPLER IS BETTER
