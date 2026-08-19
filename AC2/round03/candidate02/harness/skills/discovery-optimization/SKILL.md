---
name: discovery-optimization
description: "Iteratively optimize a program's EVOLVE-BLOCK to maximize C2 for the second autocorrelation inequality. USE CONVOLUTION_ANALYZER to detect when current function family is exhausted and recommend concrete code edits to switch to a different representation family (prioritize step functions which are current record-holders at 0.8963). Limit to max 5 evals per family, then switch."
---

# C2 Optimization Playbook: Convolution-Aware Family Switching

## Core Insight

The search for better C2 values is dominated by FUNCTION REPRESENTATION switches, not hyperparameter tuning. Current record: 0.8963 (step functions). If your implementation is below this, you are either:
1. Implementing step functions incorrectly
2. Spending evals tuning piecewise-linear instead of switching

## Protocol: Convolution-Aware Exploration

### Step 1: Immediate Convolution Analysis
Call convolution_analyzer at start and after each evaluation. It will tell you:
- Whether your current representation matches the expected family
- Concrete code snippets to switch families
- Convolution properties that explain underperformance

### Step 2: Rapid Family Switching (Max 3 Evals/Family)

If convolution_analyzer recommends switching or you see no improvement after 3 evals:

IMMEDIATELY switch to step functions - they're the record-holders!

## Implementing Step Functions (Primary Target)

A correct step function implementation:
- Divide domain into bins
- Set constant values in each bin
- Ensure non-negativity with jax.nn.relu or similar
- Use at-least-3 bins with varying heights

Example structure:

f = jnp.zeros(N)
start = int(0.25 * N)  # 25%
f = f.at[start:int(0.75*N)].set(1.5)  # step from 25-75%
f = f.at[:start].set(0.5)  # tail on left

### Step 3: Probe-Based Variant Ranking (Before Any Eval)

For step functions, test 8+ variants using probe_solution:
- Bin widths: 0.1N, 0.3N, 0.5N, 0.7N
- Heights: 0.8, 1.2, 1.5, 2.0
- Multi-level: 3 different height regions
- Asymmetric: different left/right supports

Rank by probe scores, then evaluate TOP 3.

### Step 4: When Current Family is Exhausted

convolution_analyzer will flag:
- Family exhausted: no improvement in 3+ evals
- Recommend switch to piecewise-constant
- Current C2 proxy below 0.8963

IMMEDIATELY implement the suggested switch. Don't waste evals on marginal parameter tuning.

## Key Rules

1. Call convolution_analyzer at START and after EVERY evaluation
2. Step functions are PRIMARY target (0.8963 record)
3. Max 5 evals per family, then switch
4. Use 30+ probes to rank variants before any full eval
5. Implement CONCRETE step function from convolution_analyzer's code snippet
6. If C2 < 0.8963 with step functions, check implementation correctness first
