---
name: family-optimization-protocol
description: Explore multiple function families with probes, then optimize within best family.
---

# Family-Optimization Protocol for C2 Maximization

## Core Principle
Step functions may not be optimal. Systematically explore different function families
(B-splines, Fourier series, Gaussian mixtures) using cheap probes before deep optimization.

## Phase 1: Function Class Scanning (iterations 1-8)

Step 1: Multi-Family Probe Scan
- Call scan_function_class to test 3-5 function families
- Each family returns probe scores on representative variants (e.g., peak_height 1.6 vs 2.0)
- Compare probe scores: look for consistent >1.0 indication

Step 2: Select Best Family
- Pick family with highest probe score
- If no family >1.0 probe: try step function again with different initialization
- Call evaluate_solution ONCE on the best family's top variant

Step 3: Family-Specific Setup
- Record which family won (b_spline/Fourier/mixture/hybrid)
- Configure edit_solution for that family's parameters

## Phase 2: Family-Specific Optimization (iterations 9-22)

Step 1: Optimize Within Family

- If B-spline: Optimize knot positions and peak heights
  * Target C2 ~0.90 to guide peak height scaling
  * Try knot density 50-80 for good resolution

- If Fourier: Optimize number of modes and envelope width
  * Start with 15-25 modes
  * Focus on cosine series (even functions) for symmetry
  * Gaussian envelope for localization around center

- If Mixture: Optimize Gaussian centers and widths
  * Use 2-5 components with asymmetric centers (0.2, 0.4, 0.6, 0.8)
  * Widths: 0.1-0.2 for smooth transitions

- If Hybrid: Optimize step width and spline smoothing width
  * Base step width: 0.4-0.6 of domain
  * Spline edge smoothing: 0.05-0.15 of domain

Step 2: Periodic Rescan
- At iterations 12 and 18: call scan_function_class again
- Check if new families outperform current best
- Switch families if new probe score >1.15

Step 3: Probe-Driven Iteration
- Generate 2-3 variants per iteration
- Probe all, evaluate best
- Maintain best c2 seen across all families

## Phase 3: Aggressive Final Search (iterations 23-30)

Step 1: Radical Reinitialization
- In winning family: reinitialize 50% of parameters
- Try alternative configurations:
  * B-spline: different knot spacing or peak positions
  * Fourier: reverse envelope width or mode count
  * Mixture: asymmetric centers (0.1, 0.35, 0.65, 0.9)

Step 2: Final Probe-Eval
- Probe 2-3 radically different variants
- Evaluate best (budget critical)
- If c2 > 0.8962799441554086: submit

## Key Rules
- Call scan_function_class at start of each phase
- Use probes to filter families: 5-10 probes per family, 10+ per variant
- Evaluate solution ONLY on top family candidates
- If probe score <1.0: try variant with opposite parameter direction
- Budget: 30 probes + 30 evals max
