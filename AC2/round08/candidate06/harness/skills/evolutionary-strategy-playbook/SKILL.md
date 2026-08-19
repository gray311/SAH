---
name: evolutionary-strategy-playbook
description: Playbook for evolutionary search in C2 maximization. Use population-based search with diverse initial patterns.
---

# Evolutionary Strategy for C2 Maximization

## Why Evolutionary Search?

The seed uses gradient-based optimization which is STUCK. Evolutionary search explores the
discrete step-function space differently, avoiding local minima.

## Step 1: Generate Diverse Population

CALL generate_evolutionary_population immediately:

- Creates 8-12 diverse step patterns
- Each with random heights, widths, and multi-level structures
- NOT based on seed's 13 similar patterns

## Step 2: Evaluate Population

- Run probe_solution on all population members (~10 probes)
- Rank by probe score
- Select top 3-4 for full evaluation

## Step 3: Iterative Evolution

For each generation (aim for 5-8 generations):

1. From top performers, create mutants:
   - Height mutation: +/-15% change on intervals
   - Width mutation: shift interval boundaries by +/-5%
   - Add/remove levels: increase/decrease complexity

2. Create crossovers:
   - Mix interval structures from different parents
   - Blend height profiles

3. Probe all new variants (5-8 probes per generation)

4. Evaluate top 2 of each generation

## Key Principles

- DIVERSITY > refinement of same approach
- Populations should span different scales, not just optimize one pattern
- Use probes aggressively to filter before expensive evaluations
- Keep track of ALL best performers, don't discard after one eval

## Expected Timeline

- Generation 1: probe all 8-12, eval top 2
- Generations 2-5: evolve from best, probe 6, eval 2 per gen
- Generations 6-8: refine promising lines, eval final top 1-2

## Success Metric

- Any candidate beating seed's 1.03431 is a win
- Target: 1.05+ by exploring fundamentally different step patterns
