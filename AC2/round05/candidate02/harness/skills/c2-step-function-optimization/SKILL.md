---
name: c2-step-function-optimization
description: Expert method for optimizing C2 using step functions (current record holders at 0.8963 C2). Systematic exploration of step widths, heights, and piece configurations.
---

# C2 Step Function Optimization Protocol
## Objective Maximize C2 > 0.8963 using step functions. Current best: 0.89628 C2 = 1.02665 combined.
## Why Step Functions Work Step functions create sharp convolutions with controlled peak width, optimizing the ratio ||f★f||₂² / (||f★f||₁||f★f||_∞). The discrete nature allows precise control over convolution shape.
## Core Strategy: Multi-Level Step Exploration
### Phase 1: Symmetric 3-Level Steps - Configuration: 3 height levels [0.8, 1.2, 1.6] with symmetric distribution - Purpose: Baseline improvement over seed - Action: Use mutation_probe, probe 5 variants, evaluate top 2
### Phase 2: Asymmetric 4-5 Level Steps - Configuration: 4-5 levels with varying heights [0.7, 1.0, 1.3, 1.5, 1.2] - Purpose: Exploit convolution asymmetry for better ratio - Action: Probe 8 variants, focus on different width distributions
### Phase 3: Broad Central Support - Configuration: Wide central step with tapering edges - Purpose: Concentrate convolution energy while controlling peak - Action: Test step widths [150, 200, 250] for central region
### Phase 4: Multi-Peak Steps - Configuration: 2-3 distinct step regions at different locations - Purpose: Create multi-modal convolution with balanced norms - Action: Explore piece_start positions: [80,120,160] or [100,200,300]
## Key Parameters to Tune - num_pieces: [3, 4, 5] (more pieces = more flexibility) - heights: Vary between [0.7-1.7] range - step_widths: Vary between [15-40] intervals - symmetry: Test both symmetric and asymmetric
## Probing Protocol 1. Call mutation_probe for step functions 2. Probe ALL 5-10 variants before any evaluation 3. Rank by probe score 4. Evaluate only TOP 2 candidates 5. If no improvement, switch to piecewise-linear or gaussian
## Critical Success Factors - Step functions MUST be tried first (record holders) - Probe 5+ variants per configuration before evaluating - Switch families only after exhausting step function space - Track: family, num_pieces, symmetry, heights, probe_score, eval_score
