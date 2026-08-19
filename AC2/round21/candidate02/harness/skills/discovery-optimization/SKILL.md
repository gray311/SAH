---
name: discovery-optimization
description: "Architecture-driven step function optimization. Use synthesize_step_function to explore new function architectures beyond the seed's 12 patterns. Leverage probe budget to screen structural variants before full eval."
---

# Architecture-Driven C2 Optimization

## Core Principle

The seed has 12 hardcoded step patterns defined by fraction-based intervals. The harness parser
cannot extract these formulas. You must use synthesize_step_function to systematically explore
NEW ARCHITECTURES: different numbers of peaks, asymmetric patterns, varying widths, etc.

## Phase 1: Structural Diversity (iterations 1-12)

### Step 1: Template Synthesis
Call synthesize_step_function with these templates (choose 4-6):

Template A: "high-narrow-peak"
- Single tall narrow peak at center
- Width: 20% of domain, height: 2.0

Template B: "dual-peaks-symmetric"
- Two equal peaks separated by valley
- Each peak: 25% width, height: 1.8
- Valley: 30% of domain

Template C: "plateau-center"
- Flat plateau in center with lower shoulders
- Plateau: 40% width, height: 1.5
- Shoulders: 30% each side, height: 0.8

Template D: "asymmetric-triple"
- Three peaks with different heights and widths
- Left: 20% width, height: 1.3
- Center: 30% width, height: 2.2
- Right: 25% width, height: 1.6

Template E: "step-symmetric"
- Multi-level symmetric steps
- 4 levels: 0.6, 1.0, 1.4, 1.8 (outer to inner)
- Each level: 20% of domain

Template F: "gradient-perturbed"
- Take a base pattern and perturb intervals by ±0.05
- Perturb heights by ±0.15

### Step 2: Probe & Evaluate
- Call probe_solution on ALL 4-6 variants (6 probes)
- Rank by probe score
- Call evaluate_solution on TOP 1 only

## Phase 2: Gradient + Structure Hopping (iterations 13-22)

### Step 1: Structure Hopping
If stuck, try these structure hops:
- Split the tallest peak into two
- Merge adjacent peaks into one wider peak
- Add a new peak in the lowest valley
- Remove the smallest peak entirely

### Step 2: Template Variation
Call synthesize_step_function with modified templates:
- Change peak heights: multiply by 0.8, 1.0, 1.2
- Change peak widths: multiply by 0.7, 0.9, 1.1
- Change peak positions: shift by ±10% of domain

### Step 3: Probe & Evaluate
- Probe 3-4 variants
- Evaluate best

## Phase 3: Aggressive Restructuring (iterations 23-30)

### Step 1: New Architectures
Try completely new function families:
- Gaussian-like smooth steps (using softplus transformations)
- Piecewise linear functions
- Multi-modal distributions (3-5 peaks)

### Step 2: Final Push
- Keep best c2 but restructure from scratch
- Probe 2, evaluate best
- Submit if c2 > 0.8962799441554086

## Key Rules
- NEVER call analyze_step_parameters (it doesn't work on this code)
- ALWAYS use synthesize_step_function with structured templates
- Use probes aggressively: 5-8 probes before any full eval
- If iteration 12+ with no improvement: try "structure-hop" templates
