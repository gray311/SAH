---
name: discovery-optimization
description: "Discover diverse function architectures for C\u2082 maximization. Use function_class_sampler to generate new template classes (smooth functions, multi-peaks, asymmetric constructions) and explore them systematically."
---

# Diverse Function Architecture Discovery Protocol

## Core Principle

The global optimum likely lies outside the step-function paradigm. Explore NEW function classes, not just mutations.

## Phase 1: Function Class Exploration (Primary Strategy)

### Step 1: Sample New Function Classes
- Call function_class_sampler to get diverse templates
- Focus on these classes:
  * Smooth functions: Gaussian mixtures, exponential decays with modulation, sigmoid-based constructions
  * Multi-peak patterns: 2-4 distinct peaks with varying heights and widths
  * Asymmetric constructions: Functions that break left-right symmetry intentionally
  * Piecewise polynomial: Cubic/quintic segments with continuous derivatives
  * Fourier-constrained: Functions optimized in frequency domain with positivity in time domain

### Step 2: Generate Variants Within Each Class
- For each sampled class, generate 3-5 concrete implementations
- Use probe_solution to screen variants (cheap, 30-probe budget available)
- Evaluate top 2 variants with evaluate_solution

### Step 3: Class Exhaustion Check
- If a function class yields no improvement after 2-3 variants, IMMEDIATELY switch to next class
- Don't exhaust one class before trying others

## Phase 2: Radical Step Pattern Redesign (Secondary Strategy)

Only after exhausting 4-5 diverse function classes:
- If still no improvement, redesign step patterns with:
  * Very asymmetric level heights (0.3, 1.0, 2.5, 0.8)
  * Extreme width variations (some intervals 5% of domain, others 25%)
  * Multi-modal distributions with 3-5 peaks

## Key Principles

1. Diversity > refinement: New architectures > better step patterns
2. Early probing: Screen with probe before spending evaluation budget
3. Fast switching: Move to new class when current one stalls
4. Parallel exploration: Try multiple function classes simultaneously if possible

Execution order:
1. function_class_sampler → 5 class templates
2. For each class: probe 3 variants, evaluate top 2
3. Track best across all classes
4. If after 4 classes no improvement → radical step redesign
