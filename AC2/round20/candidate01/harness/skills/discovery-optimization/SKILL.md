---
name: discovery-optimization
description: "Structured step-pattern optimization. The current best (0.8963) is achieved by sophisticated \nmulti-level step functions. Do NOT change to smooth families. Instead, perturb the existing \nstep patterns (small height/width changes) while preserving their multi-level structure. \nUse probes to explore 10+ step variants before full evaluation."
---

# C2 Maximizer: Structured Step-Pattern Refinement Protocol

## Core Principle
The current best (0.8962799441554086) is achieved by MULTI-LEVEL STEP FUNCTIONS, not smooth functions.
Smooth functions (Gaussian, B-spline, oscillatory) have WORSE L2/inf ratios due to their spread.
Your job is to PERTURB and RECOMBINE the existing step patterns, NOT to change families.

## Phase 1: Step-Pattern Refinement (iterations 1-20)

Step 1: Analyze Current Pattern
- Call analyze_step_structure on your best function
- Note: How many levels? What are the heights? Where are the transitions?
- Typical seed patterns have 3-5 levels with heights ranging from 0.5-2.5

Step 2: Generate Perturbed Variants
- Call generate_step_variants to get 3-5 PERTURBED variants of the SAME pattern type
- PERTURBATION GUIDELINES (CRITICAL):
  * Height changes: +/- 0.1 to 0.3 (not +/- 50%)
  * Width changes: +/- 3% to 5% of segment length (not drastic shifts)
  * Keep the MULTI-LEVEL STRUCTURE intact (don't collapse to single step)
  - Preserve the overall "shape" - the perturbations should be subtle refinements
- Example: If pattern has heights [0.80, 1.60, 2.00, 1.40, 0.90], try [0.85, 1.65, 1.95, 1.45, 0.90]

Step 3: Probe-Based Filtering
- Call probe_solution on ALL 3-5 variants (5 probes total)
- Call evaluate_solution on TOP 2 by probe score
- If probe score < 1.0, skip full eval and try next variant

Step 4: Iterate
- If neither full eval beats record: generate 3-5 MORE PERTURBED variants
- Use probe_solution on all new candidates
- Evaluate top 1-2
- Continue until iteration 20 or a variant beats record

## Phase 2: Hybrid Construction (iterations 21-30)
Only if a new step pattern beat the record:
1. Analyze its structure (how many levels? what heights?)
2. Try HYBRID construction: combine height sequences from two different seed patterns
3. Probe and evaluate

## Key Rules
- STAY IN STEP-LANDSCAPE: Do NOT generate Gaussians, splines, oscillatory functions
- PERTURB, DON'T REPLACE: Keep multi-level structure, vary heights/positions subtly
- Use probes to explore 10-15 step variants before full evaluations
- Small perturbations (10-20% changes) are better than large jumps
- Always analyze step structure to guide perturbations

## Why This Works
The seed's step patterns are already sophisticated. The optimization space is CONTINUOUS 
variations of these patterns, not discrete jumps to new function families. Small perturbations
can fine-tune the L2/inf ratio without losing the structural advantages of multi-level steps.
