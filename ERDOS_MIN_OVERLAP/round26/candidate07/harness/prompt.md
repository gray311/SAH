Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

**CRITICAL WORKFLOW - READ THIS FIRST:**

The seed optimizer runs 15 pattern-based initializations (patterns 0-14 in _get_best_initialization), then trains for 59000 steps.

**PROBLEM**: Full evaluation takes 5-6 minutes. You have only 60 evals. If you train all 15 patterns for 59k steps each, you'll never finish.

**SOLUTION - Analytical Screening Strategy**:

1. **STEP 1: Use probe_solution to check C5 bound after initialization ONLY (no training)**
   - Call edit_solution to change num_restarts=1 and num_steps=0 (or very small)
   - Call probe_solution to get approximate c5_bound
   - KEEP only candidates with c5_bound < 0.375

2. **STEP 2: For promising candidates, train for 10000 steps, then probe again**
   - Short training lets you refine good initializations cheaply
   - Still use probe to screen before full eval

3. **STEP 3: ONLY call evaluate_solution when probe indicates c5_bound < 0.372**
   - Full eval is expensive (~5 min) and wastes budget on bad candidates
   - You only get ~60/60 = 100% of your eval budget if you're selective

4. **STEP 4: After finding one improvement, SEARCH AROUND IT**
   - Keep the working initialization
   - Vary num_intervals (400, 800, 1600) to find optimal resolution
   - Vary learning rate (0.001-0.02) to see if it converges faster
   - Try num_steps=30000 for faster confirmation

**PATTERN INSIGHTS FROM SEED**:
- Pattern 12: Golomb ruler [0,0.4,0.8,1.2,1.6] - marks distributed to minimize overlap
- Pattern 14: Tri-modal [0.4, 1.0, 1.6] - 3 narrow peaks
- Pattern 5: Bipartite [0.5] step - simple half-half split
- These analytical patterns should be evaluated FIRST, before any training

**STRATEGY SUMMARY**: 
- Phase 1 (evals 1-15): Analytical screening via short-training + probe (num_steps=1000)
- Phase 2 (evals 16-40): Train promising candidates 30000 steps, probe before eval
- Phase 3 (evals 41-60): Full evaluation of top 3-5 candidates
- NEVER evaluate a candidate with c5_bound > 0.374 (probe threshold)
