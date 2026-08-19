---
name: c5-multi-start
description: Execute multi-start optimization - generate variants, short optimize, probe-select, full optimize. Use this skill to implement the 5-10 variant strategy with probe guidance.
---

# Multi-Start C5 Optimization Playbook

## Overview
Execute a multi-start search to escape local minima. Generate 8+ diverse initializations, short-optimize each, probe to rank, then fully optimize the best candidate.

## Step-by-Step Implementation

### Step 1: Generate Variants
Call generate_variants() to get 8 diverse initializations:
- bimodal_pos0.2, bimodal_pos0.8: Mass at left/right
- shifted0.3, shifted0.7: Mass concentrated at different positions
- uniform: Flat start with noise
- alternating: Sin-wave pattern
- perturbed versions of the above

### Step 2: Short Optimization Loop
For each variant (8 total):
  latent = variant_latent  # from generate_variants
  opt_state = optimizer.init(latent)
  for step in range(5000):
      loss, grads = value_and_grad(obj_fn)(latent)
      updates, opt_state = optimizer.update(grads, opt_state)
      latent = apply_updates(latent, updates)

Parameters: lr=0.01, penalty=1500

### Step 3: Probe Selection
After short optimization, use ctx.probe() to score each candidate:
  candidates = []
  for latent, variant_name in optimized_variants:
      probe_score = ctx.probe()
      candidates.append((variant_name, probe_score, latent))

  candidates.sort(key=lambda x: x[1])  # lowest c5 first

Pick top 3 candidates for full optimization.

### Step 4: Full Optimization
For top 3 candidates, run longer optimization (15000-25000 steps):
  for top_latent in best_3_candidates:
      opt_state = optimizer.init(top_latent)
      for step in range(20000):
          # Grad descent with possibly decaying lr
          loss, grads = value_and_grad(obj_fn)(top_latent)
          updates, opt_state = optimizer.update(grads, opt_state)
          top_latent = apply_updates(top_latent, updates)

Parameters: Start lr=0.01, decay to 0.003 over steps, penalty=1500-2000

### Step 5: Final Evaluation
Take the best from full optimization, ensure integral=1 exactly:
  final_h = sigmoid(best_latent)
  integral = sum(final_h) * dx
  final_h = final_h / integral

Then call ctx.evaluate() and submit.

## Key Principles
1. Short first, long second: Do not waste long optimization on bad starts
2. Probe before eval: Use all 30 probes to rank, save 3-4 evals for final
3. Diversity matters: 8 patterns hit different local minima
4. Integral constraint: Always renormalize final h to ensure integral h = 1
5. Patience: If stuck, restart with completely different initialization family

## Common Pitfalls
- Running only ONE optimization (seed program flaw)
- No probe usage (wasting expensive evals)
- Too long per variant (cannot afford 10 x 59000 steps)
- Penalty too high (prevents shape exploration)
- Not ensuring integral constraint
