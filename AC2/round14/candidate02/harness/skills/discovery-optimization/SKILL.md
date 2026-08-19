---
name: discovery-optimization
description: "Step-function refinement for C\u2082 maximization. Use step_pattern_analyzer to extract pattern structure, then systematically perturb heights, widths, and positions. Only explore new architectures after exhausting step refinements."
---

# C₂ Maximizer: Step-Function Refinement Protocol

## Core Principle

Step functions achieve the current record through carefully tuned heights and widths. To beat it, make SMALL, TARGETED perturbations to ONE parameter at a time, then evaluate.

## Phase 1: Pattern Analysis (Iteration 1)

1. Call step_pattern_analyzer ONCE to extract:
   - Number of levels/steps
   - Heights at each interval
   - Width ratios between intervals
   - Overall asymmetry

2. Understand the pattern class before mutating

## Phase 2: Single-Parameter Mutation

For each mutation, change ONLY ONE parameter:

**Mutation Type 1: Height Perturbation**
- Adjust ONE level height by ±0.03-0.08
- Try: increase the tallest level slightly, decrease the shortest
- Rationale: Alters ||f★f||₂² vs ||f★f||_∞ ratio

**Mutation Type 2: Width Expansion/Contraction**
- Change ONE interval width by ±3-8%
- Expand the "core" interval (highest step) to increase L2 norm
- Contract "wing" intervals to reduce infinity norm

**Mutation Type 3: Position Shift**
- Shift ONE boundary by ±1-2% of domain
- Can break symmetry and reduce constructive interference

## Phase 3: Mutation Cycle

1. Generate 3-5 mutations (each perturbing different parameters)
2. Call probe_solution for each (use all 30 probes to rank)
3. Call evaluate_solution for top 2-3 by probe score
4. If improvement: continue refining that parameter direction
5. If no improvement after 3 parameter types: try next mutation cycle

## Phase 4: Architecture Exploration (last resort)

Only after exhausting 3+ mutation cycles without improvement:
- Call generate_candidates for new families
- But expect: smooth functions likely UNDERPERFORM step functions
- Return to step refinement if new families fail

Key: ONE parameter at a time. Systematic refinement beats random exploration.
