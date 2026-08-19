---
name: enhanced-initialization-strategy
description: Method playbook for augmenting the seed's optimizer with better initialization strategies. Focus on hybrid functions that blend step and smooth characteristics.
---

# Enhanced Initialization Strategy for C2 Maximization

## Objective

Maximize C2 > 1.02665 by enhancing the seed's JAX optimizer, not replacing it.

## Why Enhance Rather Than Replace?

- Seed's optimizer uses powerful gradient descent (40,000 steps)
- Seed already has 9 diverse initializations
- Manual step construction breaks the continuous optimization signal
- Our goal: better seeds, not new architecture

## Step 1: Analyze Current State

1. Check seed's best C2 (baseline: 1.02665)
2. Note what initialization performed best
3. Identify what's missing (likely exploration diversity)

## Step 2: Generate Hybrid Initializations

Use hybrid_function_creator tool:

### Option A: Smooth Steps
- 2-3 step levels with smooth (linear) transitions
- Better differentiability than pure steps
- Try: heights [1.0, 1.3, 0.9], positions [0.1, 0.4, 0.7]

### Option B: Plateau with Sloped Edges
- Flat top region (like step) but gradual slopes
- Combines step benefits with smooth optimization
- Try: plateau at 0.4, slopes over 0.2 on each side

### Option C: Multi-Hump
- 3-4 peaks of varying widths/heights
- Explores richer function space than single peak
- Try: centers at 0.2, 0.4, 0.6; heights [1.0, 1.3, 1.1]

## Step 3: Probe-Based Selection

1. Create 3-5 hybrid initializations
2. For each:
   - Patch into seed's _create_multi_start
   - Run optimizer for 1000 steps (partial)
   - Call probe_solution
   - If probe C2 > 1.02665: proceed to full run
   - If probe C2 <= 1.02665: discard

## Step 4: Full Optimization

1. Take top 2 candidates from probing
2. Run seed's optimizer for full 40000 steps
3. Call evaluate_solution
4. Track which hybrid type performed best

## If No Progress

- Try polynomial decay: f(x) = exp(-alpha*|x|^beta) with JAX optimization
- Try B-spline based representations
- Try the seed's existing reinitialization strategy more aggressively

## Critical Rules

- MAX 4 full evaluations
- ALWAYS use seed's optimizer (gradient descent)
- Use hybrid_function_creator for structured exploration
- Probe after partial optimization, not on raw constructions
- Diversify across 3+ hybrid types before concluding
