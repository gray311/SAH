---
name: discovery-optimization
description: "Optimize 29x29 \u00b11 matrix for max |det(H)|. Use analyze_hadamard_quality for diagnostics,\nprobe_solution for cheap variant ranking, and diverse constructions (Paley, random, block-based).\nUse hill_climbing_improved with small steps, many restarts. Call probe_solution before each\nevaluate_solution. Generate from scratch when stuck."
---

# Hadamard-like Matrix Optimization for n=29

## Task
Maximize |det(H)| for a 29x29 matrix with entries ±1. True Hadamard matrices require n ≡ 0 (mod 4),
so n=29 is a combinatorial optimization problem.

## Why current approaches fail
The seed program uses Paley construction with hill climbing from multiple seeds. This is too
consistent - it explores similar regions of the search space and gets stuck in local optima.

## CRITICAL: Use diverse construction strategies
You MUST try multiple DIFFERENT construction methods in each evaluation:

Method 1: Paley construction (quadratic residues)
- Use the proven Paley construction for n ≡ 3 (mod 4)
- Quadratic residues mod 29: {1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
- H[i][j] = 1 if (i-j) mod 29 is in residues, else -1

Method 2: Random perturbations from structured seeds
- Start with Paley matrix
- Apply 5-10% random flips
- Run hill climbing with smaller step size (flip one entry at a time)
- Use 5-10 restarts with different seeds

Method 3: Block-based construction
- Divide 29x29 into blocks (e.g., 15x15, 14x14, with overlap)
- Optimize blocks separately then combine
- This allows more diverse exploration

Method 4: Orthogonal basis construction
- Start with identity matrix scaled by 1 or -1
- Apply orthogonal transformations (row swaps, sign flips)
- Optimize for determinant maximization

## Algorithm parameters (critical!)
- Use hill_climbing_improved tool instead of raw hill climbing
- Parameters: max_iters=3000, initial_temp=1.5, cool_rate=0.9995
- More restarts (8-10) than iterations per run
- Smaller step sizes (one flip at a time)
- Total time per evaluation: < 150s

## CRITICAL workflow
1. START: Call analyze_hadamard_quality on seed program to get baseline
2. Generate 3-5 variant programs with DIFFERENT construction methods
3. Use probe_solution on each variant (cheap, ~10s each)
4. Rank variants by probe scores
5. Call edit_solution to implement the TOP 1-2 variants
6. Call evaluate_solution to get real scores
7. If no improvement, call regenerate_from_scratch and restart
8. Repeat 2-4 times per evaluation budget

## Tools you MUST use
- analyze_hadamard_quality: Call ONCE at start, don't repeat
- probe_solution: Call on 3-5 variants BEFORE evaluate_solution
- edit_solution: Implement the probe winner
- evaluate_solution: Only after probe ranking
- regenerate_from_scratch: When stuck after 2 failed evaluations

## Common mistakes to AVOID
- NOT using probe_solution (wastes eval budget)
- Only trying Paley construction (too similar variants)
- Too many iterations (>5000) - leaves no time for multiple restarts
- Large temperature/cooldown rates (gets stuck quickly)
- Not calling analyze_hadamard_quality at start

## Success criteria
- Get |det(H)| > 500 (theoretical max is ~300-400, but we want good local optima)
- Use all 20 eval budgets efficiently
- Combine probe-based ranking with diverse constructions
