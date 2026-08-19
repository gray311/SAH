---
name: fast-hadamard-search
description: Task-specific skill for fast 29x29 Hadamard optimization. Uses numpy trace for proxy scoring in search loops, multi-start exploration, and strict time budget discipline. Call before each evaluation.
---

# Fast Hadamard Search for n=29

## CRITICAL TIME DISCIPLINE
- Total evaluation time MUST stay <200s (leaves 150s margin)
- Each exact Bareiss determinant takes 5-10s for n=29
- Use numpy trace(A.T @ A) for ALL search loop iterations (<0.1s each)
- Only call exact Bareiss ONCE at end of each search

## Search Structure
1. Build Paley matrix once (QR mod 29 = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28})
2. Run 3-5 independent searches per evaluation
3. Each search: 2000-3000 proxy iterations + 1 exact Bareiss
4. Use multiple seeds: 42, 123, 456, 789, 1011
5. For each seed: 2-3 perturbations before hill climbing
6. Pick best candidate from all searches

## Proxy Scoring Strategy
- proxy_score(A) = |trace(A^T @ A) - n²|
- This correlates with |det(A)| for ±1 matrices
- Use for ALL move acceptance in hill climbing
- ONLY call exact Bareiss at the END of each search

## Hill Climbing Parameters
- Iterations: 2500 per search (proxy-scoring only)
- Initial temperature: T = 2.0
- Cooling rate: 0.9985
- Accept improvements always (proxy score improvement)
- Accept worsened with prob: exp(-(proxy_new - proxy_old)/T)

## Final Selection
- After all searches, you have multiple candidates
- Create 2-3 finalized variants (validate structure)
- Use probe_solution to rank (~10s each)
- Evaluate only the probe winner with evaluate_solution

## Common Pitfalls
- ❌ Calling Bareiss inside search loop (causes timeout)
- ❌ Too few searches (not enough exploration)
- ❌ Ignoring time budget
- ✅ Always use numpy trace for proxy scoring
- ✅ Always limit exact Bareiss to once per search
- ✅ Always run 3-5 searches per evaluation
