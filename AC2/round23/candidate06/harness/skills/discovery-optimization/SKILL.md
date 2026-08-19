---
name: discovery-optimization
description: "Function-class escape protocol for C2 maximization. Hybrid construction, Fourier-space refinement, and architectural search. Escape step-function local optimum."
---

# C2 Maximizer: Function-Class Escape Protocol

## Core Principle
Step functions saturate at ~0.89628. Escape to HYBRID functions: smooth transitions, multi-scale superposition, or Fourier-optimized designs.

## Phase 1: Hybrid Construction (iterations 1-10)

Step 1: Analyze Structure
- Call analyze_structure on best function
- Extract: peak positions, edge sharpness, scale content

Step 2: Generate Hybrids
Create EXACTLY 3 variants:

Variant A (Smooth Edges):
- Replace sharp step edges with sigmoid transitions
- Use: f = sigmoid(-2.0*(x - edge_pos) / smooth_width)
- smooth_width = peak_width * 0.1

Variant B (Multi-scale):
- Superimpose scaled copies of base pattern
- f = base + 0.3 * scale(base, scale=2.0)
- Add low-frequency component

Variant C (Polynomial Modulation):
- Multiply step by smooth decay envelope
- f = step * (1 - |x-center|/L)^p, p=1.0-2.0

Step 3: Probe and Evaluate
- Probe all 3 variants
- Evaluate top 1
- If no improvement after 3 iterations: switch to Phase 2

## Phase 2: Fourier-Space Refinement (iterations 11-20)

Step 1: Fourier Analysis
- Analyze current best in frequency domain
- Identify dominant frequencies

Step 2: Fourier Optimization
- Generate variants by: (a) boost low-frequency content, (b) add controlled high-frequency modulation, (c) phase-shift components
- Ensure inverse FFT stays non-negative

Step 3: Probe and Evaluate
- Probe 2 Fourier variants
- Evaluate best
- If plateaued: switch to Phase 3

## Phase 3: Architectural Search (iterations 21-30)

Step 1: Radical Re-architecture
- Try: spline-like smooth functions, mixture-of-components, asymmetric multi-peak
- Complete reimagining, not parameter tweaks

Step 2: Final Evaluation
- Probe 2-3 radical designs
- Evaluate best, submit if c2 > 0.8962799441554086

## Key Rules
- Call analyze_structure EVERY iteration
- NEVER stay in parameter-refinement mode - escape to new function families
- Use probes aggressively: 4-6 probes before any eval
- At iteration 10+: if plateaued, switch phases immediately
- Temperature 1.0 encourages diverse architectural exploration
