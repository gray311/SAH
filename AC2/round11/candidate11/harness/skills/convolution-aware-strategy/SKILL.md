---
name: convolution-aware-strategy
description: C₂ maximization using convolution analysis. First analyze where ||f★f||∞ and ||f★f||₂² can be improved, then generate mathematically-grounded modifications. Switch from step to continuous functions if needed.
---

# Convolution-Aware C₂ Maximization Strategy

## Critical Insight
The seed program's step patterns are locally optimized. Blind regeneration won't help.
You MUST analyze the CONVOLUTION structure first.

## Phase 1: Mandatory Analysis
1. Call analyze_convolution_structure on the current best
2. Extract from output: Where is the infinity norm peak? What's the height distribution?
3. Determine: Is the problem excessive peak mass or insufficient L2 concentration?

## Phase 2: Targeted Modifications

**If analyzing a STEP PATTERN:**

The convolution of step functions has specific structure:
- The infinity norm is typically at the center where all steps overlap
- The L2 norm depends on the overlap integral

**Improvement strategies:**

1. **Reduce infinity norm**: 
   - Lower the tallest peak (reduces maximum convolution value)
   - Shift intervals to avoid perfect overlap at the center
   - Use asymmetric spacing

2. **Increase L2 norm**:
   - Raise heights where convolution is already high
   - Add intermediate peaks to increase overlap integral
   - Use multiple peaks with optimized spacing

3. **Combined approach**:
   - Asymmetric height ratios: [0.5h, 1.5h, 0.4h, 1.2h, 0.3h]
   - Non-uniform interval widths
   - One tall central peak with smaller asymmetric wings

**If analyzing a CONTINUOUS FUNCTION:**

1. Fine-tune existing parameters
2. Add mixture components
3. Switch to different basis (Gaussian mixture vs exponential)

## Phase 3: Evaluation Protocol

- Call evaluate_solution ONCE per DISTINCT modification
- If improvement: Drill deeper into that direction
- If no improvement: Re-analyze with analyze_convolution_structure and try a different approach
- Budget is precious: 30 evals for all iterations combined

## Key Principle
Analysis BEFORE modification. Mathematical reasoning BEFORE coding.
