---
name: discovery-optimization
description: "Generate diverse step function candidates using mathematical patterns (bipartite, multi-modal, symmetric).\nUse probe_solution to screen, evaluate the best candidates. Focus on structural step functions, not random curves."
---

# Structured Step Function Generation for Erdos C5

## Core Principle
The Erdős C5 problem rewards step functions with specific geometric structures.
Random sigmoid curves rarely achieve good bounds. Instead, directly generate step functions.

## Step 1: Generate Diverse Candidates

Use step_function_generator to create candidates from different pattern families:
- **Bipartite**: Single threshold function h(x) = 1 if x < t, else 0
- **Multi-modal**: Multiple narrow peaks separated by valleys
- **Symmetric**: Functions symmetric around x=1.0
- **Golomb-like**: Peaks at carefully spaced positions

Target: 5-10 diverse candidates covering different families.

## Step 2: Screen with probe

For each candidate:
- Call probe_solution to get approximate c5_bound
- Keep only candidates with c5_bound < 0.382 (promising)

## Step 3: Evaluate Best Candidates

For promising candidates:
- Call evaluate_solution for full score
- If combined_score > 1.0, finish!

## Step 4: Iterate

If no improvement after 3-5 cycles:
- Try different pattern families
- Adjust peak positions, widths, and heights
- Try asymmetric patterns

## Never Do
- Generate random sigmoid curves
- Rely on hyperparameter tuning without structural changes
- Expect random mutations to improve the score

## Always Do
- Generate structural step functions
- Use probe_solution for screening
- Focus on patterns known to work for similar optimization problems
