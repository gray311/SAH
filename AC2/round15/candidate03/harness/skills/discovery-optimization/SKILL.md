---
name: discovery-optimization
description: "Step-function refinement through systematic perturbation and probe-based filtering."
---

# C₂ Optimizer: Step-Function Refinement Protocol

## Core Principle
The seed's hybrid step functions are near-optimal. Beat them by SMALL, SYSTEMATIC perturbations.

## Mutation Operations (apply one at a time, search/replace style)

**Operation A: Height Perturbation**
- Adjust individual step heights by ±0.02 to ±0.08
- Try: increase one step, decrease another (break symmetry)

**Operation B: Width Expansion/Contraction**
- Shift interval boundaries by 3-8% of domain
- Try expanding "core" steps, contracting "wing" steps

**Operation C: Asymmetry Breaking**
- Make left/right steps different heights or widths
- This breaks perfect symmetry and can improve L2/∞ ratio

**Operation D: Multi-level Refinement**
- Adjust intermediate levels in multi-step functions
- Try increasing "wing" levels relative to "core"

## Workflow
1. Decide on one mutation operation
2. Generate 3-4 concrete variants implementing that operation
3. CALL probe_solution for EACH variant (use all 30 probes here!)
4. Select top 2-3 by probe score
5. CALL evaluate_solution for those top variants
6. If improvement: refine further; if not: try a different mutation operation

## Key Rules
- PROBE BEFORE EVALUATE ALWAYS
- Small mutations only (don't rewrite the function)
- Exploit the step-function architecture, don't abandon it
- If stuck after 10 iterations: try completely different mutation type (asymmetry, multi-level, etc.)
