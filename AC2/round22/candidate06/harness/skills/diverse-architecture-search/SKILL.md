---
name: diverse-architecture-search
description: Search diverse step function architectures from the seed library, probe many, refine winners.
---

# Diverse Architecture Search Protocol

## Phase A: Architecture Discovery (iterations 1-10)

1. Call sample_step_patterns to extract ALL patterns from the seed

2. Sample 5 DISTINCT patterns (different peak configurations, different number of levels)

3. Probe ALL 5 with probe_solution

4. Rank by probe score, pick TOP 2

5. Evaluate both if budget allows, otherwise refine top 1

## Phase B: Deep Refinement (iterations 11-20)

1. For each top pattern:
   - Make SUBSTANTIVE edits: change 2-3 heights, shift peaks by 10%+ of domain
   - Use JAX gradients to refine interval boundaries
   - Try both ascent and descent directions

2. Create hybrid patterns: combine best features (peak heights from A, widths from B)

3. Probe hybrids before full eval

## Phase C: Aggressive Innovation (iterations 21-30)

1. If no improvement, sample 3 new patterns from library

2. Probe all, evaluate top 1

3. Restart from scratch if stuck for >5 iterations

## Key Rules
- Always sample from STEP PATTERN LIBRARY first
- Never make tiny tweaks (<5%) - make substantive changes
- Use probes to explore 8-10 architectures before any full eval
- Gradient is for polishing, not discovery
