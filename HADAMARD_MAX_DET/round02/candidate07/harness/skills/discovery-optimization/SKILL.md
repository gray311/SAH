---
name: discovery-optimization
description: "Optimize 29x29 \u00b11 matrix for maximal |det(H)| using Paley construction. Use numpy trace(A^T @ A) for fast search loops, Bareiss only once per search. Run 3-5 independent searches (<200s total). Use probe_solution for variant ranking."
---

# 29x29 Hadamard-like Matrix Optimization

## Mathematical Context
- n=29 is prime ≡ 3 (mod 4), no true Hadamard exists (n√n ≈ 155.5 is theoretical max)
- Paley construction is the best starting point for primes ≡ 3 (mod 4)
- QR mod 29 = {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}

## FAST Search Strategy (CRITICAL)

### Step 1: Use numpy proxy scoring inside search loops
Inside hill climbing, NEVER call exact Bareiss determinant repeatedly.
Instead use: proxy_score(A) = |trace(A^T @ A) - n²|
These run in <0.1s for n=29 and correlate with |det| direction.

### Step 2: Structure each search to complete quickly
- Each search: 2000-3000 iterations max (proxy score for each step)
- Run 3-5 searches per evaluation
- Only compute exact Bareiss determinant ONCE at the end of each search
- Total time target: <200s per evaluation

### Step 3: Multi-start with diverse seeds
For each search:
- Start from Paley matrix
- Try 3-5 different random perturbations before hill climb
- Use seeds: 42, 123, 456, 789, 1011
- Different perturbation patterns (corner, center, diagonal flips)

### Step 4: Acceptance criteria in hill climbing
- Accept improvements always (when proxy score improves)
- Accept worsened with prob: exp((|new_proxy| - |old_proxy|) / T)
- Temperature schedule: T = 2.0 → 0.1 over iterations
- Cooling rate: 0.9985

### Step 5: Use probe_solution for final variant ranking
- After all searches complete, you have multiple candidate matrices
- Create 2-3 "finalized" variants (cleaned up, validated)
- Use probe_solution to rank them (~10s each)
- Evaluate only the top 1-2 candidates with evaluate_solution

## Time Budget Discipline
- Total evaluation time MUST stay < 200s (leaves margin)
- If a search takes >30s, it's too slow - reduce iterations
- Allowed proxy iterations per search: ~3000 (each <0.1s)
- Allowed exact Bareiss calls per eval: ≤5 (each 5-10s)

## Complete Code Structure Template
```python
def construct_hadamard_matrix():
    # 1. Build Paley matrix once
    paley = build_paley_matrix(29, qr={0,1,4,5,6,7,9,13,16,20,22,23,24,25,28})
    
    candidates = []
    max_total_time = 180  # seconds
    
    start_time = time.time()
    
    # 2. Run 3-5 searches
    for search_num in range(3):
        if time.time() - start_time > max_total_time:
            break
        
        # 3. Perturb starting matrix 3-5 ways
        perturbations = get_perturbations(paley, n_perturb=5)
        best_for_search = None
        best_det = 0
        
        for pert_idx, pert in enumerate(perturbations):
            if time.time() - start_time > max_total_time:
                break
            
            # 4. Hill climb with PROXY scoring (NOT Bareiss!)
            A, proxy_best = hill_climb_proxy(pert, n_iter=2500)
            
            # 5. Only NOW compute exact determinant (Bareiss once per perturbation)
            exact_det = compute_bareiss(A)
            if abs(exact_det) > best_det:
                best_det = abs(exact_det)
                best_for_search = A
        
        if best_for_search is not None:
            candidates.append((best_for_search, best_det))
    
    # 6. Pick best overall candidate
    best = max(candidates, key=lambda x: abs(x[1])) if candidates else paley
    return best[0] if candidates else paley
```

## Tools Usage
- edit_solution: Full rewrite of construct_hadamard_matrix if structure needs changing
- evaluate_solution: Call after search completes. Track your best combined_score.
- probe_solution: Before final evaluate, create 2-3 finalized variants, probe them, pick winner
- finish: When you've exhausted meaningful improvements

## Common Errors to Avoid
- ❌ Calling Bareiss inside hill climbing loop (causes timeout)
- ❌ Too many iterations (>5000 per search)
- ❌ Only one search per evaluation (not enough exploration)
- ❌ Ignoring time budget (always check elapsed time)
- ✅ Use numpy trace for fast iteration proxy scoring
- ✅ Only call exact Bareiss once per search (or at most once per perturbation)
- ✅ Run 3-5 searches per evaluation
- ✅ Use probe_solution before final evaluate
