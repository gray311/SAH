---
name: architectural-escape-strategy
description: Escape local optima by exploring fundamentally different step function architectures, not just parameter tweaks.
---

# Escaping Local Optima in Step Function Optimization

## The Problem
The seed program uses 5-6 level step patterns optimized within that class. Small parameter tweaks won't escape this local optimum.

## The Solution
Generate entirely NEW architectural classes:

1. **Narrow Central Peak**: Very narrow high peak (5-10% domain) with low wide base
2. **Multi-Peak Scattered**: 4-6 independent peaks scattered across domain
3. **Asymmetric Plateau**: Wide central plateau with different heights on left/right
4. **Corner-Focused**: High values concentrated at edges (0-0.2n and 0.8n-1.0n)
5. **Harmonic Peaks**: Peaks positioned at fractions that might align with Fourier modes

## Process
1. Call analyze_step_params to understand current structure
2. Call generate_step_architectures to create 3-5 new architectural classes
3. Probe each new architecture (3-5 height variations each)
4. Evaluate top 1-2 performers
5. If successful, use winning structure as new base; if not, try even more diverse architectures

## Key Insight
The C2 constant benefits from specific spectral properties. Different architectural classes activate different spectral modes. You need to explore orthogonal architectural spaces, not just tune within one.
