---
name: discovery-optimization
description: "Structured step-function mutation protocol. Systematically perturb heights, widths, positions of step patterns. Use probe-based filtering to find improvements."
---

# C2 Optimizer: Structured Step-Function Mutation Protocol

## Core Principle

Step functions are near-optimal but are LOCAL optima. Escape them via STRUCTURED perturbations, not entirely new function classes.

## Mutation Types (in order of effectiveness)

### Type 1: Asymmetric Height Perturbation
- Take symmetric pattern [h1, h2, h3] → make asymmetric [h1+δ1, h2, h3+δ3]
- δ values: ±0.02 to ±0.08 (small!)
- Example: [1.50, 1.50, 1.50] → [1.53, 1.50, 1.47]

### Type 2: Width Perturbation
- Perturb interval boundaries by 3-8% (not 10%+)
- Example: 0.25n → 0.26n, 0.75n → 0.74n
- Focus on expanding the "core" region, contracting wings

### Type 3: Center-of-Mass Shift
- Shift ALL interval boundaries by 1-2% in one direction
- Example: all starts+0.01n, all ends+0.01n
- Can break symmetry and improve ||f★f||_2

### Type 4: Local Bump Addition
- Add small bumps (height 0.1-0.3, width 0.05-0.1n) to existing steps
- Place bumps at 1/3, 2/3, or center of large intervals
- Creates local maxima that improve L2 norm

### Type 5: Multi-Level Refinement
- For 2-level steps, add intermediate levels
- Example: [high, low] → [high, mid, low] with mid = 0.7*high + 0.3*low

## Phase 1: Initial Exploration (iterations 1-3)
1. Generate 3 mutations using different types above
2. Probe all 3 (use all 3 probes)
3. Evaluate top 2 by probe score

## Phase 2: Focused Search (iterations 4+)
1. If mutation type A works: generate 2 more variants of type A
2. If type A fails: switch to type B
3. Never spend >3 iterations on one failing type
4. If no improvement after 10 iterations: restart with fresh mutation types

## Phase 3: Escaping Local Optima
If stuck:
- Try ALL 5 mutation types once
- Combine successful elements from different types
- Increase perturbation magnitude slightly (but keep <10%)

## Key Rules
- SMALL perturbations only (step functions are sensitive)
- PROBE BEFORE EVALUATE (30 probes = rank many variants)
- DIVERSE mutation types, but focus on ONE working type
- NEVER try entirely new function classes (smooth, oscillatory, etc.) - they underperform steps
