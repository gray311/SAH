---
name: discovery-optimization
description: "Systematic step-function refinement for C\u2082 maximization. Mutate seed patterns with small, targeted changes: height perturbation, width adjustment, asymmetry induction. Use probes to filter before full evaluation."
---

# C₂ Maximizer: Step-Function Refinement Protocol

## Phase 1: Pattern Selection (first iteration)

1. Review the 13 seed patterns (0-12) in the EVOLVE-BLOCK.
2. Pick ONE pattern to refine (start with pattern 0: high peak single step).

## Phase 2: Targeted Mutation Generation

For your chosen pattern, create 2-3 variants with these mutation types:

**Mutation A: Height Fine-Tuning**
- Identify peak heights in the pattern
- Adjust by small amounts: ±0.02 to ±0.08
- Example: if heights are [1.40, 1.50, 1.40], try [1.42, 1.50, 1.38]

**Mutation B: Width Optimization**
- Expand core intervals by 3-6%, contract wings by similar amount
- Example: if pattern has [0.25n, 0.75n], try [0.24n, 0.76n]

**Mutation C: Asymmetry Induction**
- Break symmetry in symmetric patterns
- Example: [1.40, 1.50, 1.40] → [1.42, 1.50, 1.38]
- Example: multi-level [0.70, 1.30, 1.70, 1.30, 0.70] → [0.72, 1.32, 1.68, 1.28, 0.72]

## Phase 3: Probe-Based Selection

1. Call generate_step_variants to get 3 concrete code implementations
2. Call probe_solution on each variant (use all 30 probes wisely)
3. Select top 1-2 variants by probe score
4. Call evaluate_solution ONLY on the best 1-2

## Phase 4: Iteration & Pattern Switching

- Track which mutation type works best (height, width, or asymmetry)
- If current pattern yields no improvement after 3 iterations:
  - Switch to a different seed pattern (try pattern 1-12)
  - Reset mutation strategy for the new pattern
- Continue until eval budget exhausted or record broken

## Key Principles

- Small, targeted mutations > random exploration
- Probes filter bad variants before wasting full evaluations
- Systematic pattern cycling > getting stuck on one pattern
- Keep trying the same mutation type if it works; switch if it fails
