---
name: recombination-mutation-strategy
description: Diversified pattern recombination strategy. Combine elements from multiple seed patterns rather than perturbing one.
---

# C₂ Maximizer: Pattern Recombination Strategy

## Core Principle

DON'T perturb one pattern. RECOMBINE 2-3 different seed patterns to create novel architectures.

## Recombination Methods

### Method 1: Peak Height Mixing
- Take heights from pattern 2 (high peak: 1.60), pattern 7 (very high: 2.20), pattern 11 (pyramid: 2.10)
- Combine to create: 1.60, 2.00, 1.40, 1.30, 1.50
- Rationale: Mix of different peak strategies

### Method 2: Core-Width Expansion
- Take central interval from pattern 5 (0.22-0.38, 0.52-0.82), expand by 15-20%
- Result: Central core width increased to capture more convolution support
- Add asymmetric wings: 0.15-0.22, 0.82-0.95

### Method 3: Multi-Level Recombination
- Pattern 3 has 3 levels (0.90, 1.90, 0.90)
- Pattern 6 has 4 levels (0.70, 1.30, 1.70, 1.00)
- Combine: 0.90, 1.90, 1.30, 1.70 (4 distinct levels)
- Rationale: More levels = richer convolution structure

### Method 4: Asymmetric Staircase
- Pattern 8 is a staircase (0.60, 1.00, 1.50, 1.20)
- Make more asymmetric: 0.70, 1.20, 1.80, 1.40, 1.10
- Rationale: Breaking symmetry may reduce ||f★f||∞

## Execution Protocol

1. Call pattern_recombiner for 2-3 complete new patterns
2. Pick ONE, implement with edit_solution (COMPLETE change)
3. Evaluate with evaluate_solution (ONE eval per idea)
4. If no improvement: Try a COMPLETELY different recombination strategy
5. Never iterate on the same pattern for more than 2 evals

## Key Warning

Each evaluation is precious. ONE eval, ONE complete architectural change, then move to the next idea.
