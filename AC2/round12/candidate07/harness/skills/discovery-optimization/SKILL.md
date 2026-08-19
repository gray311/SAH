---
name: discovery-optimization
description: "C\u2082 maximization using pattern recombination and diverse structural mutations. Focus on combining parts of different seed step patterns rather than small perturbations."
---

# C₂ Maximizer: Pattern Recombination Protocol

## Core Principle

The seed has 13 working step patterns. Small perturbations won't help. RECOMBINE different patterns to create novel architectures.

## Step 1: Get Recombination Proposals

Call pattern_recombiner to get 2-3 diverse mutation options that:
- Recombine parts of different seed patterns (e.g., peak heights from pattern 0, widths from pattern 5)
- Create completely new multi-level structures (3-5 levels)
- Try asymmetric or smoothed variants

## Step 2: Pick and Implement ONE Option

Choose ONE proposal and implement it with edit_solution:
- Make COMPLETE edits - ensure the code will run without errors
- Focus on BIG changes (heights ±0.15-0.30, widths ±10-25%, entirely new structures)

## Step 3: Evaluate Immediately

Call evaluate_solution ONCE per variant. Don't iterate locally - each eval tests a complete new direction.

## Step 4: Diverse Exploration

If no improvement after 1-2 evals:
- Try a COMPLETELY different pattern class
- Recombine different seed patterns
- Explore new architectures (smooth transitions, multi-peaked functions)

## Mutation Types to Try

1. **Pattern Recombination**: Merge peaks/levels from 2-3 different seed patterns
2. **Asymmetric Multi-Peak**: Create 3-4 peaks with varying heights/widths
3. **Widened Core**: Expand central interval by 15-25%
4. **Height Diversification**: Make all peaks distinctly different (1.2, 1.7, 2.1, 1.5, 1.3)
5. **Smooth Step**: Add gradual transitions between levels

## Key Warning

Each evaluation is precious. Never try 3-4 variants of the same idea before evaluating. ONE eval, ONE complete change, then move on.
