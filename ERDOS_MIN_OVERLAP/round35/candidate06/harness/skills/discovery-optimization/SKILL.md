---
name: discovery-optimization
description: "Generate diverse step function patterns (bipartite, multi-modal, Golomb-like), probe them cheaply, evaluate the best. Do random hyperparameter tuning only after exhausting pattern-based approaches."
---

# Erdos C5 - Pattern Exploration Strategy

## Phase 1: Generate Diverse Patterns

Create 10-15 diverse initial step functions:

### Bipartite Patterns
For threshold values a = 0.25, 0.33, 0.4, 0.5, 0.6, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5:
h(x) = 1.0 if x < a, else 0.0
Then scale to ensure integral = 1.

### Multi-modal Patterns (3 peaks)
For peak centers in [(0.2, 0.8, 1.6), (0.3, 0.9, 1.7), (0.25, 0.75, 1.5), (0.35, 0.85, 1.65)]:
h(x) = sum of Gaussian-like bumps at each center, clamped to [0,1]
Normalize to integral = 1.

### Golomb Ruler Pattern
h(x) = 4.0 for x in [0.0-0.12, 0.4-0.52, 0.8-0.92, 1.2-1.32, 1.6-1.72], 0 elsewhere
Scale to integral = 1.

### Sinusoidal Patterns
h(x) = sigmoid(a*sin(2*pi*x/b) + c) where (a,b,c) vary
Ensure integral = 1 by scaling.

## Phase 2: Probe and Filter

1. For EACH pattern:
   - Call probe_solution
   - Record approximate c5_bound
   - Keep patterns with c5_bound < 0.385

2. Sort kept patterns by c5_bound (ascending)

3. Select TOP 3 patterns

## Phase 3: Full Evaluation

1. For each of the top 3 patterns:
   - Call evaluate_solution
   - Record combined_score

2. If ANY combined_score > 1.0:
   - Call finish with summary of best pattern

3. If NONE work:
   - Proceed to Phase 4 (targeted perturbations)

## Phase 4: Targeted Perturbations (Only if Phase 3 fails)

1. If seed program is still best:
   - Call correlation_analyzer to find problematic k values
   - Call structure_inspired_mutations with target_shifts=[problematic k]
   - Generate 3-5 mutations
   - Probe each, evaluate best 1-2

## Critical Rules
- ALWAYS generate diverse patterns FIRST
- NEVER tune hyperparameters before testing patterns
- Use probe to screen, evaluate to confirm
- Stop as soon as combined_score > 1.0
