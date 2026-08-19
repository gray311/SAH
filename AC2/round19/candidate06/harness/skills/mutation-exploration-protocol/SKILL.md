---
name: mutation-exploration-protocol
description: Systematic mutation of seed step patterns with probe-heavy filtering. Build on existing 12 diverse patterns rather than jumping architectures.
---

# Mutation Exploration Protocol for C2 Optimization

## Core Principle
The seed's 12 step patterns are diverse and well-structured. Don't discard them!
Systematically mutate heights, positions, and level combinations.

## Mutation Types
1. **Height Perturbation**: Change peak/valley heights by +/-0.05-0.2
   - Try: 1.40->1.50, 1.50->1.60, or reverse
   - Rationale: Optimize local height ratios

2. **Position Shift**: Move boundaries by +/-5%
   - Try: 0.25->0.27, 0.75->0.73
   - Rationale: Shift support region to optimize convolution shape

3. **Level Merging**: Combine adjacent levels
   - Try: merge 0.90+1.10 into 1.10
   - Rationale: Reduce complexity, smooth transitions

4. **Level Splitting**: Add new level between existing ones
   - Try: insert 1.25 between 1.20 and 1.30
   - Rationale: Add flexibility

5. **Asymmetry**: Make left/right different
   - Try: set left=1.30, right=1.50
   - Rationale: Exploit directional properties

## Execution Flow
1. Probe seed to establish baseline (~1.042)
2. Generate 3-5 mutations with MUTUAL EXCLUSIVITY
3. Probe ALL mutations (target 15-20 probes)
4. Evaluate top 2 by probe score
5. If best beats seed: refine. Else: generate more mutations.

## Key Rules
- Use probes for ALL but 1-2 variants
- Try variations of ALL 12 seed patterns
- Ensure f >= 0 everywhere
- Track best combined_score
- If stuck: try completely different mutation type
