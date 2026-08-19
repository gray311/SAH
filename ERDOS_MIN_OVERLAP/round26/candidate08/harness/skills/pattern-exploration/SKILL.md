---
name: pattern-exploration
description: Use probe_pattern_variants to generate diverse pattern initializations, then edit pattern parameters to fine-tune. Workflow - 1. Call probe_pattern_variants to get 10 candidates 2. Filter for c5_bound < 0.375 3. Edit pattern parameters (mark positions, split points, peak locations) in EVOLVE-BLOCK 4. Use probe_solution to screen edited patterns 5. Evaluate best with evaluate_solution 6. If one pat
---

# Pattern Exploration for Erdos C5
## Strategy The seed optimizer has 15 patterns. We need to EXPLORE them with different parameters.
## Step 1: Generate Pattern Variants 1. CALL probe_pattern_variants() - returns 10 candidates with c5_bound 2. EXAMINE candidates with c5_bound < 0.375 3. Keep top 3-5 for evaluation
## Step 2: Parameterize Patterns
### Golomb Ruler (Pattern 12) The seed uses marks = [0.0, 0.4, 0.8, 1.2, 1.6] - Edit to: marks = [0.0, 0.3, 0.6, 0.9, 1.2] (coarser spacing) - Edit to: marks = [0.0, 0.5, 1.0, 1.5] (4 marks) - Edit to: marks = [0.0, 0.45, 1.1, 1.7] (unequal spacing)
### Bipartite (Pattern 5, 13) The seed uses x < 0.5: high, x >= 0.5: low - Edit to: x < 0.3: high, x >= 0.3: low - Edit to: x < 0.4: high, x >= 0.4: low - Edit to: x < 0.6: high, x >= 0.6: low
### Tri-modal (Pattern 14) The seed uses peaks at [0.4, 1.0, 1.6] - Edit to: peaks = [0.3, 1.0, 1.7] - Edit to: peaks = [0.2, 0.8, 1.4] - Edit to: 2 peaks at [0.5, 1.5]
## Step 3: Single-Restart Evaluation - Set num_restarts=1, num_steps=50000 - Quickly evaluate each pattern variant - Use probe_solution to screen before full eval
## Step 4: Iterate on Promising Patterns If Golomb works best: - Try more Golomb variants - Fine-tune mark spacing - Adjust amplitude
## Expected Outcome By exploring pattern parameters, you should find c5_bound < 0.38092303510845016.
