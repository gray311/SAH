---
name: c2-mutation-exploration
description: A method playbook for C2 optimization using systematic mutation-based exploration. Generates concrete mutation operations from mutation_probe, probes 5+ variants per family, and evaluates only top 2-3 candidates. Emphasizes diversification over deep tuning.
---

# C2 Mutation Exploration Playbook

## Objective
Maximize C2 > 1.026 using systematic mutations of the seed program.

## Core Strategy: Mutation-Driven Exploration
1. Call mutation_probe to get concrete mutation operations
2. Apply mutations one at a time using edit_solution
3. Probe each variant (5+ per family) before any full evaluation
4. Evaluate only top 2-3 candidates
5. Reset (switch mutation type) after 3 stale probes

## Mutation Families (in order)

### 1. Piecewise-Linear Mutations (Seed)
- Use mutation_probe to get interval/reinit variants
- Expected: Small improvements, good baseline
- Probes needed: 5-8 before eval

### 2. Step Functions (Record Holders)
- Use mutation_probe to generate step_width/height variants
- Expected: Should achieve 0.8963+ on C2
- Probes needed: 6-10 before eval

### 3. Gaussian Mixtures
- Use mutation_probe for K/sigma/mean variants
- Expected: Smooth functions may concentrate better
- Probes needed: 5-8 before eval

### 4. B-Splines
- Use mutation_probe for knot configurations
- Expected: Flexible representation
- Probes needed: 4-6 before eval

### 5. Exponential Combinations
- Use mutation_probe for decay variants
- Expected: Natural positive functions
- Probes needed: 3-5 before eval

## Workflow
1. mutation_probe → edit → probe → probe → probe → probe → probe (5x)
2. probe_solution → rank → pick top 3 → edit → evaluate → edit → evaluate → edit → evaluate
3. If no improvement: mutation_probe again with NEW mutation type
4. finish when score > 1.026 or evals exhausted

## Key Rules
- Always call mutation_probe before editing
- Always probe 5+ times per family before evaluating
- Never spend >4 evals on same mutation type
- Diversify: cover 3+ families within first 15 probes
- Record: family, mutation type, probe score, eval score
