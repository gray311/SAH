---
name: analytical-search-strategy
description: Use FFT-based analytical c5 scoring to screen candidates. Only run full optimization on best candidates.
---

# Analytical Search Strategy for Erdos Optimization

## Core Insight
The seed optimizer wastes time training for 59000 steps. We need FAST analytical scoring.

## FFT-Based Analytical Scoring
The c5_bound can be computed analytically using FFT:
1. Take h(x) values on [0, 2]
2. Compute j(x) = 1 - h(x)
3. Pad both with zeros to length 2N
4. Compute FFT of h and j
5. Compute correlation = IFFT(FFT(h) * conj(FFT(j)))
6. c5_bound = max(correlation) * dx

This is INSTANT - no training needed!

## Workflow

1. CALL gen_candidates to get 10 candidates

2. ANALYZE each candidate:
   - Check integral (should be ~1.0)
   - Note c5_bound (precomputed analytically)
   - Check pattern_type

3. FILTER candidates:
   - SKIP if integral != 1.0 (constraint violation)
   - SKIP if c5_bound >= 0.35 (too bad)
   - KEEP if c5_bound < 0.35

4. CALL evaluate_solution on kept candidates (typically 2-5)

5. If any candidate achieves combined_score > 1.0, finish!

6. If no improvement, CALL gen_candidates with temperature=0.95 for more exploration

## Expected Results
With 10 analytical candidates, we expect 3-5 to pass c5 < 0.35.
This gives us multiple chances to find improvements with minimal eval budget.

## Why This Beats Training
- Analytical scoring: instant (milliseconds)
- Training: 59000 steps per candidate (too slow)
- We can screen 10+ candidates analytically, then only train 2-3 best ones
- Budget efficient: 1 tool call + 2-5 evals per iteration
new_middlewares:
- name: enforce_analytical_first
  hook: before_model
  description: Force solver to use analytical scoring before any training
  implementation_py: |
    def before_model(hook_input):
        state = hook_input.get("state", {})
        evals_left = state.get("evals_left", 0)
        probes_used = state.get("probes_used", 0)

        if evals_left >= 5 and probes_used < 2:
            return (
                "CRITICAL: You have 5+ evals but haven't used analytical screening!\\n"
                "CALL gen_candidates first.\\n"
                "Score 10 candidates analytically (instant).\\n"
                "Only evaluate 2-3 best candidates with c5_bound < 0.35.\\n"
                "DON'T train 59000 steps before analytical screening!"
            )
        elif evals_left >= 2:
            return (
                f"{evals_left} evals remaining.\\n"
                "Look for c5_bound < 0.33 candidates for full eval.\\n"
                "Consider generating new patterns if no improvement yet.\\n"
            )
        return None
