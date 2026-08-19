---
name: discovery-optimization
description: "Break through by replacing Gaussian initialization with hard-coded piecewise constant patterns and local breakpoint search. FFT evaluation is fast enough for direct full evaluation; use all 30 evals to test 3-5 constructions with local refinement."
---

# Erdos Minimum Overlap - Piecewise Constant Initialization

## The Problem
The seed's 12 patterns are all Gaussian/sigmoid-based smooth functions. They all cluster in the SAME basin of attraction. The optimizer cannot escape because all starts are similar.

## The Solution: PIECEWISE CONSTANTS
Replace the 12 Gaussian patterns with 3-5 HARDWIRED piecewise constant functions:
- Bipartite: h=1 on [0,a], h=0 on [a,2-a], h=1 on [2-a,2] (symmetric)
- Trichotomous: h=1 on [0,a], h=0 on [a,b], h=1 on [b,2]
- Pentatomic: h=1 on [0,a], h=0.5 on [a,b], h=0 on [b,2]

## Implementation Steps

### Step 1: Replace _get_best_initialization
Edit the seed to replace _get_best_initialization with:

```python
def _get_best_initialization(self, seed: int) -> jnp.ndarray:
    N = self.hypers.num_intervals
    hardcoded_patterns = [
        {'type': 'bipartite', 'breaks': [0.5, 1.5], 'heights': [1.0, 0.0]},
        {'type': 'trichotomous', 'breaks': [0.5, 1.0, 1.5], 'heights': [1.0, 0.0, 0.0]},
        {'type': 'pentatomic', 'breaks': [0.5, 1.0, 1.5], 'heights': [1.0, 0.5, 0.0]},
        {'type': 'asymmetric', 'breaks': [0.4, 0.6, 1.4, 1.6], 'heights': [1.0, 0.5, 0.0]},
    ]
    best_h = None
    best_obj = jnp.inf

    for pat in hardcoded_patterns:
        h = jnp.zeros(N)
        for i, (b, hgt) in enumerate(zip(pat['breaks'], pat['heights'])):
            idx = int(b * N)
            if i < len(pat['breaks']) - 1:
                next_b = pat['breaks'][i+1]
                h[idx:int(next_b*N)] = hgt
        # Local search: try 5 perturbations of each breakpoint
        best_pat_h = h
        best_pat_obj = jnp.inf
        for delta in [-0.02, -0.01, 0.0, 0.01, 0.02]:
            h_test = jnp.zeros(N)
            for i, (b, hgt) in enumerate(zip(pat['breaks'], pat['heights'])):
                idx = int((b + delta) * N)
                if i < len(pat['breaks']) - 1:
                    next_b = pat['breaks'][i+1]
                    h_test[idx:int((next_b + delta) * N)] = hgt
            obj = self._compute_c5_bound(h_test)
            if obj < best_pat_obj:
                best_pat_obj = obj
                best_pat_h = h_test
        if best_pat_obj < best_obj:
            best_obj = best_pat_obj
            best_h = best_pat_h

    return best_h
```

### Step 2: Edit Solution
Edit the seed to:
- Replace _get_best_initialization with the code above
- Set num_restarts=1, seed_start=0
- Keep _objective_fn and _optimize_single_run as-is (they handle the constraint penalty)

### Step 3: Local Refinement (Optional but Recommended)
After the first run, EDIT again to add a BINARY SEARCH over breakpoints:
- For each breakpoint, try 3 refinement levels: ±0.01, ±0.02, ±0.05
- Keep the configuration with lowest c5_bound
- This can squeeze out 0.001-0.005 improvement

### Step 4: Direct Evaluation
The FFT evaluator is FAST (<10ms for 800 intervals). Do NOT use probe_solution for screening. Call evaluate_solution directly on each construction.

## Expected Outcome
- Piecewise constants can achieve c5_bound ~ 0.35-0.37 (vs. 0.38+ for Gaussian starts)
- combined_score > 1.0 (i.e., c5_bound < 0.380923)
- Use all 30 evals: test 3-5 constructions with local refinement
