---
name: diverse-architecture-protocol
description: Systematic exploration of diverse function architectures. Sample new classes, generate variants, probe, evaluate, and switch classes quickly.
---

# Diverse Architecture Discovery Protocol

## Phase 1: Rapid Class Sampling

1. Call function_class_sampler to get 5 diverse function class templates
2. These templates represent STRUCTURALLY DIFFERENT function types (not step pattern variations)

## Phase 2: Exploratory Variant Generation

For EACH function class:

a. Generate 3-5 concrete variants with different parameter settings
   - Sample from the parameter ranges provided
   - Try asymmetric combinations, boundary values, and mid-range values

b. Use probe_solution to screen all variants
   - This is cheap and you have 30 probe budget
   - Rank variants by approximate score

c. Evaluate the TOP 2 variants with evaluate_solution
   - Only 2 evaluations per class maximum
   - Track which class type performed best

## Phase 3: Class Switching Strategy

- If a function class yields no improvement after evaluating 2 variants:
  → IMMEDIATELY switch to the next function class
- Don't exhaust one class before trying others
- After 4-5 classes with no improvement:
  → Try radical step pattern redesigns (last resort)

## Key Principles

- Diversity first: New architectures > refined step patterns
- Probe aggressively: Use probe budget to screen many variants
- Fast switching: Move to new class when current one stalls
- Parallel tracking: Keep track of best variant across all classes

Execution template:
1. function_class_sampler → 5 classes
2. For each class (1-5):
   - Generate 3-5 variants
   - Probe all → rank
   - Evaluate top 2
   - Record best for this class
3. If after 4 classes no improvement → radical step redesign
