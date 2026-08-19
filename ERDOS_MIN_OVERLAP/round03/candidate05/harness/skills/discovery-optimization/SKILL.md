---
name: discovery-optimization
description: "Blueprint-first search for Erdos minimum overlap problem"
---

# Erdos Minimum Overlap - Blueprint-First Strategy

## Why Blueprints Beat Random Optimization

Known constructions for the Erdos problem are STRUCTURED and COMPLIANT with the integral constraint. Random initialization often fails to hit these sweet spots.

## Three Blueprint Types to Test

1. bimodal_step: Two high-value intervals at [0.25,0.375] and [1.25,1.625], value 1; zero elsewhere. This gives integral=1 naturally.
   Advantages: Creates large gaps between high regions, reducing overlap.

2. periodic_alternating: h=1 on [0,0.5] and [1,1.5], h=0 on [0.5,1] and [1.5,2].
   Advantages: Simple periodic pattern, easy to fine-tune boundaries.

3. golomb_construction: Five narrow rectangular peaks at Golomb ruler positions scaled to [0,2].
   Advantages: Maximizes separation between peaks.

## Optimization Workflow

1. Blueprint generation: Implement 3 blueprint functions that satisfy integral(h)=1 exactly.
2. Direct c5 bound: For each blueprint, compute the exact c5_bound (no optimization yet).
3. Probe ranking: Use probe_solution on all 3 blueprints to get quick c5 estimates.
4. Fine-tune promising ones: For blueprints with c5_bound < 0.3809:
   - Use Adam optimizer (same as seed) for 2000 steps
   - lr=0.01, penalty=1000
   - Add small random noise to the blueprint as perturbation.
5. Probe again: Rank all fine-tuned variants with probe.
6. Full evaluate: Evaluate top 2 candidates with evaluate_solution.
7. Goal: Achieve combined_score > 1.0.

## Key Principles
- DO NOT delete or replace the existing optimizer class.
- DO NOT add random noise to initializations.
- Blueprint functions must satisfy integral(h)=1 by construction.
- Use probe_solution extensively before spending full evaluations.
- The seed code already works well; augment it, don't replace it.
