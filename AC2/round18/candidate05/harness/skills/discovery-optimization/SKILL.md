---
name: discovery-optimization
description: "Systematic step-function search. Seed achieves 1.042 - explore step-space with valid, executable edits. Use controlled perturbations, probe filtering, iterative refinement."
---

# Systematic Step-Function Search

## Core Insight
Seed achieves 1.042 with step functions - architecture is viable. Don't abandon for untested families. Systematically perturb parameters with VALID edits.

## Phase 1: Structured Variation (iterations 1-12)

Step 1: Analyze Current Best
- Examine best function: how many steps, what heights, where boundaries?
- Pattern: f = f.at[int(0.10*n):int(0.30*n)].set(h1).at[int(0.30*n):int(0.50*n)].set(h2)...]

Step 2: Generate 3 Controlled Variants

   Variant A (Height):
   - Pick one step: new_h = h * 0.9 OR h * 1.1
   - Code: f = f.at[start:end].set(new_h)

   Variant B (Position):
   - Shift boundary: int(0.30*n) -> int(0.27*n) or int(0.33*n)
   - Code: f = f.at[int(0.27*n):int(0.73*n)].set(h)

   Variant C (Width/Interval):
   - Adjust interval: if end-start=200, try 180 or 220

Step 3: Probe-Based Filtering
- Call probe_solution on ALL 3 variants
- Skip full eval if probe < 1.0
- Evaluate TOP 2 by probe

Step 4: Iterative Refinement
- Best program becomes new base
- Generate fresh variants from it
- Repeat until iteration 12 or improvement

## Phase 2: Combinatorial (iterations 13-24)
1. Take best from Phase 1
2. Generate 4 variants: combinations of height+pos, pos+width, etc.
3. Probe all, evaluate top 2
4. If no improvement after 5 iterations: Phase 3

## Phase 3: Finetuning (iterations 25-30)
1. Fine perturbations: +/-3% height, +/-2% position
2. Generate 2 variants
3. Probe, evaluate top 1
4. If stuck: reset to seed

## Valid Edit Syntax
- CORRECT: f.at[int(0.25*n):int(0.75*n)].set(1.40)
- WRONG: f.at[0.25*n:0.75*n].set(1.40)  # needs int()
- ALWAYS add: f = jax.numpy.maximum(f, 0.001) for non-negativity

## Execution
- After each eval, update best_f
- Generate next variants from current best, not seed
- Use all 30 probes before full evals
