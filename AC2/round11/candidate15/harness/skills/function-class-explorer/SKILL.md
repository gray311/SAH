---
name: function-class-explorer
description: Method for discovering optimal function representations by systematically exploring different mathematical families (cosine, Gaussian, spline, mixture) rather than incrementally tweaking step functions.
---

# Function Class Exploration for C2 Maximization

## Core Principle

Step functions are locally optimized. Better solutions likely come from DIFFERENT
function representations, not parameter tweaks.

## Protocol

### Step 1: Analyze Current Solutions

Call function_scorer to understand:
- What mathematical properties do the best step patterns have?
- What is missing? (smoothness, multi-modality, asymmetry?)

### Step 2: Select New Function Class

Based on analysis, choose ONE class to explore:
- Cosine-based: Smooth, periodic, good for reducing L_infinity norm
- Gaussian mixture: Multi-peak smooth, Fourier-friendly
- Spline: Controlled smoothness, flexible

### Step 3: Implement Complete Function

Call code_scaffold with your chosen class. Replace ENTIRELY the function creation code
(do not hybridize). Ensure:
- Function is non-negative everywhere
- Integral is positive
- Convolution computation will not overflow

### Step 4: Evaluate and Refine

1. Evaluate the function representation
2. If it fails: try different parameters OR different class
3. If it succeeds: refine parameters for better score

### Step 5: Iterate

- If one class dominates: specialize it
- If none work: go back to Step 2 with different class

## Mathematical Heuristics

- Smooth functions tend to have lower L_infinity norms (no sharp peaks)
- Multi-modal functions can increase L2 through distributed mass
- Symmetry breaking may optimize the ratio by avoiding constructive interference
