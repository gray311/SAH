---
name: discovery-optimization
description: "Direct structural search for step functions with probe-based screening and diverse candidate generation."
---

# Erdos Minimum Overlap - Direct Structural Search

## Problem Understanding
Find step function h: [0,2] -> [0,1] with integral(h)=1 that minimizes:
max_k ∫ h(x)(1-h(x+k)) dx

Current best: C5 <= 0.380923 (need combined_score > 1.0)

## Why Direct Construction Works
The seed optimizer transforms latent vectors through sigmoid to get h, then optimizes.
But the optimal h might be a STEP FUNCTION with sharp transitions, not a smooth sigmoid.
We should CONSTRUCT diverse step-function shapes directly and test them.

## Strategy

### Phase 1: Direct Candidate Generation (Use probe_solution extensively)
1. Call construct_structured_init to generate 5-10 diverse step functions
2. For each candidate:
   - Check integral constraint via probe (quick ~10s)
   - If constraint satisfied, get approximate c5 score
   - If constraint violated, discard
3. Track top 3 candidates by approximate score

### Phase 2: Full Evaluation (Budget: 30 evals total)
4. Call evaluate_solution on top 3 candidates
5. If ANY has combined_score > 1.0, SUCCESS

### Phase 3: If Phase 2 Fails
If no direct candidates beat seed:
1. Edit _get_best_initialization() to add MORE structural patterns:
   - More bimodal patterns with different peak positions
   - Triangular/trapezoidal step patterns
   - Multi-peak patterns (3-4 peaks)
   - Asymmetric patterns
2. Test these with the optimizer but with DIRECTED searches

### Phase 4: Structural Experiments
If still stuck, try:
- num_intervals = 400 (coarser, faster)
- num_intervals = 1600 (finer, more precise)
- Different penalty strengths to enforce integral=1 more strictly

## Success Criteria
- combined_score > 1.0 (c5_bound < 0.380923)
- If not achievable, document the best structural insight gained

## Key Tool: construct_structured_init
Generates step functions directly (not via latent optimization):
- Bimodal: two sharp peaks
- Triangular: three-level steps
- Multi-peak: 3-5 narrow peaks
- Golomb-like: optimal spacing patterns
All candidates satisfy sigmoid(h) -> [0,1] and we check integral(h)=1.
