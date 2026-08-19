---
name: discovery-optimization
description: "Mathematically-grounded pattern mutation with verification. Use pattern_mutator to generate proposals, then mutation_verifier to validate before editing. Follow one-mutation-at-a-time protocol."
---

# C₂ Maximizer: Verified Single-Mutation Protocol
## Core Principle
ONE MUTATION PER EDIT. The seed's patterns are fragile. You MUST:
1. Get ONE mutation proposal from pattern_mutator 2. VERIFY it with mutation_verifier (mandatory - don't skip!) 3. Implement ONLY that mutation with edit_solution 4. Evaluate with evaluate_solution 5. Repeat with same mutation TYPE or try next type if no improvement
## Mutation Types (try in order)
### Type 1: Single Height Perturbation - Change ONE peak height by ±0.05-0.10 - Example: change 1.40 to 1.45 (only one value!) - Rationale: Tests sensitivity of L2/∞ ratio to individual peak heights
### Type 2: Single Width Adjustment - Change ONE interval boundary by 3-5% - Example: change int(0.25*n) to int(0.26*n) (only one boundary!) - Rationale: Tests how convolution support responds to width changes
### Type 3: Single Center Shift - Shift ONE boundary pair (start and end together) by 0.01-0.02 - Example: change both 0.25n and 0.75n to 0.26n and 0.76n - Rationale: Tests symmetry breaking
### Type 4: Asymmetric Pair Adjustment - Change two adjacent heights with opposite perturbations - Example: change 1.40 to 1.43 and 1.45 to 1.42 (maintain sum, create asymmetry) - Rationale: Tests how asymmetry affects infinity norm
## Verification Step (MANDATORY)
Before every edit, call mutation_verifier. It will: - Check syntax validity of the proposed edit - Verify the change is semantically meaningful (not just noise) - Confirm the edit matches the requested mutation type - Return the exact SEARCH/REPLACE code to use with edit_solution
## Execution Flow
Iteration 1-3: Try mutations of Type 1 (height perturbation) - For each: pattern_mutator → mutation_verifier → edit → evaluate - If improvement: continue with more Type 1 variants - If no improvement after 3: move to Type 2
Iteration 4-6: Try mutations of Type 2 (width adjustment) - Same pattern: pattern_mutator → mutation_verifier → edit → evaluate - If no improvement after 3: move to Type 3
Iteration 7-9: Try mutations of Type 3 (center shift) - Same pattern - If no improvement after 3: move to Type 4
Iteration 10+: If all types exhausted, call pattern_mutator for completely new architecture - Only after systematic refinement fails for all 4 types
