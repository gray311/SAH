---
name: architecture-jump-protocol
description: Jump between fundamentally different function families to escape local optima.
---

# Architecture Jump Protocol for C2 Maximization

## Core Principle
Small mutations within step-functions cannot escape the local optimum. You MUST
jump to completely different function families that have different mathematical properties.

## When to Jump (trigger conditions)
1. After 3 failed mutation attempts on same architecture
2. After iteration 10 without improvement
3. When probe scores plateau across 5+ variants
4. When analyze_convolution_profile suggests structural changes

## Architecture Families (rotate through these)
1. Gaussian Mixtures: f(x) = sum w_i * exp(-((x-mu_i)^2)/(2*sigma_i^2))
   Pros: Smooth, analytically tractable convolution
   Call when: analysis suggests widening support
   
2. B-spline Basis: Optimized control points with softplus positivity
   Pros: Flexible smooth transitions, many degrees of freedom
   Call when: need fine control over shape
   
3. Oscillatory Decay: f(x) = (1 + alpha*cos(beta*x))*exp(-gamma*|x|)
   Pros: Creates structured convolution with potential for better L2/inf ratio
   Call when: interference pattern suggests adding structure
   
4. Piecewise-Linear: Linear segments connecting optimized vertices
   Pros: Balances smoothness with computational efficiency
   Call when: smooth functions don't improve
   
5. Multi-Level Asymmetric Steps: Refined step structures with varying heights
   Pros: Keeps advantages of steps while adding flexibility
   Call when: steps still show promise but need refinement

## Execution Flow
1. Call analyze_convolution_profile to get diagnosis
2. Choose architecture family based on diagnosis
3. Call generate_candidates with that family focus
4. Probe all candidates, evaluate top 2
5. If no improvement after 2 full evals: switch to next family

## Key Rule
NEVER stay in one family for more than 3 iterations. Rotate families every time you
run out of promising variants. Parallel diversity beats sequential refinement.
