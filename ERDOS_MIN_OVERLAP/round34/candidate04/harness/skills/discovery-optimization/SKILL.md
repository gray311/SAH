---
name: discovery-optimization
description: "Generate diverse step function constructions from scratch (bipartite, multi-peak, Golomb-ruler, etc.), verify constraints, then optimize the best candidate with JAX gradient descent. Avoid myopic structural mutations."
---

# Diverse Initialization + JAX Optimization Strategy

## Phase 1: Generate Diverse Base Shapes (CRITICAL)

The current harness fails because it only does structural mutations from the seed. We need COMPLETELY DIFFERENT shapes first.

### Construction 1: Bipartite (Threshold Function)
h(x) = 1 if x < t, else 0
- Set t = 1.0 for integral = 1
- Verify: integral = t = 1.0 ✓

### Construction 2: Three-Peak Square Wave
h(x) = 1 if x ∈ [0.25, 0.75] ∪ [1.25, 1.75], else 0
- Integral = 0.5 + 0.5 = 1.0 ✓

### Construction 3: Four-Peak Square Wave
h(x) = 1 if x ∈ [0.2, 0.6] ∪ [1.0, 1.4], else 0
- Integral = 0.4 + 0.4 = 0.8 → Need to scale! 
- Actually: h(x) = 1.25 for x ∈ [0.2, 0.6] ∪ [1.0, 1.4], else 0
- Integral = 0.4*1.25 + 0.4*1.25 = 1.0 ✓

### Construction 4: Golomb-Ruler Like
h(x) = 1 at discrete points {0.1, 0.3, 0.7, 1.1, 1.5, 1.9}, else 0
- Scale to get integral = 1
- Each point gets weight 1/6 ≈ 0.1667

### Construction 5: Triangular Pulse
h(x) = triangular function centered at 1.0, width 1.0, height 2.0
- h(1.0) = 2.0, h(0.5) = h(1.5) = 1.0, h(0) = h(2) = 0
- Integral = area of triangle = 0.5 * base * height = 0.5 * 1.0 * 2.0 = 1.0 ✓

### Construction 6: Two-Plateau
h(x) = 0.5 for x ∈ [0.25, 0.75], else 0
- Integral = 0.5 * 0.5 = 0.25 → NOT VALID!
- Fix: h(x) = 2.0 for x ∈ [0.25, 0.75], else 0
- Integral = 2.0 * 0.5 = 1.0 ✓

## Phase 2: Quick Probe Ranking

1. For each construction, compute c5_bound using ctx.probe_solution (cheap)
2. Keep top 2 candidates with lowest c5_bound
3. Verify constraints (h in [0,1], integral = 1)

## Phase 3: JAX Optimization

For the best 1-2 candidates:

### Optimization Setup
- Learning rate: 0.001 (small for fine-tuning)
- Steps: 20000 (enough to escape local minima)
- Penalty strength: 15.0 (for integral constraint)
- Gradient clipping: norm 1.0 (prevent exploding gradients)

### Training Loop
1. Initialize h from chosen construction
2. For each step:
   - Compute c5_bound = max_k integral h(x)(1-h(x+k))dx
   - Compute gradient = d(c5_bound) / d(h)
   - Apply gradient descent with penalty term
   - Clip gradient norm
3. After 20000 steps, return final h

## Phase 4: Final Evaluation

1. Call evaluate_solution on optimized h
2. If combined_score > 1.0 (c5_bound < 0.38092303510845016), finish
3. If not, try different constructions

## Key Rules
- ALWAYS generate 3-5 DIVERSE constructions first
- Use probe_solution to rank before full evaluation
- NEVER do structural mutations without a good base shape
- Small learning rate (0.001) for fine-tuning
- Verify integral(h) = 1 EXACTLY before evaluating
