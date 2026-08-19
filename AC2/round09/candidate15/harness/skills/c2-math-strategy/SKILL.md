---
name: c2-math-strategy
description: Mathematical strategy for maximizing C₂ in autocorrelation inequality. Focus on function classes that balance L1, L2, and L∞ norms optimally.
---

# C₂ Maximization Strategy
The goal: maximize C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞)

KEY PRINCIPLES:
1. Higher peak heights improve L2 more than L∞ → better ratio
2. More levels (3-6) allow shaping the convolution
3. Asymmetric distributions can exceed symmetric limits

SEARCH STRATEGY:
- Analyze current patterns with analyze_step_function FIRST
- Follow its specific suggestions
- Use probe_solution AFTER each edit (30 probes available!)
- Only evaluate when probe shows improvement
- If score < 1.0, try: higher peaks, more levels, or asymmetric

TOOL USAGE ORDER:
1. analyze_step_function → understand current state
2. edit_solution → make ONE targeted change per its advice
3. probe_solution → check direction cheaply
4. evaluate_solution → confirm only if probe good
5. math_insight → when directionless

AVOID:
- Blind random mutations
- Wasting evals on bad ideas
- Ignoring probe results
