---
name: discovery-optimization
description: "Seed-adapted structural exploration. Start from the proven 1.042 seed architecture, use structural_mutator to generate controlled variants (perturb heights/widths/positions), probe to rank, and climb toward better C2. Only jump to new architectures when local search exhausts potential."
---

# C2 Maximizer: Seed-Adapted Structural Exploration

## Core Principle
The seed's step functions achieve 1.042 because they are carefully tuned. Don't abandon them randomly.
Systematically explore STRUCTURAL VARIANTS by perturbing key parameters.

## Phase 1: Seed-Adapted Diversity (iterations 1-20)

Step 1: Analyze Current Best
- Call structural_mutator on your best function to get 8 variants
- Each variant perturbs: peak heights (+/-0.1), widths (+/-0.05), positions (+/-0.03)

Step 2: Probe-Based Filtering
- Call probe_solution on ALL 8 candidates (8 probes)
- Identify top 2 by probe score
- Skip full eval if probe < 1.0

Step 3: Evaluate and Learn
- Call evaluate_solution on top 2
- Track which perturbations improved score (e.g., "increasing middle height helped")
- Use this to guide next iteration's mutations

Step 4: Iterate
- Generate 8 new variants with perturbations in successful directions
- Continue until iteration 20 or improvement

## Phase 2: Focused Ascent (iterations 21-30)

1. Take best variant from Phase 1
2. Apply SMALL targeted mutations (+/-0.05 height, +/-0.02 width, +/-0.01 position) in direction of improvement
3. Probe all 5, evaluate top 1
4. If no improvement after 5 iterations: go to Phase 3

## Phase 3: Architecture Evolution (iterations 31-40)

1. Only if Phase 2 stalls: combine successful mutations into a new base function
2. Generate 4 variants with moderate perturbations (+/-0.1, +/-0.08, +/-0.05)
3. Probe all, evaluate top 2

## Key Rules
- START FROM SEED - it's already tuned!
- Use structural_mutator for controlled exploration, not random generation
- Probe 8-10 variants before spending full evals
- Track which perturbations work; reuse successful patterns
- Only jump to new families if local search exhausts after 5+ failed evals
