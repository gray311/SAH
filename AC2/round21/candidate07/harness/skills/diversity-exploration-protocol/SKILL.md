---
name: diversity-exploration-protocol
description: Broad function family exploration with gradient refinement within promising families. Never stay in one family for > 8 iterations.
---

# C2 Maximizer: Diversity Exploration Protocol
## Core Principle
Step functions are a LOCAL optimum. You MUST explore multiple function families (steps, splines, polynomials, exponential, mixtures) before refining any one. Use gradients ONLY within a promising family.
## Phase 1: Broad Family Exploration (iterations 1-10)
1. Call analyze_function_family to identify current structure
2. Generate 4 variants from DIFFERENT families: - Family A: Multi-level steps (5-7 levels, asymmetric heights 0.5-2.5) - Family B: B-spline (5-7 basis functions, smooth transitions) - Family C: Piecewise polynomial (3-5 segments, C1 continuity) - Family D: Exponential-plateau (decay-rise-flat-decay)
3. Probe all 4, evaluate top 2
4. If all score <= 1.0: try Family E (Gaussian mixture of 3-5 components)
5. Continue with best-performing family
## Phase 2: Gradient Refinement (iterations 11-20)
1. Compute JAX gradients on current family's parameters
2. Generate 3 variants: (a) gradient ascent, (b) orthogonal perturbation, (c) gradient + noise
3. Probe all 3, evaluate best
4. If gradient norm < 0.001: switch to Phase 3
## Phase 3: Hybrid Approaches (iterations 21-25)
1. Mix best candidates: smooth steps, add polynomial tails, ensemble top 2
2. Probe 3 hybrids, evaluate best
3. Submit if c2 > 0.8962799441554086
## Key Rules
- TRY AT LEAST 3 DIFFERENT FAMILIES before Phase 2 - Use gradients ONLY within a family - Probe 4-6 variants before ANY full eval - If stuck at iteration 10+: call reinitialize_with_diversity
