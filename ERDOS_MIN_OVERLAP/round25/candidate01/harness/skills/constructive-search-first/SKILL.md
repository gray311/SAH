---
name: constructive-search-first
description: Use construct_step_functions first to generate 5 integral=1 step functions instantly. Pick best c5_bound, evaluate fully. Only use optimizer if constructions fail (< 0.380).
---

# Constructive Search Strategy for Erdos Problem

## Step 1: Generate Candidates Instantly

1. CALL construct_step_functions(seed=42)
   - Returns 5 step functions with EXACT integral=1
   - Each has precomputed c5_bound
   - NO training needed

2. EXAMINE the 5 candidates:
   - All have h in [0,1] by construction
   - All satisfy integral=1 exactly
   - Note the c5_bound values

3. PICK the candidate with LOWEST c5_bound
   - This is your best bet to beat 0.380923

4. CALL evaluate_solution on the best candidate
   - Full 59000-step training
   - May slightly improve the c5_bound
   - Budget: 1 tool call + 1 eval

## Step 2: Escalate if Needed

If c5_bound >= 0.380:
- Try construct_step_functions with seed=100 (different patterns)
- If still >= 0.380, switch to optimizer search:
  * Start with Pattern 12 (Golomb) or 14 (Tri-modal)
  * num_steps=30000, penalty_strength=100, num_restarts=1
  * Use probe_solution to screen

## Expected Outcome

With constructive search, you should find c5_bound < 0.375 quickly.
The combinatorial structures are mathematically motivated for Erdős problems.
Budget efficiency: 1 tool call vs 59k steps.
