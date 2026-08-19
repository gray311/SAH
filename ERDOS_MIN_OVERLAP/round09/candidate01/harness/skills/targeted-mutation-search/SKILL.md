---
name: targeted-mutation-search
description: Targeted mutation search for Erdos minimum overlap - analyze current solution, generate systematic mutations, probe to rank, evaluate winners.  This skill guides you to NOT just restart with random patterns, but to - 1. Understand what you have 2. Mutate it intelligently 3. Use probes to efficiently find improvements
---

# Targeted Mutation Search for Erdos Problem

## The Problem with Random Restarts
The current harness kept failing because it only offered static constructions
(bimodal, triangular, Golomb) but no way to IMPROVE upon them.

## Our New Strategy
1. **Analyze first**: Use analyze_current_best() to understand your current solution's structure
   - How many peaks? Where are they? What widths?
   - This tells you WHAT to mutate

2. **Targeted mutations**: Use analyze_and_mutate() to generate mutants that:
   - Shift peaks slightly (±0.05) - maybe optimal is at 0.22 not 0.25
   - Adjust widths - maybe peaks should be broader/narrower
   - Try different bimodal splits - maybe 0.3 or 0.7 works better
   - Create asymmetric patterns - maybe unequal peaks are better

3. **Probe-based screening**: Before spending full evaluations:
   - Call probe_solution() on each mutant (fast, ~10s, separate budget)
   - This lets you screen 10+ mutants with only a few full evaluations
   - Keep only the top 2-3 by probe score

4. **Full evaluation**: Only call evaluate_solution() on your top candidates
   - Aim for combined_score > 1.0 (c5_bound < 0.380923)
   - If none beat it, iterate: analyze the best probe result, mutate again

## Key Principles
- Don't just generate and forget: understand what you're mutating
- Use probes religiously: they're cheap, full evals are expensive
- Keep iterating: mutation -> probe -> mutation -> probe -> evaluate
- The seed solution likely has 2 peaks around 0.25, 0.75; try perturbing this
- A split at 0.5 (midpoint) might be worse than 0.3 or 0.7
- Track your progress: what mutation types worked?
