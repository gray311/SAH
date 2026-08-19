---
name: discovery-optimization
description: "Optimize step functions for Erdos minimum overlap. Generate diverse candidates, probe/rank cheaply, then evaluate. Focus on construction diversity and hybrid optimization strategies."
---

# Erdos Minimum Overlap Optimization

## Task
Minimize max_k integral(h(x)*(1-h(x+k))) dx where h: [0,2]->[0,1] and integral(h)=1.

## Strategy
DIVERSITY FIRST: Generate multiple construction methods, compare internally, then refine.

### Construction Approaches
1. Block Functions: Partition [0,2] into equal intervals, set h constant per block
2. Sine-based: h(x) = 0.5 + A*sin(B*x) adjusted for constraints
3. Random Perturbations: Start from a good seed, add controlled noise
4. Two-Bump: Concentrate mass in two regions

### Workflow
1. Call generate_variants(num=5) to create diverse candidates
2. For each candidate, call probe_solution to get quick scores
3. Rank candidates: top 3 get gradient descent refinement
4. For each refined candidate: edit_solution, evaluate_solution
5. Track best combined_score (0.380923.../C5_bound). Must exceed 1.0.

### Debugging
- If validity=0: check sigmoid clips values, integral penalty, array sizes
- If scores don't improve: try different construction method, adjust learning rate
- If timeout: reduce num_steps or num_intervals

## Tools
- generate_variants: Creates N diverse step functions using different strategies
- probe_solution: Cheap score on ~2000-row subsample, doesn't cost evaluation budget
- edit_solution: Modify EVOLVE-BLOCK code
- evaluate_solution: Official score (costs evaluation budget)
- finish: End session when done
