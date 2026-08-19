---
name: discovery-optimization
description: "Generate structured step functions (bipartite, multi-peak, Golomb) with integral=1.\nUse probe to screen, evaluate best candidates."
---

# Erdos C5 - Structured Step Function Search

## Phase 1: Generate Structured Candidates

1. CALL step_function_generator with pattern="bipartite"
   - Creates h(x) = 1 for x < threshold, 0 otherwise
   - Normalize so integral = 1 (threshold = 0.5)
   - Try different threshold positions: 0.25, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7

2. CALL step_function_generator with pattern="multi_peak"
   - Creates 2-4 narrow peaks (width 0.05-0.1)
   - Space peaks to minimize overlap
   - Ensure equal mass per peak so total integral = 1

3. CALL step_function_generator with pattern="golomb"
   - Creates sparse marks at positions like [0, 0.4, 0.8, 1.2, 1.6]
   - Optimized for minimum pairwise overlap

## Phase 2: Probe and Evaluate

4. CALL probe_solution on each candidate
   - Keep those with c5_bound < 0.378

5. CALL evaluate_solution on best 2-3 candidates
   - If combined_score > 1.0, finish

## Phase 3: Variations

If no improvement:
- Try different num_intervals (100, 200, 500, 1000, 2000)
- Try different peak widths and numbers
- Try asymmetric patterns (more mass at one end)

## Key Rules
- Generate STRUCTURED step functions, not random latents
- Always normalize so integral(h) = 1
- Use probe to screen before full evaluation
- Try multiple patterns before giving up
