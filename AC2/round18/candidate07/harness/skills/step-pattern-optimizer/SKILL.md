---
name: step-pattern-optimizer
description: Optimizes C₂ by editing existing step-function patterns with targeted, small changes. Use analyze_patterns to identify best pattern, generate_variants to create edits, probe to filter, then evaluate. Only switch to new architectures after exhausting pattern variations.
---

# Step Pattern Optimizer for C₂ Maximization

## Core Principle
The seed contains 10+ well-designed step patterns. Don't try to generate new function
families (edit_solution can't do that). Instead, make SMALL, targeted edits to existing
patterns and use probes to filter before full evaluation.

## Method: Pattern Editing Protocol

### Step 1: Analyze Patterns
- Call analyze_patterns ONCE to see all 10 patterns
- Identify: Which has best c2? What are their structures (width, height, levels)?
- Note patterns that are diverse (different properties) vs similar

### Step 2: Generate Targeted Variants
- Call generate_variants on the BEST pattern
- Generate 5-8 variants with SMALL edits:
  * Width shifts: ±2-5% on interval boundaries
  * Height adjustments: ±0.05-0.15
  * Add/remove edge plateaus
  * Create asymmetric variants
  * Combine patterns (left of A + right of B)
- CRITICAL: Keep edits ≤10% structural change

### Step 3: Probe and Evaluate
- Call probe_solution on ALL 5-8 variants (fast filtering)
- Call evaluate_solution ONLY on variants with probe score > current best
- If no improvement after trying 3 different seed patterns: go to Phase 2

### Step 4: Switch Architectures (Phase 2)
- Only if Phase 1 fails completely: call generate_new_architectures
- Create 5 NEW diverse step patterns from scratch
- Probe all, evaluate top 2
- If still no improvement after 5 iterations: report best found

## Mathematical Intuition
- C₂ = ||f★f||₂² / ((∫f)² ||f★f||_∞)
- Widening support: increases L2 faster than sup (good)
- Adding plateaus: smooths convolution, may improve L2/sup ratio
- Asymmetry: creates interference patterns that can boost the ratio
- Step functions are already optimal candidates; small improvements possible

## Key Rules
- NEVER try to replace step functions with Gaussian/B-spline/etc.
- ALWAYS edit EXISTING patterns with small, targeted changes first
- Use probes to explore 5-8 variants before any full evaluation
- Only rewrite architectures after exhausting pattern variations
