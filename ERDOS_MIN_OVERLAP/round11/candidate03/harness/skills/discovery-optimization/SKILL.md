---
name: discovery-optimization
description: "Search for asymmetric bimodal step functions using diverse initialization generation and probe-based screening to find candidates with low overlap."
---

# Erdos Minimum Overlap - Diverse Initialization Strategy

## Why This Works
The seed's 12 initialization patterns may not include the optimal asymmetric bimodal structure.
We need to GENERATE new candidates outside the seed's search space.

## Two-Phase Search

### Phase 1: Generate and Probe (Use 20-25 evals)
1. CALL generate_variants() to get diverse latent vectors
2. For each variant:
   - Convert to h = sigmoid(latent)
   - CALL probe_solution to get quick score + check constraint penalty
   - Keep variants with penalty < 100 AND lowest probe score
3. Rank top 3-5 variants by probe score

### Phase 2: Full Evaluation (Use 5-10 evals)
4. CALL evaluate_solution on top 2-3 variants from Phase 1
5. If any achieve combined_score > 1.0, FINISH

### Phase 3: Refinement (if needed)
6. If best score is ~0.999-1.0 but not > 1.0:
   - EDIT EVOLVE-BLOCK to use the initialization pattern of the best variant
   - Tune ONE hyperparameter (learning rate, penalty, or num_steps)
   - Call evaluate_solution on refined version
   - Repeat 1-2 times if budget remains

## Key Patterns to Look For
- Asymmetric bimodal: two peaks at different heights/locations
- Multi-peak with varying widths
- Functions that are NOT symmetric about x=1

## Tool Usage
- generate_variants(): Get diverse candidates (call once, get 4-8) - NEW TOOL
- probe_solution(): Quick score (~10s), uses separate budget (call for each candidate)
- evaluate_solution(): Full score, consumes real eval budget (call on top candidates)
- edit_solution(): Only after finding promising candidate to refine further
- finish(): Submit when combined_score > 1.0
