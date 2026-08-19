---
name: constructive-search
description: Method for finding Erdős C₅ bounds via constructive template search. Generates diverse piecewise constant functions and uses beam search to find high-quality candidates without relying on gradient descent from random noise.
---

# Constructive Search for Erdős C₅

## Overview
This method generates piecewise constant function templates with specific mathematical structures
and searches for better C₅ bounds without relying on gradient-based optimization.

## Template Classes

### 1. Single Step Templates
Place a single block of value 1 (normalized) at various positions and widths.
- Start with block on [0,1] (normalizes to h=1 everywhere, invalid - adjust)
- Try blocks centered at 0.5, 0.75, 1.0, 1.25, 1.5
- Vary width from 0.5 to 1.5, adjusting for integral=1

### 2. Double Step Templates
Split the mass across two separated blocks.
- Classic: [0, 0.5] and [1.5, 2] with h=0.5 each (gives integral=1)
- Shifted: move blocks closer together or apart
- Different amplitudes: adjust to maintain ∫h=1

### 3. Symmetric Templates
Mirror patterns around x=1.
- Symmetric double blocks
- Symmetric single block centered at 1
- Symmetric trapezoidal patterns

### 4. Shifted Block Templates
Uniform blocks at different positions.
- Scan position from 0 to 2 in increments of 0.25
- Multiple widths: 0.4, 0.6, 0.8, 1.0, 1.2

### 5. Sinusoidal Templates
Map sine waves through sigmoid to get [0,1] values.
- h(x) = sigmoid(a * sin(ω * x + φ))
- Tune a (amplitude), ω (frequency), φ (phase)
- Normalize to ∫h=1

## Beam Search Algorithm

1. **Generate**: Create 50-200 base templates across classes
2. **Score**: Evaluate each template's c5_bound (quick computation)
3. **Select**: Keep top 10-20 candidates
4. **Mutate**: For each kept candidate:
   - Perturb breakpoint positions by ±0.05-0.1
   - Slightly adjust block widths/positions
   - Try different template class combinations
5. **Refine**: Keep top 5, repeat mutation 1-2 more times
6. **Final Eval**: Use full evaluation on final 3-5 candidates

## Key Principles

- **Diversity is key**: Templates must be structurally different
- **Constraints matter**: Always verify ∫h=1 and h∈[0,1]
- **Start coarse**: Use num_intervals=100-200, not 800
- **Limited refinement**: Don't waste evaluations on fine-tuning
- **Template variety**: Try all template classes, not just one

## Expected Performance
- Seed best: c5_bound ≈ 0.3805 (combined_score ≈ 0.999)
- Target: c5_bound < 0.3809 (combined_score > 1.0)
- This method explores the template space directly, not through gradient ascent
