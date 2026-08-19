---
name: discovery-optimization
description: "Systematic step-function refinement for C\u2082 maximization. Analyze convolution properties, apply targeted mutations, probe to rank, evaluate top variants, iterate."
---

# C₂ Maximizer: Systematic Step-Function Refinement Protocol

## Core Principle

The step-function record is HIGH but achievable. Break it through PRECISE, mathematically-informed refinements, not wild exploration.

## Phase 1: Initial Analysis (First Iteration)

1. Call analyze_convolution ONCE on the current best function
2. Study the convolution profile:
   - Where is ||f★f||_∞ achieved (peak location, width)?
   - How is energy distributed (L₂ vs L₁)?
   - Are there symmetries or asymmetries?

## Phase 2: Targeted Mutation

Generate ONE concrete implementation per mutation type:

**Mutation Type 1: Peak Height Optimization**
- Increase the central peak by 0.01-0.03
- Decrease side peaks by 0.01-0.02
- Rationale: Adjust L₂/∞ balance

**Mutation Type 2: Width Refinement**
- Expand the high plateau by 2-5% (e.g., 0.22n → 0.23n)
- Contract the side regions by 2-5%
- Rationale: Spread convolution energy more evenly

**Mutation Type 3: Asymmetric Enhancement**
- Make left and right steps slightly different (e.g., 1.45 vs 1.40)
- Rationale: Break symmetry to reduce interference peaks

**Mutation Type 4: Small Bump Addition**
- Add a tiny bump (height 0.05-0.10, width 0.02n) in a low region
- Rationale: Fill "valleys" in convolution, improve L₂

## Phase 3: Probe → Evaluate Loop

1. For each mutation, call probe_solution to rank
2. Select top 2-3 by probe score
3. Call evaluate_solution on top 2-3
4. If none improve: pick a different mutation type
5. If improvement: use new best as starting point and repeat

## Phase 4: Pattern Switching

If 15+ iterations with no improvement:
- Try a completely different step pattern (e.g., 4 levels instead of 2, or asymmetric multi-step)
- Then restart the refine→probe→evaluate loop
