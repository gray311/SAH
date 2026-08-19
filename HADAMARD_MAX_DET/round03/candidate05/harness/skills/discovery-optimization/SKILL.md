---
name: discovery-optimization
description: "Maximize |det(H)| for 29x29 \u00b11 matrix via sequential refinement. n=29 \u2261 3 mod 4, Paley construction works.\\n\\nUse ONLY ONE construction method per evaluation. Seed next evaluation from previous best result.\\nRun 25,000-30,000 iterations with numpy.linalg.det. Try cooling schedules sequentially.\\nProbe 2-3 variants before each full evaluation.\\nOnly switch methods after 3+ plateaus."
---

# Sequential Hadamard Optimization for n=29

## Core Principle: Sequential Refinement

**DO NOT try multiple methods in one evaluation.** Each of your 20 evaluations should:
1. Take the BEST result from the previous evaluation as the seed
2. Run ONE construction method to near-convergence
3. Evaluate and keep the result
4. Repeat with refinements

Only after 3+ consecutive evaluations with <1% improvement should you try a different construction method.

## Construction Methods (Use One at a Time)

### Method A: Paley Construction (Primary)
Quadratic residues mod 29: {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
- Start with Paley matrix
- Run simulated annealing: 25,000-30,000 iterations
- Use numpy.linalg.det for all iterations

### Method B: Random Start + Refinement
- Generate random ±1 matrix with fixed seed
- Run simulated annealing: 20,000-25,000 iterations
- Use as fallback if Paley plateaus

## Simulated Annealing Parameters

Try these COOLING SCHEDULES SEQUENTIALLY across evaluations:
1. Schedule 1: initial_temp=5.0, cool_rate=0.998
2. Schedule 2: initial_temp=2.5, cool_rate=0.995
3. Schedule 3: initial_temp=1.0, cool_rate=0.992

For each evaluation, try 2-3 seeds with the same parameters, pick best.

## Determinant Calculation
- SEARCH: numpy.linalg.det (fast, ~0.001s per 29×29 matrix)
- VALIDATION: Bareiss only on final result
- NEVER use Bareiss during hill climbing (causes timeout)

## Workflow
1. Evaluation 1: Paley + Schedule 1, 25k iters, 3 seeds
2. Use best result as seed for Evaluation 2
3. Try Schedule 2 with same Paley start
4. If improved: Continue with Schedule 3
5. If plateau: Try different schedule or random start
6. Always probe 2-3 variants before full evaluation
7. End when score converges or budget exhausted

## Critical Rules
- ✅ Seed next evaluation from previous best
- ✅ ONE method per evaluation
- ✅ 25,000+ iterations per evaluation
- ✅ numpy.linalg.det for all search
- ✅ Probe before evaluate
- ❌ NO parallel method exploration in one evaluation
- ❌ NO fresh start each evaluation (wastes convergence progress)
