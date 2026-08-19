---
name: discovery-optimization
description: "Generate structural variants of the pattern initialization code. Modify wave parameters, try new Golomb rulers, experiment with different initialization strategies. Use probes to screen before full evaluation."
---

# Structural Variant Generation Strategy

## Problem
The seed's 15 patterns may not explore the right region. We need systematic modifications.

## Solution: structural_variants Tool

This tool generates 5 program edits that modify the initialization code:
- Wave pattern modifications (different frequencies/amplitudes)
- New Golomb ruler constructions (optimal spacing)
- Fourier-based spectral methods
- Threshold pattern variations
- Hybrid constructions

## Workflow

1. CALL structural_variants() - get 5 program edits

2. For each variant:
   - CALL probe_solution to check c5_bound (cheap, ~10s)
   - Record the score

3. Rank by probe score (lowest c5_bound = best)

4. CALL evaluate_solution on top 2-3 variants (full score)

5. If best new score < 0.380923, CALL structural_variants again with different strategies

6. Total probes: 5-7. Total evals: 2-6.

## Why This Works

- Structural changes, not just hyperparameters
- Probe-based screening: find winners before expensive evals
- Multiple variants per call: diverse exploration
- Focus on code-level innovations, not grid search
