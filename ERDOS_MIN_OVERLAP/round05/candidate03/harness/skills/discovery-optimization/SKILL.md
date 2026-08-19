---
name: discovery-optimization
description: "Expert-level optimization for Erd\u0151s C5 bound minimization. Uses structural pattern search, probe-based screening, and mathematical insights to find step functions beating the current best bound. Emphasizes discrete structural changes over gradient descent alone."
---

# Erdős C5 Optimization Strategy

## Core Principle
The optimal step function has a specific piecewise-constant structure. Don't rely solely on gradient descent. Instead, systematically try different structural patterns.

## Pattern Families to Explore (in order of priority):

### 1. Symmetric Threshold Patterns
- Single threshold: h(x) = 1 if x ∈ [a, b], else 0, where (b-a)=1
- Double threshold: Two rectangular pulses with specific spacing

### 2. Periodic/Quasi-Periodic Patterns
- Try sin/cos-based latent functions with careful amplitude scaling
- Test frequencies: fundamental 1, 2, 3, and combinations

### 3. Multi-Region Step Functions
- Divide [0,2] into 2-6 regions with different constant values
- Use linear programming mindset: optimize region boundaries and heights

### 4. Asymmetric Patterns
- Concentrate mass in specific subintervals
- Try h(x) concentrated on [0,1] vs [1,2] vs asymmetric splits

### 5. Hybrid: Gradient + Structural Restart
- Run gradient descent but reset to a structural pattern when improvement stalls

## Execution Protocol:

### Round 1: Baseline Analysis
1. Call analyze_structure once
2. Record the base C5 from seed

### Rounds 2-15: Pattern Exploration
For each round:
1. Pick ONE pattern family
2. EDIT: Implement that pattern with concrete parameters
3. PROBE: Immediately score the probe
4. If probe < 0.4 * base: discard, try new pattern
5. If probe >= 0.5 * base: EVALUATE (spend budget)
6. Update best if successful

### Rounds 16-30: Fine-tuning & Aggressive Search
1. Take best pattern from previous rounds
2. Try parameter perturbations (boundary shifts, amplitude tweaks)
3. Use analyze_structure_results to guide boundary placement
4. Continue probe-first screening

## Pattern Implementation Hints:

For threshold patterns:
- N_intervals = 800, dx = 0.0025
- Single pulse: set h=1 on [a, a+1], 0 elsewhere
- Double pulse: two pulses of width w1, w2 with gap

For threshold h(x):
- Use h = jnp.where(condition, 1.0, 0.0)
- Ensure integral = sum(h) * dx = 1.0

## Common Pitfalls:
- Don't spend all 30 evals on one pattern; diversify
- Probe scores ≈ 0.6-0.8 of real scores typically
- Integral constraint is critical: missing it gives validity=0
- If validity=0: check integral constraint first, then try simpler pattern

## When to Stop:
- After 25+ rounds with no improvement: try a completely different approach
- If probe consistently fails: the pattern class is unproductive
- Call finish when budget low or clear progress made
