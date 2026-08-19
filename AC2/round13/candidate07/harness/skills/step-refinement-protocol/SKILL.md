---
name: step-refinement-protocol
description: Targeted refinement of step-function patterns. Mutate heights (±0.02-0.08), widths (±3-8%), or induce asymmetry in one step at a time.
---

# Step-Function Refinement Protocol

## Core Principle

The 13 seed patterns are well-tuned. Beat the record through **small, targeted mutations**, not random exploration.

## Mutation Types (use one at a time)

### 1. Height Fine-Tuning
- Adjust peak heights by ±0.02 to ±0.08
- Try both increasing and decreasing the main peak
- Keep other heights fixed while mutating one

### 2. Width Optimization  
- Expand core intervals by 3-6%
- Contract wing intervals by similar amount
- Maintain total domain coverage

### 3. Asymmetry Induction
- Take symmetric patterns and break symmetry
- Example: [1.40, 1.50, 1.40] → [1.42, 1.50, 1.38]
- Small asymmetries (2-4%) can improve the C₂ ratio

## Execution Strategy

1. Call generate_step_variants to get 3 variants (one of each mutation type)
2. Call probe_solution on all 3 (uses probe budget)
3. Evaluate the top 1-2 by probe score
4. If improvement: apply same mutation type to current pattern
5. If no improvement after 3 iterations: switch to different seed pattern

## Pattern Cycling

If current pattern stalls:
- Move to next seed pattern (0→1→2→...→12→0)
- Each pattern has different structure, may respond to different mutations
- Don't refine one pattern to exhaustion; cycle through all
