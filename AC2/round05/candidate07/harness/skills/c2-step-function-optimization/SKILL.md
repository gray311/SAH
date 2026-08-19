---
name: c2-step-function-optimization
description: Specialized playbook for maximizing C₂ via step-function representations and mathematical insights.
---

# C₂ Optimization: Step-Function Dominant Strategy

## Core Principle

Step functions (piecewise-constant) are the mathematical champions for C₂. The AlphaEvolve record (0.8963) uses step functions. Your goal: beat this in C₂ score.

## Why Step Functions Win

- Sharp transitions concentrate ||f★f||₂ without spreading mass
- Easy to optimize heights and widths
- Avoids the "smoothing penalty" of continuous functions

## Execution Protocol

### Phase 1: Baseline Analysis

1. Call analyze_c2_function() to understand your current representation
2. If smooth (Gaussian/exponential): Immediately convert to step approximation
3. If multi-modal: Check symmetry, enforce if absent

### Phase 2: Step-Function Exploration

For EACH of these variants, call analyze_c2_function → probe 5+ times → eval top 2:

**A. Asymmetric 2-Step**
- Left support: 40% of domain, height 1.0
- Right support: 30% of domain, height 1.4-1.5
- Gap: 30%

**B. Symmetric 3-Step**
- Three levels at positions ~0.33n, ~0.66n
- Heights: [1.0, 1.2, 1.5]

**C. Optimized Single Step**
- Width: 50% of domain
- Height: 1.35-1.45
- Centered or slightly offset

**D. 4-Step Multi-Modal**
- Two peaks, 2-3 steps per side
- Symmetric configuration

### Phase 3: Refinement

After probe ranking:
- Take top 2 by probe score
- Evaluate each with 2 seeds
- If no improvement: Call analyze_c2_function with NEW family

### Critical Rules

- Max 3 full evaluations without re-analysis
- Always probe ≥5 variants before first eval
- Never try Gaussian/exponential as primary strategy
- Step functions are your friend

## Expected Progression

Seed (1.0267) → Step function variants (1.03-1.04+) → Optimized step (1.05+)
