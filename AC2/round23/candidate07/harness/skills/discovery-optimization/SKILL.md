---
name: discovery-optimization
description: "Step-function configuration generation for C2 maximization. Generate diverse architectures: multi-level steps, asymmetric patterns, multi-peak functions. Use probes to screen before full evaluation."
---

# C2 Maximizer: Step-Configuration Generation Protocol

## Core Principle

Step functions have rich ARCHITECTURAL VARIATIONS beyond small parameter tweaks. Generate COMPLETE new configurations with:
- Different numbers of levels (2-6)
- Varied peak heights (0.5-3.0)
- Different peak positions and widths
- Asymmetric patterns
- Multi-peak structures

## Phase 1: Broad Architecture Exploration (iterations 1-12)

Step 1: Generate Diverse Configurations

Create 5-8 step functions with VARYING structures:
- Pattern A (Single Peak): Height 1.2-2.5, position center, width 30-40%, base 0.6-1.0
- Pattern B (Dual Peaks): Two peaks at 0.25 and 0.75, heights 1.5-2.5 each, base 0.7-1.2
- Pattern C (Multi-Level): 3-4 levels with heights e.g. 0.8, 1.6, 2.0, 1.3
- Pattern D (Asymmetric): Wide base 60-70% with narrow high peak 15-20%

Step 2: Probe and Evaluate

- Call probe_solution on ALL 5-8 variants
- Rank by probe score
- Call evaluate_solution on TOP 1 only
- Continue generating new configs if no improvement

## Phase 2: Local Refinement (iterations 13-22)

Step 1: Perturb Best Configuration

Take best parameters from Phase 1:
- Vary peak heights by +/-0.1-0.2
- Shift peak positions by +/-5%
- Adjust widths by +/-3%

Step 2: Generate 3 Perturbations
- Variant 1: Increase heights, keep positions
- Variant 2: Decrease heights, widen peaks
- Variant 3: Asymmetric perturbation

Step 3: Probe and Evaluate
- Probe all 3, evaluate best

## Phase 3: Aggressive Diversification (iterations 23-30)

Step 1: Generate Novel Architectures
- 2-peak with very different heights (e.g. 1.0 and 2.8)
- 3-peak symmetric pattern
- Oscillating levels (high-low-high-low)
- Narrow spike on wide base

Step 2: Final Evaluation
- Probe 4-5 variants, evaluate best
- Submit if c2 > 0.8962799441554086

## Key Rule

GENERATE COMPLETE NEW CONFIGURATIONS every iteration. Do not try to extract parameters from existing code.
