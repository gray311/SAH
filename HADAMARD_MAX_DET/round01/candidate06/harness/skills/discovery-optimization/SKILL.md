---
name: discovery-optimization
description: "Hadamard matrix optimization: maximize |det(H)| for 29\u00d729 \u00b11 matrix. Use Paley construction, systematic search, and probe-based variant ranking under fixed evaluation budget."
---

# Hadamard Matrix Optimization (n=29)

## Objective
Maximize |det(H)| where H is 29×29 with entries ±1.

## Construction Strategies (try all in probe phase)

1. **Paley Construction (prime n≡3 mod 4)**:
   - H[0,0]=1
   - H[i,j] = 1 if (i-j mod 29) is quadratic residue, else -1
   - Quadratic residues mod 29: {1,4,5,6,7,9,13,16,20,22,23,24,25,28}

2. **Sylvester truncation**: Start with n=32 Hadamard, remove 3 rows/cols
3. **Random with many seeds**: Generate 10-20 random matrices, hill climb each

## Search Protocol
**PHASE 1 - PROBE (cheap, up to 30 calls)**:
- Implement 3-5 different constructions in parallel
- Use hadamard_probe on each (fast, separate budget)
- Keep top 2 by probe score

**PHASE 2 - FULL EVAL (budget-limited, ~20 calls)**:
- Full evaluate top 2 from Phase 1
- For the winner, refine with targeted hill climbing

**PHASE 3 - REFINEMENT**:
- Modify only the best-performing components
- Use larger perturbations, more iterations (1000-2000)
- Keep the best final result

## Perturbation Schedule (for hill climbing)
- Start: flip 1 random entry, accept if |det| increases
- Later: flip 2-3 entries, use simulated annealing acceptance
- Always maintain ±1 entries

## Bareiss Determinant
Use the provided integer-preserving Bareiss algorithm. Never use float det() - precision issues.

## Probes vs Full Eval
- hadamard_probe: fast (~10s), approximate, 30-call budget, separate from eval budget
- evaluate_solution: slow (~350s), exact, ~20-call budget

**Never call evaluate_solution more than 5-8 times on the same variant**. Use probes to filter.
