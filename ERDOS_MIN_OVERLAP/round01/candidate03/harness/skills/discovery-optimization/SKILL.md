---
name: discovery-optimization
description: "Mathematical optimization for the Erd\u0151s minimum overlap problem. Use pattern exploration and bounded internal search to find step functions that minimize C5 bound. Try multiple constructions per evaluation and report the best."
---

# Erdős C5 Minimization Strategy

## Core Approach

The C5 problem seeks a step function h: [0, 2] → [0, 1] with ∫h(x)dx = 1 that minimizes the maximum autocorrelation max_k ∫ h(x)(1 - h(x+k)) dx.

## Key Strategy: Pattern Exploration + Bounded Search

**DO NOT** run long gradient descent (20000+ steps) in a single evaluation. Instead:

1. **INTERNAL SEARCH LOOP**: Run multiple restarts (5-10) with different initialization patterns
2. **BUDGETED OPTIMIZATION**: Use 200-500 optimization steps per restart (total 2500-5000 steps across all restarts)
3. **DIVERSITY**: Try different construction patterns as initializations
4. **BEST RESULT**: Return the best C5 bound found across all attempts

## Recommended Initialization Patterns

- **Random + Momentum**: Multiple random initializations with momentum-based SGD
- **Periodic Block**: Construct h as repeating blocks of [a, 1-a] pattern
- **Alternating Strategy**: High/low value patterns with varying block sizes
- **Peak-Avoidance**: Place higher values away from k=1 region to minimize overlap

## Constraint Handling

Use projection or penalty: after each update, ensure:
- h[i] = max(0, min(1, h[i])) for all i
- Scale so sum(h) * dx ≈ 1.0

## Tool Usage

- `pattern_searcher`: Call this to generate and evaluate multiple pattern-based candidates
- `edit_solution`: Use to change the internal optimization strategy
- `evaluate_solution`: Call once at the end with your best attempt only

## Time Budget Reality

The evaluator has a time limit. Aim to complete your internal search in < 15 seconds, leaving margin for the evaluator overhead. Better to evaluate 10 quick candidates than 1 slow one.
