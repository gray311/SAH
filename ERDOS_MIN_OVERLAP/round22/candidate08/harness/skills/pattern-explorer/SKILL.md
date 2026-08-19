---
name: pattern-explorer
description: Systematic pattern discovery for Erdos C5. Generate candidate pattern edits, probe-filter, evaluate best.
---

# Pattern Explorer for Erdos C5

## Objective
Find pattern edits that produce h with integral=1 and c5_bound < 0.380923.

## Protocol

### Phase 1: Generate Batch of Pattern Edits
Edit the seed's _get_best_initialization method to try:
- Two-peak patterns with separation ∈ {0.5, 1.0, 1.5}
- Three-peak patterns with centers ∈ {[0.3,1.0,1.7], [0.4,0.9,1.5], [0.5,1.0,1.5]}
- Bipartite patterns with cut ∈ {0.35, 0.5, 0.65}
- Broad single peak (sigma ∈ {0.15, 0.2, 0.25})
- Clustered peaks (2-3 within [0.6, 1.4])

### Phase 2: Probe Screening
CALL probe_pattern or probe_solution on all edits.
Keep only those with c5_bound < 0.37 (probe can be approximate).

### Phase 3: Full Evaluation
For each kept candidate:
  1. Generate the edited program
  2. CALL evaluate_solution
  3. Record combined_score

### Phase 4: Iterate or Finish
If any combined_score > 1.0, call finish and submit.
Otherwise, try variations:
  - Adjust peak widths (widen if too narrow, narrow if too broad)
  - Shift peak positions
  - Try different peak counts (2 vs 3 vs 4)
  - Mix pattern types (e.g., one broad + two narrow)

## Key Insight
The seed's optimizer already trains well - we need BETTER initial patterns,
not longer training. Focus on pattern STRUCTURE, not hyperparameters.

## Constraints to Preserve
- Always use sigmoid: h = 1/(1+exp(-latent))
- Always normalize to integral=1
- Always clip latent to positive values before sigmoid
