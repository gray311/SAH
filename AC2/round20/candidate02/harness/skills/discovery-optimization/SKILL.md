---
name: discovery-optimization
description: "Step-pattern optimization with tail exploration. Diagnose step structure, generate variants with different tail behaviors (asymmetric, extended support), use all 30 probes to explore many step patterns before evaluation. Stay in step-function space."
---

# C2 Maximizer: Step-Pattern Optimization Protocol

## Core Principle
The seed's step-function approach (1.042 = 1.042 * 0.8962799441554086) WORKS. Don't abandon it for Gaussian mixtures or splines. Focus on:
1. Finding better step patterns (already proven to work)
2. Exploring tail behaviors (longer support, asymmetric decay)
3. Using all 30 probes to explore diversity

## Phase 1: Pattern + Tail Exploration (iterations 1-20)

Step 1: Analyze Current Step Pattern
- Call analyze_step_patterns on your best function
- Note: How many steps? What's the support range? Where is ||f*f||_∞ located?
- If support is [-3, 3]: consider extending to [-4, 4]
- If asymmetric: try the opposite asymmetry

Step 2: Generate Step Variants with Tail Modifications
Call generate_candidates with:
- tail_mode: "extended", "asymmetric_left", "asymmetric_right", "double_tailed"
- Try 3-5 different variants

Step 3: Probe-Based Filtering
- Call probe_solution on ALL variants (use all 30 probes)
- Only evaluate variants with probe score >= 1.0
- If probe < 1.0, skip full eval

Step 4: Iterate
- If no improvement after 10 iterations: generate patterns with EXTENDED TAILS
- Continue until iteration 20 or improvement

## Phase 2: Focused Refinement (iterations 21-40)

1. Take best pattern from Phase 1
2. Generate 3 variants with SMALL mutations:
   - Adjust one interval boundary by ±3%
   - Adjust one height by ±0.15
   - Slightly shift peak position
3. Probe all, evaluate top 1
4. If no improvement after 5 iterations: return to Phase 1 with DIFFERENT tail

## Key Rules
- STAY IN STEP-FUNCTION SPACE - it works!
- Use 30 probes to explore 15-20+ variants before full evaluations
- Focus on TAIL BEHAVIORS: extended support, asymmetric decay
- Call analyze_step_patterns at iterations 0, 8, 20, and when stuck
- NEVER generate Gaussian, B-spline, or oscillatory functions
