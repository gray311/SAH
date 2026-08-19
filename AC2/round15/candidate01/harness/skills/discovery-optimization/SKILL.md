---
name: discovery-optimization
description: "Step-function mutation protocol for C\u2082 maximization. Use analyze_and_mutate_step to generate mathematically-informed mutations of the winning step pattern. Focus on small, systematic refinements (height perturbations, width adjustments, position shifts) that preserve the architecture."
---

# C₂ Maximizer: Step Function Mutation Protocol

## Core Principle

The seed's 5-level step function is your WINNING architecture (combined_score 1.03896). Don't abandon it!
Mutate it systematically to push C₂ higher.

## Phase 1: Analysis & Mutation Generation (First iteration)

1. Call analyze_and_mutate_step ONCE to analyze current best step function

2. Understand its structure:
   - Number of levels (5)
   - Heights, widths, positions
   - Symmetry properties

3. The tool returns mutation proposals in these categories:

## Mutation Types (in order of sophistication)

**Mutation Type 1: Height Fine-Tuning**
- Perturb heights by ±0.02-0.08 (small changes)
- Goal: Optimize the ||f★f||₂² / ||f★f||_∞ ratio

**Mutation Type 2: Width Redistribution**
- Expand/contract specific intervals by 3-8%
- Goal: Spread ||f★f||₂² while controlling ||f★f||_∞

**Mutation Type 3: Asymmetric Perturbation**
- Break symmetry slightly (e.g., left width 0.22 → 0.225)
- Goal: Reduce constructive interference

**Mutation Type 4: Level Merge/Split**
- Merge two close levels or split one level into two
- Goal: Create more sophisticated step patterns

**Mutation Type 5: Position Shift**
- Shift all boundaries by ±2% of domain
- Goal: Change the effective support

## Phase 2: Probe-Based Selection

1. For each mutation type, generate 2-3 concrete implementations

2. Call probe_solution for EACH to rank them

3. Select TOP 2 by probe score for full evaluation

4. If probe scores are similar (<2% difference), try a different mutation type

## Phase 3: Full Evaluation & Iteration

1. Evaluate top variants with evaluate_solution

2. If improvement: repeat Phase 1-2 with the new best

3. If no improvement after 10 mutation cycles: try a new architecture

## Key Rules

- MUTATE THE WINNING PATTERN, don't replace it
- Use probes to filter (they're reliable for same-architecture variants)
- Small mutations first, then larger ones
- Track which mutation type works best
