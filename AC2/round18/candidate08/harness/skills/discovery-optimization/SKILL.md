---
name: discovery-optimization
description: "Systematic parameter space exploration within step function architecture. Mutate heights, positions,\nand symmetry systematically. Add small Gaussian perturbations in Phase 2. Use probes to filter variants."
---

# C2 Maximizer: Systematic Step Function Parameter Tuning

## Core Principle
Step functions work (1.042 combined_score). Escaping the local optimum requires systematic
parameter exploration, not architecture jumps.

## Parameter Mutation Operators

### 1. Height Mutation
- Change step heights by +/- 0.05 to 0.15 (5-15% variation)
- Try: lower peaks reduce ||f*f||_inf while maintaining L2
- Try: higher peaks increase ||f*f||_inf but may hurt L2/inf ratio
- Test pattern_idx=1 (height 1.50) at 1.45, 1.55, 1.60, 1.35

### 2. Position Mutation
- Shift interval boundaries by +/- 2-5% of n_intervals
- Try: narrow the central peak (reduces ||f*f||_inf)
- Try: widen the support (increases integral, affects denominator)
- Test: move start from 0.25n to 0.23n, 0.27n, 0.20n

### 3. Asymmetry Introduction
- Make left and right sides different
- Try: left side height = base*0.9, right side = base*1.1
- Try: asymmetric peak widths (narrow left, wide right)

### 4. Multi-peak Patterns
- Create 2-3 distinct peaks with controlled spacing
- Pattern: low-high-low (like Gaussian) but with steps
- Pattern: high-low-high (two peaks, one valley)

## Execution Flow

Iteration 1-5 (Parameter Sensitivity):
1. Pick a base pattern (e.g., pattern_idx=2 with height 1.60)
2. Generate 3 height variants: 1.55, 1.60, 1.65
3. Probe all 3, evaluate best
4. Record which direction helped

Iteration 6-15 (Combined Mutations):
1. Take winning variant from previous phase
2. Apply one more mutation: position shift OR asymmetry
3. Generate 3 new variants
4. Probe all, evaluate top 2

Iteration 16-25 (Refinement):
1. If height mutation helped: try finer granularity (±0.02)
2. If position helped: try multi-scale (coarse outer, fine inner)
3. If stuck: try new base pattern with different structure

Iteration 26-30 (Hybrid):
1. Take best step function
2. Add small Gaussian: f = step + 0.03*exp(-((x-0.25n)^2)/(2*(0.1n)^2))
3. Probe variants, evaluate best

## Key Rules
- Systematic exploration beats random jumps
- Track mutation effects: height↑? position shift? asymmetry?
- Use 20-25 probes to explore 8-12 variants before full evaluations
- Evaluate max 1-2 candidates per iteration (save budget)
- If iteration 15+ with no improvement: try new base pattern with different structure
