---
name: hadamard-29-escape-strategy
description: Escape local optima in Hadamard-29 optimization using diverse constructions, probe-based ranking, and adaptive hill climbing parameters. Critical for beating the seed score.
---

# Hadamard-29 Escape Strategy

## Problem
n=29 has no true Hadamard matrix (requires n ≡ 0 mod 4). Current approaches using
Paley construction + hill climbing get stuck in local optima with |det| ~ 300-400.

## Escape Strategy (CRITICAL!)

### Step 1: Diagnostic baseline
- Call analyze_hadamard_quality ONCE at start
- Record baseline |det|, orthogonality score
- If orthogonality_score < 0.5, expect local optimum

### Step 2: Diverse construction exploration
In EACH evaluation, try DIFFERENT construction methods:

A. Paley + small perturbations
   - Start with Paley matrix
   - Apply 5% random flips
   - Run hill_climbing_improved (3000 iters, temp=1.5, cool=0.9995)
   - 10 restarts

B. Random seeds with structure
   - Generate random matrix with bias toward structured patterns
   - 5-10 different seeds
   - Same hill_climbing parameters

C. Block-based optimization
   - Divide into 3x3 or 4x4 blocks
   - Optimize each block independently
   - Combine and optimize globally

### Step 3: Probe-based variant ranking
- Create 3-5 variants with DIFFERENT construction methods
- Call probe_solution on EACH (cheap, ~10s each)
- Rank by probe scores
- Call evaluate_solution ONLY on top 1-2

### Step 4: Adaptive hill climbing
- Use hill_climbing_improved, NOT raw hill climbing
- Parameters: max_iters=3000, initial_temp=1.5, cool_rate=0.9995
- Auto-restart every 500 iters if no improvement
- Total time per run: < 120s

### Step 5: When stuck
- After 2 failed evaluations with no improvement:
  - Call regenerate_from_scratch
  - Choose completely different construction method
  - Restart entire process

### Key metrics for success
- |det(H)| > 400 is a good improvement
- Use all 20 eval budgets efficiently
- Each evaluation should try 2-3 different construction methods
- Probe before every evaluate_solution
