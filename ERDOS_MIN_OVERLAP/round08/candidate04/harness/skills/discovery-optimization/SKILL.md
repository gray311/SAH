---
name: discovery-optimization
description: "Erd\u0151s C\u2085 optimization harness. Uses constructive search over piecewise constant templates with mathematical structure. Prioritizes template generation and beam search over gradient-based optimization."
---

# Erdős C₅ Optimization: Constructive Search Strategy

## Problem
Minimize: max_k ∫₀² h(x)(1-h(x+k))dx
Subject to: h:[0,2]→[0,1], ∫₀² h(x)dx = 1

## Why Gradient Descent Fails
- The objective landscape is highly non-convex
- Random initializations lead to poor local optima
- The seed's multi-restart Adam gets trapped, never escaping

## Winning Strategy: Constructive Template Search

### Step 1: Generate Diverse Templates
Create piecewise constant functions with specific mathematical structures:
- Single interval: h=1 on [0,1], h=0 elsewhere (then normalize)
- Double intervals: split mass across multiple regions
- Symmetric patterns: mirror images around x=1
- Shifted patterns: uniform blocks at different positions
- Sinusoid-based: h(x) = sigmoid(a*sin(ωx+φ)) with tuned parameters

### Step 2: Enumerate Parameters
For each template class, vary:
- Number of intervals (2-10 breakpoints)
- Breakpoint positions (quantized to avoid redundancy)
- Amplitudes (constrained to [0,1] and integral=1)

### Step 3: Beam Search
1. Generate 50-100 base templates
2. Score each, keep top 10
3. Mutate top candidates (perturb breakpoints, slightly adjust amplitudes)
4. Keep top 5, repeat 2-3 levels
5. Use full evaluation only on final candidates

### Step 4: Optional Fine-Tuning
Only if you have a promising template:
- Use gradient descent to refine the template's breakpoint positions
- Keep num_intervals moderate (100-200), not 800+
- Use strong integral constraint to maintain feasibility

## Key Principles
- **Diversity > Optimization**: Generate many structurally different templates
- **Constraints First**: Ensure ∫h=1 before evaluating
- **Coarse Structure**: Find good piecewise constant structure first, then refine
- **Evaluation Budget**: Use sparingly on the best 3-5 candidates

## When to Use Tools
- construct_candidates: Generate fresh templates at the start or when stuck
- edit_solution: Mutate promising templates or try new template classes
- evaluate_solution: Evaluate final candidates

## Expected Outcome
The seed's best templates achieve c5_bound ≈ 0.3805 (combined_score ≈ 0.999). You need to find templates achieving c5_bound < 0.3809 for combined_score > 1.0.
