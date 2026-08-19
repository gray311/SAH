---
name: step-function-discovery
description: Methodology for discovering better step functions in C₂ optimization. Use systematic pattern exploration, FFT properties, and probing.
---

# Step Function Discovery Methodology for C₂ Optimization
## Core Principles
1. **C₂ = ||f★f||₂² / (||f★f||₁||f★f||_∞)**: Maximize numerator (L₂ energy), minimize denominator (especially L∞) 2. **Step functions work**: 13 pre-defined patterns in seed achieved 1.03+ 3. **FFT convolution**: Use O(n log n) convolution via FFT 4. **Positivity constraint**: f(x) >= 0 (use relu or ensure non-negative construction)
## Systematic Exploration Strategy
### Step 1: Understand Current Pattern - Count steps and analyze height distribution - Check symmetry (even functions reduce search space) - Estimate convolution L₂ vs L∞ balance
### Step 2: Parameter Sweep Systematically vary: - Peak heights: [1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2] - Peak widths: [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75] - Number of levels: [1, 2, 3, 4, 5]
### Step 3: Probing Before Evaluation - Generate 3-5 variants from seed - Probe each (~10s each, separate budget) - Pick top 2, evaluate fully - This saves 10+ eval budget per iteration
### Step 4: Refinement Once score > 1.03431: - Tighten peaks (narrower width, higher height) - Add asymmetric components - Try multi-scale approach (coarse→fine grid) - Explore Fourier-based representations
### Step 5: Avoid Traps - Don't increase num_intervals beyond necessity - Don't use random initialization (deterministic is better) - Don't skip probing - Always analyze before editing - Keep edits small (SEARCH/REPLACE)
