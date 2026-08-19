---
name: discovery-optimization
description: "Deterministic mathematical constructions replace failed random pattern approach for Erdos minimum overlap optimization."
---

# Deterministic Constructions Strategy

The random pattern approach (12 patterns with Gaussian noise) completely failed across 8 harness attempts. The solution is to use DETERMINISTIC, mathematically principled constructions with NO randomness.

## Five Constructions to Implement

### 1. BIMODAL_TIGHT
Two narrow symmetric peaks:
x = linspace(0,2,N)
latent = exp(-((x-0.25)/0.12)**2 * 25) + exp(-((x-0.75)/0.12)**2 * 25)

### 2. TRIANGULAR_3STEP
Three-level step function:
levels = [10.0, 0.0, -5.0]
phases = [0.0, 1/3, 2/3]
latent = zeros(N)
for phase, level in zip(phases, levels):
    latent += level * (I(x>=phase) - I(x>=phase+1/3))

### 3. GOLOMB_5
Peaks based on Golomb ruler spacing:
marks = [0.0, 0.5, 1.5, 2.5, 2.0]
widths = [0.08, 0.12, 0.08, 0.10, 0.10]
latent = zeros(N)
for mark, width in zip(marks, widths):
    latent += 8.0 * exp(-((x-mark)/width)**2 * 20)

### 4. BIQUADRATIC_4PEAK
Four peaks for fine control:
peak_x = [0.2, 0.4, 1.0, 1.6]
bw = 0.08
latent = zeros(N)
for px in peak_x:
    latent += 6.0 * exp(-((x-px)/bw)**2 * 25)

### 5. PERIODIC_ALTERNATING
Simple alternating pattern:
periodic = 2*(x<0.5) - 1
latent = periodic * 3.0

## Scaling for Integral Constraint

For each construction:
h = sigmoid(latent)
dx = 2.0 / N
scale = 1.0 / (sum(h) * dx)
h = h * scale

## Phased Optimization Strategy

Run 120000 optimization steps with three phases:
Phase 1 (steps 0-40000): lr=0.01, penalty=5000
Phase 2 (steps 40000-80000): lr=0.003, penalty=15000
Phase 3 (steps 80000-120000): lr=0.001, penalty=50000

## Complete Workflow

1. Generate 4-5 deterministic constructions (ZERO randomness allowed)
2. For each: run 30000 optimization steps with phased settings
3. Use probe_solution to get approximate c5_bound for each
4. Rank by probe score
5. Run evaluate_solution on top 2 candidates
6. Submit result with best combined_score

## Hyperparameter Changes Required

num_steps = 120000 (was 59000)
num_restarts = 2 (was 3)
base_learning_rate = 0.01 (was 0.0053)
penalty_strength = 5000 (phased up to 50000)

## Success Criterion

combined_score > 1.0 means c5_bound < 0.38092303510845016
