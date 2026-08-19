---
name: probe-first-search
description: Use probe_solution to screen many initialization variants before full evaluation. Focus on asymmetric bimodal and multi-peak patterns that minimize overlap.
---

# Probe-First Search for Erdos Optimization

## Strategy
1. Generate diverse candidates using generate_variants()
2. For EACH candidate:
   - Convert latent to h = sigmoid(latent)
   - Check integral(h) ≈ 1 (constraint penalty)
   - CALL probe_solution for quick score
3. Rank by probe score (lowest c5_bound wins)
4. CALL evaluate_solution on top 2-3 candidates
5. If best score > 1.0, FINISH immediately

## Why Probe-First?
- Full evaluation takes minutes; probe takes ~10s
- With 30 eval budget, you can test 30+ candidates with probes
- This lets you explore INITIALIZATION space, not just hyperparameters

## Key Insight
The optimal h likely has ASYMMETRIC bimodal structure.
Seed's 12 patterns may miss this. generate_variants provides NEW patterns.

## Success Criteria
- Find variant with probe_score corresponding to c5_bound < 0.380923
- Verify with full evaluate_solution (combined_score > 1.0)
- Submit with finish()
