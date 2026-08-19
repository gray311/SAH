---
name: discovery-optimization
description: "Discover novel mathematical functions optimizing C\u2082 constant via systematic exploration. Use c2_analyzer() for initial analysis, c2_probe() for rapid ranking, then confirm with evaluate_solution(). Start with c2_analyzer() to understand the landscape."
---

# C₂ Optimization Strategy

## Step 1: Analyze the Mathematical Space
Start by calling c2_analyzer() to see the convexity landscape, current best structure, and sensitivity analysis for different parameters. This tells you WHAT to optimize for.

## Step 2: Systematic Exploration Strategy

### A. Piecewise Constant Functions (Expand the seed)
The seed uses 13 step patterns. Try:
- More levels (4-6 pieces)
- Asymmetric patterns
- Different peak positions
- Variable heights based on mathematical intuition

### B. Spline-Based Functions
Create smooth transitions between step levels. This might increase ||f★f||₂² while maintaining good ||f★f||_∞.

### C. Multi-Scale Constructions
Combine a coarse envelope with fine structure. Think: Gaussian envelope × piecewise function.

### D. Fourier-Optimized
If the convolution is FFT-based, work in frequency domain: optimize Fourier coefficients that yield positive time-domain functions.

## Step 3: Use the Probe Loop
After EACH edit:
1. Call c2_probe() - gets approximate C₂ without consuming evaluation budget
2. If c2_probe < current best probe, REVERT and try a different direction
3. If c2_probe looks promising, call evaluate_solution() to confirm

## Step 4: When to Evaluate Fully
- You have 2+ evaluation budget left
- c2_probe suggests >1.02 combined_score
- You're confident in the mathematical structure

## Step 5: Recovery from Failure
- If evaluate_solution errors, read the error, fix SPECIFICALLY that issue
- If score drops, analyze why: was it a different function class? Try something orthogonal

## Tools Reference
- edit_solution(): Make your next hypothesis (prefer SEARCH/REPLACE)
- c2_analyzer(): Get sensitivity analysis to guide your next edit. Call ONCE at start.
- c2_probe(): Get fast approximate C₂ score (doesn't consume eval budget). Call AFTER each edit.
- evaluate_solution(): Get exact C₂ score (consumes 1 eval)

Remember: 30 evaluations total. Each must push the frontier.
