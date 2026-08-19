---
name: family-exploration-protocol
description: Systematically explore diverse function families (Gaussian hybrids, splines, polynomial cutoffs) before refining. Escape step-function local optima.
---

# Family Exploration Protocol for C2 Maximization

## Core Principle
The seed step function is a LOCAL OPTIMUM within the step-function class.
To exceed C2 = 0.89628, you MUST explore NEW FUNCTION ARCHITECTURES.

## Phase 1: Diverse Family Exploration (iterations 1-10)

Step 1: Generate New Families
- Call generate_family_variant 1-2 times to get different architectures
- Types to try:
  * Gaussian hybrid: step x Gaussian envelope
  * Spline-based: piecewise polynomial with smooth transitions
  * Polynomial cutoff: step function with polynomial-smoothed edges
  * Hybrid step: core step + Gaussian tails
  * Fractal-like: multi-scale self-similar structure

Step 2: Rapid Screening
- Call probe_solution on 2-3 different families
- Rank by probe score

Step 3: Initial Evaluation
- Call evaluate_solution on TOP 1 that beats current c2

## Phase 2: Hybridization & Tuning (iterations 11-20)

Step 1: If new family outperforms:
- Refine its parameters with small perturbations (plus-minus 5 percent)
- Try hybridizing with step-function base

Step 2: Probe 2-3 hybrid variants
- Evaluate best

## Phase 3: Exotic Architecture Search (iterations 21-30)

Step 1: Generate more exotic families (Fourier-optimized, multi-modal)
Step 2: Use gradients on promising candidates for final tuning
Step 3: Submit if c2 > 0.8962799441554086

## Key Rules
- Step functions are a STARTING POINT, not the answer
- Always try new architectures before refining existing ones
- Use probes to screen 5+ different families before full eval
- Temperature 1.2 encourages architectural diversity
