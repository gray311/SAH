---
name: discovery-optimization
description: "Multi-pattern search for Erdos minimum overlap: generate diverse structured seeds, short-optimize, probe-rank, refine top candidates, then full-evaluate."
---

# Erdos Minimum Overlap - Multi-Pattern Search Strategy

## Why Current Approaches Fail
Single-shot optimization from one random/structured seed cannot escape local minima. The landscape has MANY good structured points but few global optima.

## REQUIRED WORKFLOW (MUST FOLLOW IN ORDER)

### Step 1: Generate Diverse Seeds
Call generate_diverse_seeds() IMMEDIATELY. This returns 5-8 patterns:
- bimodal_tight: Two narrow peaks at 0.25, 0.75
- bimodal_wide: Two broader peaks with more overlap
- triangular_3step: 3-level linear ramps
- periodic_2: Alternating high/low on [0,0.5], [0.5,1]
- periodic_4: Four-cycle pattern
- golomb_5: Peaks at Golomb ruler positions
- shifted_bimodal: Same as bimodal but shifted left/right
- mixed: Random combination of 2-3 patterns

### Step 2: Short Optimization with Varying Hyperparams
For EACH seed pattern:
- Run optimization for 3000-5000 steps
- Use DIFFERENT hyperparams each time:
  * Run A: lr=0.05, penalty=1000
  * Run B: lr=0.01, penalty=5000
  * Run C: lr=0.02, penalty=3000
- Record the c5_bound after each run

### Step 3: Probe-Rank All Candidates
Call probe_solution on each optimized candidate.
Sort by c5_bound (lowest = best). Keep TOP 3.

### Step 4: Refine Top 3
For each of the TOP 3:
- Extend optimization to 10000-15000 steps
- Try ADAPTIVE MUTATIONS:
  * AddPeak: Insert a small new peak at a random position
  * RemovePeak: Remove the smallest peak
  * ShiftPeak: Shift all peaks by +/-0.1
  * SplitPeak: Split a wide peak into two narrower ones
  * Compress: Narrow all peaks by 20%
- After each mutation, run 1000-2000 steps
- Probe each mutated variant

### Step 5: Select Best and Full Evaluate
Call probe_solution on all refined candidates.
Select absolute best by c5_bound.
Call evaluate_solution ONCE on this best candidate.

### Step 6: Check and Restart
If combined_score > 1.0, you succeeded - call finish().
If not, the current seed set may be suboptimal. Call generate_diverse_seeds() again with DIFFERENT base patterns and restart Steps 2-5.

## Important Implementation Notes
- Ensure integral(h)=1 by normalizing after sigmoid
- Use jax.lax.stop_gradient during initial seed creation
- The EVOLVE-BLOCK must contain a WHILE/LOOP that iterates through these steps
- Save intermediate results to ctx.scratch_write() for debugging
- Max evaluations = 30, use probes extensively before final evals
