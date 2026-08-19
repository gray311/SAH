---
name: discovery-optimization
description: "Pattern-focused optimization for Erdos C5. The seed code has 14 pattern initializations. Test them one at a time (num_restarts=1) with short training (20000 steps), use probe to screen, then full evaluate only promising candidates. Mutate working patterns to find better variants."
---

# Pattern-Focused Erdos Optimization

## Understanding the Seed Code

The seed optimizer has 14 patterns (Pattern 0-13 visible, Pattern 14 tri-modal). Each pattern creates a different initial h(x) distribution. The problem is training ALL patterns (num_restarts=3) when we should test THEM INDIVIDUALLY.

## Strategy: Single-Pattern Deep Dives

1. **SELECT ONE pattern type** (e.g., Golomb ruler with marks at [0.0, 0.4, 0.8, 1.2, 1.6])

2. **EDIT the EVOLVE-BLOCK** to:
   - Remove other pattern attempts
   - Use ONLY that one pattern
   - Set num_restarts=1 (do not waste on others)
   - Set num_steps=20000 (quick validation)
   - Keep num_intervals=800 for now

3. **USE probe_solution** to get approximate c5_bound (500 intervals, fast)

4. **Decision**:
   - If c5_bound >= 0.375: DISCARD, try different pattern/variation
   - If c5_bound < 0.375: CALL evaluate_solution for full score

5. **If promising (c5_bound < 0.37)**: Create variations!
   - Golomb: Try different mark spacings (0.35, 0.5, 0.6), different number of marks (4, 6)
   - Tri-modal: Move peaks (0.3, 0.9, 1.5), adjust widths (bw=0.08, 0.12)
   - Bipartite: Move threshold (0.4, 0.6, 0.7), try asymmetric heights

## Pattern Mutation System

### Golomb Ruler Patterns
Marks at evenly spaced points minimize autocorrelation. Base: [0.0, 0.4, 0.8, 1.2, 1.6]
Variations:
- Golomb-4: [0.0, 0.5, 1.0, 1.5]
- Golomb-wide: [0.0, 0.6, 1.2, 1.8]
- Golomb-tight: [0.1, 0.45, 0.8, 1.15, 1.5]

### Tri-Modal Patterns  
Three narrow peaks spread mass. Base peaks: [0.4, 1.0, 1.6]
Variations:
- Shift left: [0.3, 0.9, 1.5]
- Shift right: [0.5, 1.1, 1.7]
- Wider peaks: bw=0.18
- Narrower peaks: bw=0.04

### Bipartite Patterns
Simple threshold-based. Base: x < 0.5 -> high, x >= 0.5 -> low
Variations:
- Threshold at 0.4, 0.6, 0.7
- Asymmetric: high=4.0, low=-2.0 (different magnitudes)

## Workflow Summary

1. Start with seed (see what baseline it achieves)
2. If no improvement, extract ONE pattern type
3. Edit code to use ONLY that pattern (num_restarts=1, num_steps=20000)
4. Probe to screen
5. Evaluate only if promising
6. If successful, mutate that pattern to find better variants
7. Never train full 59000 steps without probe confirmation
