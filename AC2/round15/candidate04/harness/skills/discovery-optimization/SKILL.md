---
name: discovery-optimization
description: "Mathematically-grounded pattern mutation for C\u2082 maximization. Use pattern_mutator to analyze current patterns and generate improved variants within the same pattern class. Focus on systematic refinements before exploring entirely new architectures."
---

# C₂ Maximizer: Systematic Pattern Mutation Protocol
## Core Principle
Don't jump to entirely new architectures. The seed's 13 step patterns work - refine them systematically. Use pattern_mutator to generate mathematically-informed mutations.
## Phase 1: Initial Analysis (first iteration)
1. Call pattern_mutator ONCE to analyze current best pattern and get mutation proposals
2. Understand the pattern class (number of levels, height distribution, spacing)
3. Note: pattern_mutator will categorize your current pattern and suggest mutation types
## Phase 2: Systematic Mutation
Generate mutations in this order of sophistication:

**Mutation Type 1: Height Perturbation**
- Slightly adjust peak heights (±0.05-0.15) to optimize the L2/∞ ratio - Try one high peak increased, others decreased (and vice versa)
**Mutation Type 2: Width Expansion/Contraction**
- Expand or contract specific intervals by 5-10% - Expanding the "core" interval often increases ||f★f||₂² without increasing ||f★f||∞
**Mutation Type 3: Center of Mass Shift**
- Shift the entire pattern left or right by 2-3% of the domain - Can break symmetry and reduce constructive interference
**Mutation Type 4: Asymmetric Height Variation**
- Take a symmetric pattern and make heights asymmetric (e.g., 1.40, 1.45, 1.35) - Breaking exact symmetry can improve the ratio
**Mutation Type 5: Intermediate Level Adjustment**
- For multi-level patterns, adjust intermediate levels - Try: increase the "wings" relative to the "core"
## Phase 3: Exploration Strategy
1. For each mutation type, generate 2-3 concrete implementations 2. Evaluate each with evaluate_solution (probe is unreliable) 3. Track which mutation TYPE improves 4. If a mutation type works: generate more variants in that class 5. If all mutations fail for a pattern class: try the next mutation type 6. Only after trying 3-4 mutation types without success, consider new architectures
## Phase 4: Architecture Exploration (last resort)
If all mutation types exhaust on current pattern:
- Generate entirely new pattern classes (asymmetric multi-peaks, smooth transitions) - But only AFTER exhausting refinements of current working patterns
Key: Systematic refinement beats random exploration. One mutation at a time.
