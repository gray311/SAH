---
name: fourier-architecture-explore
description: Playbook for exploring novel function architectures using Fourier analysis. Use fourier_space_probe to guide architecture choices.
---

# Fourier-Architecture Exploration Playbook

## Philosophy

Instead of only optimizing step functions, explore novel architectures:
- Mixtures of basis functions
- Multi-scale refinements  
- Fourier-space optimized functions

## Workflow

### Phase 1: Baseline Fourier Analysis

1. Call fourier_space_probe on seed program
2. Record: spectral_complexity, dominant_frequency, energy_distribution
3. This is your baseline for comparison

### Phase 2: Architecture Generation

Based on baseline, choose exploration direction:

#### If baseline shows single dominant freq:
- Try MULTI-MIXTURE: combine 2-3 basis functions with different frequencies
- Example: f(x) = w1*gaussian1 + w2*gaussian2 + w3*step

#### If baseline shows spread energy:
- Try CONCENTRATION: optimize to concentrate energy in desired bands
- Use Fourier-space optimization

#### If baseline shows oscillations:
- Try SMOOTHING: use splines or mollified functions
- Reduce high-frequency content

### Phase 3: Iterative Refinement

1. Edit to new architecture
2. Call fourier_space_probe to compare spectral properties
3. Did it improve? Look for:
   - More concentrated energy (if that's the pattern)
   - Better frequency matching
   - Reduced oscillations
4. Probe multiple variants (5-10 with probe_solution)
5. Evaluate top 2-3

### Phase 4: Architecture Evaluation

Track which architectures work:
- Mixture models: Do weighted combinations help?
- Multi-scale: Does coarse-to-fine refinement help?
- Fourier-optimized: Does frequency-domain optimization help?

## Architecture Templates

### Template 1: Gaussian Mixture
f(x) = sum(w_i * exp(-((x - mu_i)/sigma_i)^2))

### Template 2: Step Mixture
f(x) = sum(w_i * I(x in [a_i, b_i]))

### Template 3: Multi-Scale
Start coarse grid -> refine around peaks

### Template 4: Fourier-Optimized
Optimize Fourier coefficients with inverse FFT for positivity

## Checklist

- [ ] Called fourier_space_probe BEFORE major architecture change
- [ ] Compared spectral properties before/after
- [ ] Tried at least 2 different architectures
- [ ] Used probe_solution for ranking variants
- [ ] Only evaluated top 2-3 after probing
- [ ] Documented which architecture succeeded
