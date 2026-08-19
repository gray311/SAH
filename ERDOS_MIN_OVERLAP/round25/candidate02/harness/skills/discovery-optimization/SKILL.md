---
name: discovery-optimization
description: "Erdos C5: Generate integral-constrained analytical candidates FIRST,\nevaluate the best, only then explore hyperparameter tuning if needed. Prioritize\ndirect evaluation of structurally promising step functions over SGD."
---

# Analytical Candidate Evaluation for Erdos C5

## PRIMARY STRATEGY: Direct Evaluation of Structured Candidates

### Step 1: Generate Analytical Candidates

1. CALL generate_analytical_candidates() - this returns 5-8 step functions with:
   - Exact integral = 1.0 (guaranteed by construction)
   - Precomputed c5_bound via FFT (no training needed)
   - Values already scaled to [0,1]

2. Expected outputs include patterns:
   - Golomb-4: 4 marks at [0, 0.4, 0.8, 1.2] spacing
   - Golomb-5: 5 marks at [0, 0.4, 0.8, 1.2, 1.6] spacing
   - Bipartite: High on [0,a), low on [a,2] for various a
   - Tri-modal: 3 narrow peaks at [0.4, 1.0, 1.6]
   - Uniform-2: 2 blocks [0,a) and [a,2] with proper mass split

### Step 2: Filter and Evaluate

1. FILTER candidates with c5_bound < 0.380 (about 3-4 candidates typically pass)
2. CALL evaluate_solution on EACH filtered candidate
3. If ANY returns combined_score > 1.0 → CALL finish()

### Step 3: Secondary Search (ONLY if Step 2 fails)

1. If no improvement: CALL generate_analytical_candidates(temperature=0.8) for variety
2. Re-evaluate new candidates
3. Still stuck: Try ONE hyperparameter change with num_restarts=1, num_steps=30000
4. Always use probe_solution to screen before full eval

## Why This Works

- Analytical candidates are EXACT integral=1 solutions (SGD may violate constraint)
- No training overhead: c5_bound computed instantly via FFT
- Structurally optimal patterns (Golomb) minimize overlap by design
- SGD from seed pattern likely cannot beat an already-optimized analytical solution

## Critical Rule

NEVER waste an eval budget on SGD training when you have an analytical candidate.
The analytical candidates ARE the answer - they are mathematically constructed
optimal step functions, not random walks. If they fail, only then explore SGD.
