---
name: systematic-mutation-protocol
description: Systematic approach to refining existing patterns. Generate mutations, evaluate, and iterate before exploring new architectures.
---

# Systematic Mutation Protocol for C₂ Maximization
## Overview
Don't jump to entirely new architectures. The seed's patterns work - refine them systematically using pattern_mutator.
## Mutation Types (in order of preference)
### 1. Height Perturbation - Increase one peak by 0.08-0.10 - Decrease all other peaks by 0.04-0.06 - Rationale: High peak boosts L2 norm; lower sides reduce infinity norm risk
### 2. Width Expansion - Expand the central/core interval by 5-10% - Keep other intervals unchanged - Rationale: Wider core increases convolution overlap, boosting L2 norm
### 3. Center of Mass Shift - Shift all interval boundaries right or left by 0.01-0.03 (1-3%) - Apply uniformly to all intervals - Rationale: Breaks perfect symmetry, can reduce constructive interference
### 4. Asymmetric Variation - Apply +6% to half the levels, -4% to the other half - Alternating pattern or based on position - Rationale: Asymmetry breaks exact symmetry, may reduce ||f★f||∞
### 5. Intermediate Level Adjustment - Increase intermediate levels by 0.05-0.08 - Keep main peaks unchanged - Rationale: Higher intermediates increase convolution support without dominating infinity norm
## Execution Strategy
1. Call pattern_mutator once at start 2. Pick first proposal, implement with edit_solution 3. Evaluate with evaluate_solution 4. If improvement: generate more variants of that mutation type 5. If no improvement after 2-3 variants: try next mutation type 6. Only after trying 3-4 mutation types without success, explore new architectures
## Key Principle
Systematic refinement > random exploration. Exhaust the current pattern's potential before abandoning it.
