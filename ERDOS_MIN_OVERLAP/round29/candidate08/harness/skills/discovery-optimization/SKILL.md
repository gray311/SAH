---
name: discovery-optimization
description: "Generate mathematically-informed C5 initializations via generate_c5_candidates, evaluate best candidate, then refine hyperparameters if needed. Focus on known constructions (Golomb, bipartite, triangular) with exact integral constraint."
---

# Erdos C5 Optimization Strategy
## Phase 1: Mathematical Initialization (MOST IMPORTANT)
1. CALL generate_c5_candidates() - This generates 10 diverse, integral-constrained initial step functions - Uses known C5 constructions: Golomb ruler (4-7 marks), Bipartite (threshold), Triangular (single peak), Multi-peak (2-4 peaks), Gaussian, Uniform - All satisfy integral(h)=1 and h in [0,1] - Each has num_intervals=200 for faster evaluation
2. EXAMINE the candidates: - Call evaluate_solution on ALL candidates (they are high-quality initializations) - Track the best combined_score
3. If best combined_score > 1.0, FINISH with the summary
## Phase 2: Hyperparameter Refinement (only if Phase 1 fails)
If all candidates have combined_score <= 1.0:
1. Test different hyperparameters: - num_intervals: 400, 800, 1600 (coarse to fine) - base_learning_rate: 0.001, 0.005, 0.01 - penalty_strength: 40, 80, 120 - num_steps: 30000, 60000
2. For each combination: - Set num_restarts=1 for focused search - Test ONE hyperparameter at a time - Track best result
3. If still no improvement, try num_intervals=3200 for very fine search
## Key Rules
- ALWAYS use generate_c5_candidates FIRST (these are high-quality initializations) - NEVER call evaluate_solution on random latents - If stuck, refine hyperparameters systematically - Track best c5_bound across ALL candidates
