---
name: discovery-optimization
description: "Step-pattern search within fixed grid. Generate diverse multi-level step functions, use probes to rank before full eval. NEVER try smooth functions - step functions win by creating sharp convolution peaks."
---

# C2 Maximizer: Step Pattern Search Protocol

## Core Principle
Step functions create sharp peaks in f*f convolution, maximizing C2. Smooth functions smear these peaks and UNDERPERFORM. STICK TO STEPS.

## Phase 1: Step Pattern Diversification (iterations 1-20)

Step 1: Analyze Current Best
- Examine the best step pattern: How many levels? What are heights? Where are transitions?
- Note: The seed has 5 patterns with 2-5 levels. Try MORE levels (7-12) or ASYMMETRIC structures.

Step 2: Generate Step Variations
- Create 5-7 NEW step patterns by varying:
  * Number of levels: Try 7, 9, 11 levels (more granularity than seed's 2-5)
  * Asymmetry: High-low-high vs low-high-low vs all levels ascending
  * Support: Narrow (50% width) vs wide (80% width)
  * Heights: Try extreme values (0.3-3.0 range), e.g., [0.5, 1.0, 2.5, 1.0, 0.5]
- Pattern templates:
  * Pyramid: [low, medium, HIGH, medium, low, ...]
  * Mountain: [low, low, HIGH, HIGH, low, low]
  * Asymmetric: [very_low, medium, HIGH, medium, medium, low]

Step 3: Probe-Based Filtering
- Call probe_solution on ALL 5-7 candidates (5-7 probes used)
- Call evaluate_solution on TOP 2 by probe score
- If probe score < 1.0: skip full eval, try next pattern

Step 4: Iterate
- Continue until iteration 20 or one beats record
- Generate completely new step architectures if stuck

## Phase 2: Targeted Refinement (iterations 21-30)

Only if a step pattern beat the record:
1. Take the best step pattern
2. Try LOCAL mutations:
   - Adjust ONE level height by ±15%
   - Shift ONE boundary by ±2 grid positions
   - Add/remove ONE level
3. Probe all 3 variants, evaluate top 1
4. If no improvement after 5 iterations: go back to Phase 1 with NEW architectures

## Key Rules
- STICK TO STEP FUNCTIONS - they maximize C2 by creating sharp convolution peaks
- Use 30 probes to explore 12-20+ step variants before full evaluations
- If iteration 10+: try NEW step architectures (different level counts)
- Always ensure f >= 0 using jax.nn.relu or jnp.maximum
