---
name: hyperparameter-exploration-playbook
description: Guide for exploring hyperparameter space in Erdos optimization. Focus on varying lr, penalty, steps, and num_restarts around the seed's good initialization.
---

# Hyperparameter Exploration Playbook for Erdos Optimization

## Core Principle
The seed program's initialization is strong. DON'T try to improve it.
Instead, explore HOW to optimize FROM those seeds better.

## Search Space to Explore

### Learning Rate (lr): 0.001 - 0.05
- Low lr (0.001-0.005): Good for fine-tuning near optimum, but may be slow
- Medium lr (0.01-0.02): Balanced, good for moderate optimization
- High lr (0.03-0.05): Risky but can escape shallow local minima

### Penalty Strength: 500 - 20000
- Low penalty (<1000): May not enforce ∫h=1 constraint tightly
- Medium penalty (1000-5000): Good balance
- High penalty (>10000): Enforces constraint but may hurt objective

### Optimization Steps: 10000 - 80000
- Short (10000-20000): Quick but may not converge
- Medium (30000-50000): Good balance for most cases
- Long (60000+): Best for high-stakes final tuning

### Number of Restarts: 3 - 20
- Few restarts (3-5): May miss global optimum
- Medium restarts (10-15): Good coverage
- Many restarts (20+): Comprehensive but expensive

## Probe-First Strategy

1. **Generate 150 hyperparameter combinations** using hypergrid_search
2. **Run 500-1000 optimization steps** for each (not full training)
3. **Probe** each result to estimate c5_bound
4. **Rank by probe score**, take top 10
5. **Run full evaluation** on top 3-5 candidates
6. **Analyze patterns** in successful combos (analyze_probe_results)
7. **Iterate**: Focus next search round on promising patterns

## Red Flags (When to Change Strategy)
- If all probes give combined_score < 0.9995: May need different initialization
- If best score uses lr=0.05 but penalty varies wildly: Constraint not helping
- If best score uses very long steps (>60000): May be stuck in local min

## Success Criteria
- combined_score > 1.0 means we found c5_bound < 0.380923
- Stop when we can't beat current probe results with remaining budget
