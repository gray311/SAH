---
name: architecture-exploration-protocol
description: Systematic exploration of step function architectures using synthesize_step_function templates. Avoid parsing weak points.
---

# Architecture Exploration Protocol

## Core Principle

Use synthesize_step_function to generate valid step functions from templates. Never rely on parsing
the seed code (it cannot extract the mathematical formulas). Explore structural diversity systematically.

## Phase 1: Template Diversity (iterations 1-12)

### Step 1: Choose 4-6 Templates
Select from: "high-narrow-peak", "dual-peaks-symmetric", "plateau-center", "asymmetric-triple",
"step-symmetric", "gradient-perturbed".

### Step 2: Generate Variants
For each template:
- Call synthesize_step_function with template="high-narrow-peak"
- Call with template="dual-peaks-symmetric"
- Call with template="plateau-center"
- Call with template="asymmetric-triple"
- Call with template="step-symmetric"
- Call with template="gradient-perturbed"

### Step 3: Probe All
Call probe_solution on ALL 4-6 variants (6 probes total)
Rank by probe score
Call evaluate_solution on TOP 1 only

## Phase 2: Parameter Tuning (iterations 13-22)

### Step 1: Structure Hop
Take winning architecture from Phase 1:
- Split tallest peak into two
- Merge adjacent peaks
- Add peak in lowest valley
- Remove smallest peak

### Step 2: Generate Modified Templates
Call synthesize_step_function with modified parameters:
- height_scale: 0.8, 1.0, 1.2
- width_scale: 0.7, 0.9, 1.1
- position_offset: -0.15, 0.0, 0.15

### Step 3: Probe & Evaluate
Probe 3-4 variants, evaluate best

## Phase 3: Aggressive Restructuring (iterations 23-30)

### Step 1: New Architectures
Try: Gaussian-like smooth steps, piecewise linear, multi-modal (3-5 peaks)

### Step 2: Final Push
Keep best c2 but restructure from scratch
Probe 2, evaluate best
Submit if c2 > 0.8962799441554086

## Key Rules
- NEVER call analyze_step_parameters (doesn't work)
- ALWAYS use synthesize_step_function with templates
- Use probes aggressively: 6-8 probes before any full eval
- If iteration 12+ with no improvement: try structure-hop templates
