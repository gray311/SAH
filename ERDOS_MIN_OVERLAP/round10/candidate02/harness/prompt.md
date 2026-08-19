You are solving the Erdős minimum overlap problem: find a step function h: [0,2] → [0,1] with integral(h)=1 that minimizes C5 = max_k ∫ h(x)(1-h(x+k)) dx.

Current best bound: C5 ≤ 0.38092303510845016 (combined_score = 0.380923 / C5, need > 1.0)

**CRITICAL STRATEGY: CONSTRUCTIVE SEARCH**
The seed optimizer uses gradient descent from 12 initialization patterns. This often gets stuck in local minima.

YOUR APPROACH:
1. **DIRECT CONSTRUCTION**: Use construct_valid_step_function to generate valid step function candidates
2. **EXPLORE DIVERSE PATTERNS**: Try bimodal, triangular, periodic, multi-peak constructions
3. **RAPID EVALUATION**: Use probe_solution to screen constructions, then evaluate_solution on promising ones
4. **HYPERPARAMETER TUNING IS SECONDARY**: Only use if constructions alone fail

Tool usage order:
- call construct_valid_step_function to get diverse candidate structures
- call edit_solution to implement a specific construction (can bypass optimizer for direct C5 computation)
- call probe_solution to quickly validate integral constraint and get approximate score
- call evaluate_solution on top 1-2 candidates

Keep in mind: the EVOLVE-BLOCK contains an optimizer. Your goal is to replace it with direct construction + evaluation, as direct computation often beats gradient optimization for this problem.

Focus on constructions that exploit the FFT-based correlation structure:
- Concentrate h(x) in specific regions to minimize overlap with 1-h(x+k)
- Try asymmetric placements, multi-peak distributions, Golomb ruler-inspired patterns
