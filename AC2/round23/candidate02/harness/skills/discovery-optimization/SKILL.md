---
name: discovery-optimization
description: "Structural recombination of step patterns with frequency-aware optimization. Recombine seed patterns, explore multi-scale architectures, prioritize spectral smoothness."
---

# C2 Maximizer: Structural Recombination Protocol

## Core Principle
The seed's 12 step patterns provide building blocks. RECOMBINE them by merging peaks, swapping heights, and creating asymmetric variants. This explores the ARCHITECTURE space, not just parameter space.

## Phase 1: Pattern Recombination (iterations 1-10)

Step 1: Analyze and Recombine
- Call analyze_and_recombine_patterns to identify active patterns
- Note: number of peaks, peak heights, relative positions
- Generate 4-5 recombinations:
  * Recombination A: Merge two adjacent peaks into wider peak
  * Recombination B: Swap heights between patterns (e.g., copy middle peak height to outer peaks)
  * Recombination C: Create asymmetric variant (shift one side higher)
  * Recombination D: Try 3-peak configuration by splitting a wide peak
  * Recombination E: Combine features from patterns 1, 3, and 11

Step 2: Probe and Evaluate
- Call probe_solution on ALL 4-5 variants
- Rank by probe score
- Call evaluate_solution on TOP 1
- If probe score < 1.0: try opposite direction (e.g., split instead of merge)

## Phase 2: Frequency-Domain Optimization (iterations 11-22)

Step 1: Analyze Spectral Properties
- Probe solution and examine convolution frequency spectrum
- Note: high-frequency oscillations reduce C2 (they increase L2 norm without improving L1)
- Goal: flatten the convolution spectrum (smoother functions)

Step 2: Smoothness Mutations
- Widen narrow peaks to reduce high-frequency content
- Create smoother transitions between steps
- Try spline-like approximations (piecewise linear instead of piecewise constant)

Step 3: Gradient Refinement
- If promising, use JAX gradients to fine-tune parameters
- Focus on parameters that affect spectral smoothness

## Phase 3: Architecture Search (iterations 23-30)

Step 1: Multi-Peak Exploration
- Systematically try 2-peak, 3-peak, 4-peak configurations
- Keep best peak height, reposition others

Step 2: Asymmetric Exploration
- Try left-skewed and right-skewed variants
- Try exponential-like decay (front-loaded peaks)

Step 3: Final Evaluation
- Probe, evaluate best
- Submit if c2 > 0.8962799441554086

## Key Rules
- RECOMBINE patterns before tweaking parameters
- Prioritize spectral smoothness (flatter convolution = better C2)
- Use 5-7 probes before any full eval
- Try architectural changes (merge/split peaks) before gradient descent
