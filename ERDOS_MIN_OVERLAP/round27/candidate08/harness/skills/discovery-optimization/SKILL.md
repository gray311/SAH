---
name: discovery-optimization
description: "Structural search for Erdos C5 minimization. Use generate_structural_variants for mathematically-informed\npulse patterns (triangular kernels, optimal spacing). Focus on patterns with 4-6 narrow pulses\nseparated by ~0.5 units. These minimize h(x) vs h(x+k) overlap by design."
---

# Structural Pattern Search for Erdos C5

## Core Insight
The C5 bound = max_k integral h(x)(1-h(x+k))dx is minimized when h(x) consists of
narrow, well-separated pulses. Each pulse contributes little overlap with shifted versions.

## Pattern Formula
For a pulse at center c with width w: h(x) = max(0, 1 - |x-c|/w) (triangular)
- Normalization: scale so integral(h) = 1 over [0,2]
- Expected c5 for 4 pulses at [0.2, 0.7, 1.2, 1.7] with w=0.12: ~0.35

## Workflow

Step 1: Generate candidates
- CALL generate_structural_variants(config="narrow_4pulse") or similar
- Review each candidate's c5_bound (computed via FFT, no training)

Step 2: Filter and evaluate
- KEEP only candidates with c5_bound < 0.375
- For each kept candidate, CALL evaluate_solution (full 59000 steps)
- The optimizer will refine the pulse positions/widths

Step 3: Iteration
- If none improve: try config="medium_5pulse" or "wide_6pulse"
- If still no improvement: try "bipolar_2pulse" or "central_1pulse"

## What NOT to do
- Don't train on bad initializations (c5_bound > 0.375) - gradient descent won't escape
- Don't waste evals on hyperparameter tuning when pattern is wrong
- The INITIAL FORM of h matters more than learning rate, steps, etc.
