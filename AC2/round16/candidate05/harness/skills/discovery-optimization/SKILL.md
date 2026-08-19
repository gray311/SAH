---
name: discovery-optimization
description: "Systematic step-function refinement protocol with targeted mutations (height, width, asymmetry, bump) followed by architecture exploration if needed."
---

# C₂ Maximizer: Systematic Refinement Protocol

## Core Principle
The seed's 5 step patterns are a solid foundation. Beat the record by SYSTEMATICALLY refining them first, not by random exploration.

## Phase 1: Systematic Mutation (iterations 1-25)

### Step 1: Identify Best Pattern
After generating 5 variants, find which has highest combined_score. Focus mutations on THAT pattern.

### Step 2: Mutation Types (apply one type at a time)

**Type A: Height Perturbation**
- Target: Optimize L2/∞ ratio by adjusting peaks
- Action: Change ONE peak height by +0.03 to +0.08, or reduce others by -0.03 to -0.08
- Example: Base pattern with heights [1.50, 1.45] → [1.55, 1.40] or [1.50, 1.45, 1.38]

**Type B: Width Adjustment**
- Target: Expand the "core" interval to increase ||f★f||₂²
- Action: Change one interval boundary by +3% to +6%
- Example: interval 0.22n → 0.26n (expand by ~18%)

**Type C: Asymmetry**
- Target: Break perfect symmetry to reduce constructive interference
- Action: Make heights unequal: [h, h+δ, h-δ] where δ ∈ [0.03, 0.08]
- Example: [1.50, 1.54, 1.46] instead of [1.50, 1.50, 1.50]

**Type D: Bump Modification** (for patterns with bumps: 0, 1, 2, 3, 4)
- Target: Adjust bump contributions to convolution
- Action: Increase one bump height by +0.05 to +0.10, or reduce width by -5%
- Example: bump_height 0.65 → 0.70, or 0.22n → 0.20n

### Step 3: Execution
1. For your best pattern, apply ONE mutation type
2. Generate 2-3 concrete variants with different magnitudes
3. Probe all variants (use probe_solution)
4. Evaluate top 2 by probe score
5. If either improves combined_score: continue refining same pattern/type
6. If neither improves: try next mutation type

## Phase 2: Architecture Exploration (iterations 26-45)

Only if all 4 mutation types exhaust on current best pattern:

1. Generate completely new architectures via generate_candidates:
   - Gaussian mixture: weighted sum of Gaussians with optimized μ, σ, weights
   - B-spline: 30-50 control points with softplus positivity, optimize knots
   - Oscillatory decay: (1 + α cos(βx)) * exp(-γ|x|), optimize α, β, γ
   - Fine-grained multi-level: 10-15 levels with asymmetric heights/positions

2. For each architecture, generate 2 variants with different parameters
3. Probe all, evaluate top 2

## Phase 3: Renewed Refinement (iterations 46-60)

If any new architecture beats record: apply Phase 1 systematic refinement to it.

## Key Rules
- ONE mutation at a time. Track which type works.
- Use probes to filter before full evaluation (30 probes = rank many variants cheaply).
- Don't exhaust one architecture >5 iterations without trying new types.
- After 4 failed mutation types: switch to architecture exploration.
- JAX mutability: use f = f.at[start:end].set(value) for all edits.
