---
name: discovery-optimization
description: "Step-function-first optimization for C2. Exhaustive step pattern search before trying smooth functions. Uses existing probe_solution for rapid ranking."
---

# C2 Maximizer: Step-Function First Protocol

## Core Principle
Step functions are NOT trapped! The seed's 5 patterns are just starting points. 
Systematically explore step-function space before abandoning this class.

## Phase 1: Step Function Exploration (iterations 1-20)

Step 1: Analyze Current Best
- Use existing analysis methods to understand current best's structure
- Note: Where is L2 concentrated? Where is sup norm?
- For step functions: check if levels are too uniform, peaks too narrow

Step 2: Generate Step Variants (NOT smooth functions!)
- Generate 8 step-function candidates with diverse structures:
  * Vary level count: 3 levels, 4 levels, 5 levels, 6 levels, 7 levels
  * Vary height ranges: [0.5, 1.0], [1.0, 2.0], [1.5, 3.0]
  * Vary asymmetry: left-heavy, right-heavy, centered
  * Try "clustered" patterns: 2-3 high peaks with low valleys
  * Try "fractal-like" patterns: self-similar multi-scale steps

Step 3: Probe-Based Ranking
- Call probe_solution on ALL 8 candidates
- This is approximate but good for relative ranking of steps
- Call evaluate_solution on TOP 2 by probe score

Step 4: Iterate
- If neither full eval beats record: generate NEW step families
- Continue until iteration 20 or a candidate beats record

## Phase 2: Refinement or Smooth Functions (iterations 21-30)

Only if step functions beat record:
1. Refine best step with small mutations (+/-3% width, +/-0.03 height)
2. Probe all, evaluate top 1

If NO improvement after 15 iterations with steps:
1. THEN try smooth functions (Gaussian mixtures) with probe_solution
2. Only spend 3-5 evals on smooth functions

## Key Rules
- STEP FUNCTIONS FIRST: exhaustive search before trying smooth functions
- Use probe_solution for rapid ranking (approximate but sufficient)
- Smooth functions use probe_solution (approximate)
- If stuck at iteration 15: try NEW step families (fractal, mirror, clustered)
- Always analyze structure to guide step design
