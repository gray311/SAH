---
name: discovery-optimization
description: "Constructive search for Erdos C5. Use construct_step_functions to generate exact integral=1 step functions\nimmediately. Then use optimizer only if constructions fail to beat 0.380. Use probe_solution for screening."
---

# Constructive Search for Erdos Problem

## Phase 1: Generate Exact Step Functions (NO TRAINING NEEDED)

1. CALL construct_step_functions() ONCE
   - Returns 5 step functions with EXACT integral=1
   - Each has precomputed c5_bound via FFT
   - All h values in [0,1] by construction

2. FILTER the 5 candidates:
   - Pick the one with LOWEST c5_bound
   - If c5_bound < 0.380, this is promising!

3. CALL evaluate_solution on the best candidate(s)
   - Full training may slightly improve but the construction is already strong
   - Budget efficient: 5 constructions = 1 tool call, then 1-5 evals

## Phase 2: Optimizer-Only Search (IF Phase 1 Fails)

If best construction has c5_bound >= 0.380:
- Start with: num_intervals=800, num_steps=30000, penalty_strength=100, num_restarts=1
- Seed patterns: 12 (Golomb), 14 (Tri-modal) - lowest initial c5
- Learning rate: 0.01 or 0.02 (aggressive)
- Use probe_solution to screen before full eval
- Only evaluate if probe c5_bound < 0.375

## Why This Works

- construct_step_functions gives you 5 VALID candidates INSTANTLY (no 59k steps)
- Step functions are mathematically motivated for Erdős problems
- Budget efficient: 1 tool call vs 59k-step training
- If constructions fail, optimizer is your backup (not your primary)
