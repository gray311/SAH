---
name: discovery-optimization
description: "C2 maximization via DIVERSIFIED function class exploration. Probe splines, Fourier, polynomial, Gaussian, and hybrids."
---

# C2 Maximization: DIVERSIFIED Function Class Exploration

## Core Principle: Broad Exploration Over Narrow Refinement

The seed program's step functions achieve 1.034x improvement - but this leaves 6x gap to the theoretical maximum (1.0). To bridge this, you MUST explore function classes beyond step functions.

## Strategy: Multi-Phase Exploration

### Phase 1: Rapid Family Survey (iterations 1-5)

Create COMPLETELY DIFFERENT function representations:

1. B-spline functions: Use scipy.interpolate with knots in [-3, 3]
2. Fourier basis functions: sum of cos(k*pi*x/L) with softplus coefficients
3. Polynomial decay: (1 - |x|/R)^alpha for |x|<R
4. Gaussian/Polya functions: Sum of exp(-a*(x-x0)^2)
5. Hybrid approaches: Step function with smooth tails

### Phase 2: Deepen Promising Directions (iterations 6-12)

Once a function class shows promise (probe combined_score > 1.05):
- Increase complexity
- Systematically vary parameters

### Phase 3: Convergence (iterations 13-20)

- Evaluate only 1-2 best candidates from Phase 1-2
- Call finish when exhausted budget or plateau

## Critical Avoidances

- DON't loop endlessly refining step functions
- DON't waste evals on unproven function classes - always probe first
- DO explore at least 3-4 different function families
- DO use probes aggressively
