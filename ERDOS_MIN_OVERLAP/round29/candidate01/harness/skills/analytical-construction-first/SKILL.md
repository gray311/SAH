---
name: analytical-construction-first
description: Always construct step functions analytically (bipartite, multi-peak, sparse) before using the optimizer. Use construct_bipartite, construct_multipeak, or construct_sparse to generate candidates. Screen with probe_solution, then evaluate top candidates with c5_bound < 0.375. Only after exhausting analytical constructions should you tune hyperparameters.
---

# Analytical Construction First for Erdos C5

## Core Principle
The optimizer cannot discover good h functions from random noise. Instead, CONSTRUCT them analytically with guaranteed integral constraint.

## Workflow

### Phase 1: Analytical Construction
1. CALL construct_bipartite(a=0.5) OR construct_multipeak(n_peaks=3, peak_positions=[0.4, 1.0, 1.6]) OR construct_sparse(num_spikes=5)
2. Each returns h with integral=1 and precomputed c5_bound via FFT
3. Check c5_bound < 0.375

### Phase 2: Screening
4. CALL probe_solution on each candidate
5. Keep those with c5_bound < 0.375 (or even < 0.37)

### Phase 3: Optimization
6. CALL evaluate_solution on the BEST candidate (lowest c5_bound)
7. If combined_score > 1.0, finish
8. If not, try different construction parameters (different a, positions, etc.)

### Phase 4: Alternative Constructions
If Phase 1 fails:
- Try bipartite with a=0.45, 0.55
- Try multipeak with n=2, n=4, n=5
- Try sparse with different spike positions
- Try symmetric constructions

## Key Rules
- ALWAYS construct analytically first
- GUARANTEE integral = 1 in construction
- Use FFT for fast c5_bound (don't waste evals)
- Only optimize candidates with c5_bound < 0.375
- Try multiple construction types before tuning hyperparameters
- Don't use random initialization from the seed program

## Tools to Use
- construct_bipartite: simple two-level function
- construct_multipeak: multiple rectangular peaks
- construct_sparse: narrow spikes with mostly zeros
- probe_solution: fast screening
- evaluate_solution: full optimization on promising candidates
