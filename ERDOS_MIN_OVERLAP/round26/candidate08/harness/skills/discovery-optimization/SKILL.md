---
name: discovery-optimization
description: "Pattern-based initialization search for Erdos C5 minimization. Use probe_pattern_variants to generate diverse pattern initializations (Golomb, bipartite, tri-modal with varied parameters). Screen with probe_solution (c5_bound < 0.375). Evaluate best candidates. Then edit pattern parameters (mark locations, split points) to fine-tune. Finally tune hyperparameters only if pattern search stalls."
---

# Pattern-Based Search for Erdos C5 Problem
## Core Insight The seed optimizer has 15 pattern types. We need to EXPLORE these patterns with different parameters, not just tune hyperparameters.
## Step 1: Generate Pattern Variants 1. CALL probe_pattern_variants() - generates 10 diverse pattern initializations 2. EXAMINE candidates with c5_bound < 0.375 3. CALL evaluate_solution on top 3-5 best candidates
## Step 2: Parameterize Existing Patterns The seed patterns include:
**Golomb ruler (Pattern 12)**: marks = [0.0, 0.4, 0.8, 1.2, 1.6] - Try different spacings: [0, 0.3, 0.6, 0.9, 1.2], [0, 0.5, 1.0, 1.5], [0, 0.4, 0.9, 1.4] - Try 4 marks instead of 5: [0, 0.5, 1.0, 1.5] - Try different amplitudes: marks get value 5.0 or 8.0
**Bipartite (Pattern 5, 13)**: x < 0.5: high, x >= 0.5: low - Try different split: x < 0.3, x < 0.4, x < 0.6, x < 0.7 - Try two-split: x < 0.33: high, 0.33 <= x < 1.33: low, x >= 1.33: high
**Tri-modal (Pattern 14)**: peaks at [0.4, 1.0, 1.6] - Try different peaks: [0.3, 1.0, 1.7], [0.2, 0.8, 1.4] - Try 2-peak: [0.5, 1.5] - Try 4-peak: [0.3, 0.7, 1.3, 1.7]
## Step 3: Single-Restart Evaluation When testing one pattern variant: - Set num_restarts=1, num_steps=50000 - This quickly evaluates that specific initialization - Use probe_solution to screen before full eval
## Step 4: Only Then Tune Hyperparameters If pattern search yields no improvement: - Vary num_intervals: 400, 800, 1600 (coarse to fine) - Vary penalty_strength: 40, 60, 80 (weaker to stronger constraint)
## Step 5: Iterate - If one pattern works well, try variants of it - If multiple patterns work, combine ideas - Stop when combined_score > 1.0
## Tool Usage Summary 1. probe_pattern_variants: Generate 10 pattern candidates 2. probe_solution: Check c5_bound (cheap, < 10s) 3. edit_solution: Modify pattern parameters or hyperparameters 4. evaluate_solution: Confirm top candidates (full 59000 steps)
