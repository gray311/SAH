---
name: discovery-optimization
description: "Mathematical function optimizer for autocorrelation inequality discovery. Analyze step function patterns, use FFT convolution properties, and systematically search for non-negative functions maximizing C\u2082. Prefer targeted edits, use probes for ranking, and only evaluate promising candidates fully."
---

# Mathematical Function Optimization for C₂ Maximization
## Step 1: Initial Analysis Call analyze_step_patterns immediately. Examine: - Number of steps and their widths - Height values and their distribution - Symmetry properties - Convolution properties (via the tool's analysis)
## Step 2: Pattern Analysis The seed provides 13 pre-defined step patterns. Your goal is to: - Understand which features contribute to high C₂ - Identify if multi-level patterns beat single-step patterns - Consider asymmetric vs symmetric designs
Key insight: C₂ rewards functions where ||f★f||₂² is large but ||f★f||_∞ is small. This favors: - Moderate peak heights (not too concentrated) - Broad support with smooth transitions - Balanced energy distribution in convolution
## Step 3: Iterative Improvement Strategy
### Phase A: Pattern Exploration (if score < 1.0) The seed achieves ~1.03, beating the theoretical 0.896. This suggests the evaluator has different scoring or the seed has a bug. Still, we must beat 1.03.
Try modifications: - Adjust step widths: ±5-10% changes - Adjust step heights: ±0.05-0.1 changes - Add/remove intermediate steps - Shift peaks left/right - Try asymmetric patterns (current seed is symmetric)
### Phase B: Multi-scale Optimization 1. Start with coarse grid (num_intervals = 80-120) 2. Optimize to find good structure 3. Refine on fine grid (num_intervals = 400+) 4. This avoids local minima in high-dimensional space
### Phase C: Probing Strategy 1. Call analyze_step_patterns 2. Generate 3-5 variant patterns 3. Probe each (cheap, separate budget) 4. Pick top 2 variants 5. Evaluate fully (costs real budget) 6. Iterate
## Step 4: Avoid Common Pitfalls - DON'T change imports or the entry function - DON'T use stochastic sampling (fixed seed = reproducibility) - DON'T increase num_intervals too much (O(n log n) but still costly) - DO use probe_solution before evaluate_solution - DO call analyze_step_patterns first to understand your function - DO keep changes targeted (SEARCH/REPLACE small blocks)
## Step 5: Tool Usage Pattern
Turn 1: analyze_step_patterns -> understand structure Turn 2-4: edit_solution (3 variants) + probe_solution x3 Turn 5: edit_solution (best variant) + evaluate_solution Turn 6-10: Iterate with probes, evaluate top 1-2 per iteration
When score > 1.03431: CONGRATULATIONS, you're ahead of seed! Try: tighter peaks, more levels, asymmetric designs.
When stuck: Call analyze_step_patterns again, try a completely different pattern class.
