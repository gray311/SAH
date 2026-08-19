---
name: discovery-optimization
description: "Architecture-level search for step function optimization. Focus on structural diversity: interval count, peak count, symmetry."
---

# Architecture-Level Search Protocol for C2 Maximization

## Phase 1: Structural Diversity (iterations 1-12)

### Step 1: Generate Structurally Different Variants
Generate EXACTLY 4 variants with FOCUS on architecture:

**Variant A (Change Resolution):**
- If num_intervals = 600: try 400 (coarse) OR 900 (fine)
- Keep same step pattern type, change resolution

**Variant B (Multi-Peak Design):**
- If current has 1 peak: create 2-peak, 3-peak, or 4-peak pattern
- Use symmetric or asymmetric peak spacing

**Variant C (Asymmetric Design):**
- Shift mass to left side: concentrate peak at 0.2-0.4 of domain
- OR shift to right side: peak at 0.6-0.8 of domain

**Variant D (Narrow Peak Test):**
- Create very narrow high peak: height 2.0-2.5, width 10% of domain
- Keep surrounding steps low (0.5-0.8)

### Step 2: Probe and Evaluate
- Probe ALL 4 variants
- Evaluate TOP 1 by probe score
- If no improvement: try different architectural direction

## Phase 2: Gradient Refinement (iterations 13-22)
- Use @jax.grad on -c2_ratio objective
- Generate 2 variants following gradient direction
- Probe and evaluate best

## Phase 3: Architecture Redesign (iterations 23-30)
- Try 300 intervals with 5-level step pattern
- Try 900 intervals with 3 narrow peaks
- Probe 2-3 architectures, evaluate best
- Submit if c2 > 0.8962799441554086

## Key Rules
- Structural changes > parameter tweaks
- Use probes aggressively: 4-6 per iteration
