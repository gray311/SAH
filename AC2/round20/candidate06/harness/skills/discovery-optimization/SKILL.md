---
name: discovery-optimization
description: "Diverse architecture exploration with convolution analysis. Diagnose step-function \nlimitations, generate fundamentally different function families, use probes to explore \n10+ candidates before full evaluation. Jump between architectures rather than refining \none type sequentially."
---

# C2 Maximizer: Diverse Architecture Exploration Protocol

## Core Principle
The step-function local optimum cannot be escaped by small mutations. You MUST 
explore fundamentally different function architectures in parallel, using probes to 
filter before full evaluation.

## Phase 1: Diagnostic + Diverse Generation (iterations 1-15)

Step 1: Analyze Current Best
- Call analyze_convolution_profile on your best function
- Note: Where is ||f*f||2^2 concentrated? Where is ||f*f||_inf?
- If L2 is concentrated in a narrow region and sup is at peak: need wider support
- If sup is too high relative to L2: need smoother transitions

Step 2: Generate Diverse Candidates
- Call generate_candidates to get 5 proposals across DIFFERENT families:
  * Gaussian mixtures: smooth multi-peaked functions
  * B-spline: flexible smooth transitions with optimized control points
  * Oscillatory decay: (1 + alpha*cos(beta*x))*exp(-gamma*|x|) for structured convolution
  * Piecewise-linear: controlled smoothness
  * Multi-level steps: refined asymmetric step structures

Step 3: Probe-Based Filtering
- Call probe_solution on ALL 5 candidates (5 probes total)
- Call evaluate_solution on TOP 2 by probe score
- If probe score < 1.0 (worse than seed), skip full eval and try next candidate

Step 4: Iterate
- If neither full eval beats record: generate 5 MORE diverse candidates
- Use probe_solution on all new candidates
- Evaluate top 1-2
- Continue until iteration 15 or a candidate beats record

## Phase 2: Focused Refinement (iterations 16-30)

Only if a new architecture beat the record:
1. Analyze its convolution profile
2. Generate 3 variants with SMALL mutations (+/-5% width, +/-0.05 height, +/-10% weight)
3. Probe all, evaluate top 1
4. If no improvement after 5 iterations: go back to Phase 1

## Key Rules
- PARALLEL DIVERSITY > SEQUENTIAL REFINEMENT
- Use 30 probes to explore 10-15+ variants before full evaluations
- NEVER refine the same architecture for 3+ iterations
- If iteration 10+: generate completely new families
- Always analyze convolution profile to guide architecture choice
