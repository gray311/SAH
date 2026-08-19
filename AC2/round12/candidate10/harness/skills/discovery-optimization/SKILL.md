---
name: discovery-optimization
description: "Multi-strategy mutation for C\u2082 maximization. Use mutation_generator to analyze current patterns and generate diverse mutation proposals (height, width, asymmetry, center shifts, intermediate adjustments, radical reconstructions). Use arch_explorer to propose entirely new pattern architectures when stuck."
---

# C₂ Maximizer: Multi-Strategy Mutation Protocol

## Core Principle

Don't just refine - explore diverse mutation types in PARALLEL. The seed's patterns work but are locally optimized. Need both systematic refinement AND radical innovation.

## Phase 1: Initial Exploration (first 3 iterations)

1. Call mutation_generator ONCE to get 5 diverse mutation proposals

2. Implement the TOP 2-3 mutations with edit_solution (different types if possible)

3. Evaluate each with evaluate_solution

4. Track which mutation TYPE improves (height, width, asymmetry, center, intermediate)

## Phase 2: Focused Refinement

If a mutation type shows promise:

- Generate 2-3 more variants of that SAME type
- Implement and evaluate
- Continue until NO improvement for 3 consecutive variants

## Phase 3: Strategy Reset (when stuck)

Call arch_explorer when:
- 5+ iterations with no improvement OR
- Tried 4+ different mutation types without success

arch_explorer returns COMPLETELY NEW pattern architectures (different number of levels, different shapes).

Then:
- Implement the top new architecture
- Evaluate
- Treat it as a fresh starting point

## Mutation Types (mutation_generator provides):

### Type 1: Height Perturbation
- Increase main peak by 0.08-0.12, decrease others by 0.04-0.06

### Type 2: Width Expansion
- Expand central interval by 8-12%, keep others unchanged

### Type 3: Asymmetric Variation  
- Apply +6% to odd levels, -4% to even levels (alternating pattern)

### Type 4: Center of Mass Shift
- Shift all interval boundaries right/left by 1.5-2.5%

### Type 5: Intermediate Adjustment
- Increase intermediate levels by 0.05-0.08, preserve main peaks

### Type 6: Radical Reconstruction (arch_explorer only)
- Completely new pattern with different structure (e.g., bimodal, trimodal, different spacing)

## Key Principles

1. PARALLEL exploration: try multiple mutation types, not sequential
2. RADICAL when stuck: arch_explorer is your reset button
3. SYSTEMATIC within a type: exhaust one type before moving to next
4. DIVERSE proposals: always get 5 options, pick from different types
