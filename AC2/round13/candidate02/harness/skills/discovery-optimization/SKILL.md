---
name: discovery-optimization
description: "Mathematically-grounded pattern mutation for C2 maximization with structural analysis. Use analyze_convolution to understand current patterns' Fourier characteristics, then generate targeted mutations. Leverage probes for rapid filtering before full evaluation."
---

# C2 Maximizer: Structural Analysis and Targeted Mutation Protocol

## Core Principle

Step functions achieve C2 approximately 0.8963 because their convolutions have specific spectral properties. To beat them, you need to:
1. Understand what makes the current best work (via analyze_convolution)
2. Find directions that reduce the denominator while increasing the numerator

## Phase 1: Structural Analysis (First 1-2 iterations)

1. Call analyze_convolution ONCE on your current best solution
2. Study the output:
   - Frequency spectrum: Where is energy concentrated?
   - Peak location: Where is the infinity norm achieved?
   - Width characteristics: How broad is the convolution?
3. Form hypotheses about improvement directions

## Phase 2: Targeted Mutation Generation

Based on your analysis, generate mutations in this priority order:

Mutation Type A: Peak Reduction
- If the convolution has a sharp peak, try functions with smoother transitions
- Reduce local maxima by 5-15% in the original function

Mutation Type B: Width Expansion
- Expand the core region by 10-20% to broaden the convolution's main lobe
- This can increase the L2 norm squared without significantly increasing the infinity norm

Mutation Type C: Spectral Hole Filling
- If analysis shows certain frequencies have low energy, add oscillatory components
- Try multiplying the base function by one plus a cosine term

Mutation Type D: Asymmetric Perturbation
- Break symmetries by making heights asymmetric
- Shift patterns left or right by 2-3% of domain

## Phase 3: Probe-Based Filtering

1. Generate 3-5 mutations of the same type
2. Call probe_solution for each (you have 30 probes)
3. Keep only those with probe greater than current best
4. Call evaluate_solution once per promising candidate

## Phase 4: Iteration and Restart

If no improvement after 10 iterations:
1. Call analyze_convolution on the current best
2. Try a completely different function class

## Key Rule: Probes First, Evaluations Last

- You have 30 probes and only 30 full evaluations
- Use probes to filter five to ten mutations down to three to five promising ones
- Never call evaluate_solution on a mutation you haven't probed first
