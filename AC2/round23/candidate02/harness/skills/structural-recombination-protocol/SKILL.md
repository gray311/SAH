---
name: structural-recombination-protocol
description: Recombine step patterns by merging peaks, swapping heights, creating asymmetric variants. Prioritize spectral smoothness.
---

# Structural Recombination Protocol for Step Functions

## Core Principle
The seed provides 12 step patterns. RECOMBINE them by merging peaks, swapping heights, and creating asymmetric variants. This explores ARCHITECTURE, not just parameters.

## Phase 1: Pattern Recombination (iterations 1-10)

Step 1: Analyze and Recombine
- Call analyze_and_recombine_patterns to identify active patterns
- Generate 4-5 recombinations:
  * A: Merge two adjacent peaks into wider peak
  * B: Swap heights between patterns
  * C: Create asymmetric variant
  * D: Try 3-peak by splitting a wide peak
  * E: Combine patterns 0, 3, 11

Step 2: Probe and Evaluate
- Probe ALL 4-5 variants
- Evaluate TOP 1
- If no improvement: try opposite direction

## Phase 2: Frequency-Domain Optimization (iterations 11-22)

Step 1: Analyze Spectral Properties
- Examine convolution frequency spectrum
- Goal: flatten high-frequency oscillations (smoother = better C2)

Step 2: Smoothness Mutations
- Widen peaks to reduce high-frequency content
- Create smoother transitions between steps

## Phase 3: Architecture Search (iterations 23-30)

Step 1: Multi-Peak Exploration
- Systematically try 2-peak, 3-peak, 4-peak configs

Step 2: Final Evaluation
- Submit if c2 > 0.8962799441554086
