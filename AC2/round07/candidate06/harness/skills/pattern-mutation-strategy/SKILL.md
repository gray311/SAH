---
name: pattern-mutation-strategy
description: Playbook for Phase 1 (new configs) and Phase 2 (pattern mutation) C2 optimization. Phase 1 uses step_config_generator to explore. Phase 2 uses pattern_mutation_tool to fine-tune the 13 seed patterns which are near-optimal.
---

# C2 Maximization: Two-Phase Strategy

## Phase 1: Exploration (Iterations 1-3)
Goal: Discover new step function families

1. CALL step_config_generator
   - Try symmetric (2-4 steps), asymmetric (2-5 peaks)
   - Vary heights: 0.5-2.0, widths: 0.15-0.45
2. Create step functions with jnp.piecewise
3. Probe 3-5 variants
4. Evaluate top 2
5. Track best score

## Phase 2: Refinement (Iteration 4+ or if score > 1.030)
Goal: Fine-tune SEED PATTERNS (0-13) which are near-optimal

1. CALL pattern_mutation_tool
   - Select pattern_idx from 0-13
   - Mutate heights: ±5-15%
   - Mutate positions: ±10-20%
   - Generate 3-5 variants
2. Create step functions
3. Probe 3-5 variants
4. Evaluate top 2
5. Continue until score > 1.030 or budget exhausted

## Critical Rules
- MAX 4 full evaluations TOTAL
- Phase 1: step_config_generator
- Phase 2: pattern_mutation_tool (after iter 3 or score > 1.030)
- Probe 3-5 before any eval
- Seed patterns 0-13 are PROVEN - we optimize, don't replace
- TRUE step functions only (constant, not linear)
