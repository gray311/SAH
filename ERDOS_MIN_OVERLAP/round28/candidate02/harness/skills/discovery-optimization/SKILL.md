---
name: discovery-optimization
description: "Analyze Erdos C5 patterns structurally before training. Use validate_patterns to check validity, then train simple variants with fast iteration."
---

# Analytical Pattern Validation for Erdos Problem

## Step 1: Validate Patterns

1. CALL validate_patterns with your proposed pattern (e.g., "golomb_5", "bipartite_0.5", "tri_0.4_1.0_1.6")

2. EXAMINE the returned struct_c5_bound:
   - If struct_c5_bound >= 0.382, SKIP this pattern (will fail full eval)
   - If struct_c5_bound < 0.375, proceed to training
   - If struct_c5_bound in [0.375, 0.382), consider trying variant

3. VALIDATION CHECKS:
   - Pattern must be integral-normalized (sum(h) * dx = 1.0)
   - Pattern must have h in [0,1] for ALL intervals
   - Pattern must use N=800 intervals (domain width 2.0)

## Step 2: Fast Training Loop

1. Set num_restarts=1 (single initialization)
2. Set num_steps=30000 (quick convergence test)
3. Set penalty_strength=80 (strong integral constraint)
4. Set num_intervals=800 (standard)

5. CALL edit_solution with your validated pattern code
6. CALL probe_solution to check c5_bound
7. If probe c5_bound < 0.375, call evaluate_solution

## Step 3: Pattern Templates

### Golomb Ruler (5 marks):
marks = [0.0, 0.4, 0.8, 1.2, 1.6]
h[i] = gaussian_peak(i, center=mark, width=0.08) normalized

### Bipartite (half-half):
h[i] = 0.8 if x < 0.5 else 0.2 (normalized to integral=1)

### Tri-modal (3 peaks):
peaks = [0.4, 1.0, 1.6]
h[i] = sum of 3 Gaussians at peaks, normalized

## Workflow

1. CALL validate_patterns("pattern_name")
2. If struct_c5_bound < 0.375, proceed
3. CALL edit_solution with pattern code
4. CALL probe_solution
5. If good, CALL evaluate_solution
6. Report best combined_score
