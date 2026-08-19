You are optimizing the C₂ constant: C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞) for non-negative f.

CRITICAL: The seed program implements hybrid step functions that already achieve combined_score 1.03896.
Your goal: REFINE THE STEP-FUNCTION ARCHITECTURE to push C₂ higher.

Strategy (proven effective):
1. Generate 3-5 small perturbations of the current step function (height tweaks, width shifts, asymmetry)
2. For each, call probe_solution FIRST (30 probe budget available - use cheaply!) to filter
3. Call evaluate_solution ONCE per variant that beats the probe score
4. If a variant improves, refine it further; if not, try a different perturbation
5. NEVER explore completely new function families (Gaussian, splines, etc.) - they won't beat optimized steps

Constraints: f(x)≥0, use SEARCH/REPLACE edits for small mutations (±0.02-0.08 on heights, ±3-8% on widths).
