---
name: hadamard-optimization
description: Hadamard matrix construction for n=29. Use Paley (quadratic residues) as primary method. Systematic workflow - probe multiple constructions (Paley, Sylvester, random), fully eval top 2, then refine with hill climbing. Always use hadamard_probe before full eval.
---

# Hadamard Matrix Optimization (n=29)

## Construction Strategies

### 1. Paley Construction (PRIMARY METHOD)
- H[0,0]=1
- For i,j: H[i,j] = 1 if (i-j mod 29) in quadratic residues, else -1
- Quadratic residues mod 29: {1,4,5,6,7,9,13,16,20,22,23,24,25,28}
- This is the MOST important baseline - implement correctly!

### 2. Sylvester Truncation
- Start with n=32 Sylvester Hadamard (recursive Kronecker product)
- Remove 3 rows and 3 columns to get 29×29
- Try different removal combinations

### 3. Random Multiple Starts
- Generate 10-20 random ±1 matrices
- Apply hill climbing (500-1000 iterations each)

## Search Workflow

**PHASE 1: Probe (cheap, up to 30 calls)**
1. Implement Paley construction
2. Implement Sylvester truncation (try 3-5 truncations)
3. Implement random + hill climb (2-3 variants)
4. Call hadamard_probe on each variant
5. Pick top 1-2 by probe score

**PHASE 2: Full Evaluation (~20 calls)**
1. Full evaluate top 2 from Phase 1
2. For the winner, create 2-3 refinements
3. Probe refinements, full eval best

**PHASE 3: Refinement**
1. Take the best full-eval result
2. Apply targeted perturbations (flip 2-3 entries)
3. Run 1000-2000 hill climbing iterations
4. Final full eval, then finish

## Key Parameters
- Hill climbing iterations: 500 (probe) to 2000 (full)
- Temperature: start 0.5, decay 0.001 per iteration
- Bareiss determinant: mandatory, never use numpy det()

## Budget Discipline
- Use hadamard_probe FIRST to rank variants
- Only FULL EVAL the top 1-2 probe-ranked variants
- Never call evaluate_solution more than 5-8 times on same variant
