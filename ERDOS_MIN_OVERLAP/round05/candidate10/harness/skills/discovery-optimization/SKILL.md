---
name: discovery-optimization
description: "C5 bound discovery: Focus on algorithm diversity. Try population-based, evolutionary, and constructive methods. Use probes to compare variants. Switch algorithm families when stuck."
---

# C5 Bound Discovery Strategy

Problem: Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx
Constraints: h in [0,1], integral(h)=1
Goal: Beat C5 <= 0.38092303510845016 (achieve combined_score > 1)

## Algorithm Families

### 1. Population-Based (Recommended First)
- Population: 10-20 candidates, each = random or pattern-initialized latent
- Per candidate: 5000-10000 optimization steps
- After all done: select top 3, do local refinement
- Keep global best

### 2. Evolutionary Strategy
- Start: 20 random candidates
- For generation in 500..2000:
    - Score all candidates
    - Select parents (top 10%)
    - Crossover: blend latent vectors
    - Mutate: add Gaussian noise
    - Tournament selection
- Keep population diverse

### 3. Constructive Approach
- Try explicit patterns:
  * Two-plateau: h(x) = 1 for x in [a, 2-a], 0 otherwise
  * Triangular: h(x) = max(0, 1 - |x-c|/w)
  * Three-level: piecewise constant at levels 0, 0.5, 1
- Grid search parameters
- Local refinement of best

### 4. Simulated Annealing
- Start: random valid h
- For step in 1..2000:
    - Propose small perturbation
    - Accept if: new < old OR exp(-(new-old)/T)
- Anneal T from 1.0 to 0.01

## Execution Plan
Round 1-3: Test 3-4 algorithm families with probes
Round 4-6: Full evaluate top 2-3 winners
Round 7+: Refine best approach

Remember: COMPLETE REWRITES > parameter tweaks. Use probes aggressively.
