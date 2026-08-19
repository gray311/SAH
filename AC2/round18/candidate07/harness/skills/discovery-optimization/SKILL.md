---
name: discovery-optimization
description: "Targeted step-pattern mutation. The seed already has diverse, high-quality step functions.\nGenerate targeted edits (width/height/asymmetry changes) to existing patterns, use probes\nto filter, then evaluate. Only after exhausting pattern variations, switch to new architectures."
---

# C₂ Optimizer: Targeted Pattern Mutation Protocol

## Understanding the Problem
The seed program contains 10+ well-designed step patterns in _create_step_initializer.
These patterns are diverse (different widths, heights, asymmetries). The harness previously
failed by trying to generate completely new function families (Gaussian, B-spline, etc.).

**KEY INSIGHT**: edit_solution performs SEARCH/REPLACE on the EVOLVE-BLOCK. It cannot
generate entirely new function architectures. To improve, you must EDIT existing patterns.

## Phase 1: Pattern Exploration (iterations 1-20)

Step 1: Analyze Current Patterns
- Call analyze_patterns ONCE to see all 10 patterns and their current c2 values
- Identify: Which pattern has best c2? Which patterns are similar? Where's room for improvement?

Step 2: Generate Targeted Variants
- Call generate_variants on the BEST pattern (or top 2 patterns)
- Generate 5-8 variants with SMALL edits:
  * Width shifts: ±2-5% on interval boundaries
  * Height adjustments: ±0.05-0.15 on plateau heights
  * Add/remove small plateaus at edges
  * Create asymmetric variants of symmetric patterns
  * Combine: take left side of pattern A, right side of pattern B
- IMPORTANT: Keep edits SMALL (≤10% structural change) to maintain mathematical properties

Step 3: Probe-Based Filtering
- Call probe_solution on ALL 5-8 variants (fast, ~10s each, separate from eval budget)
- Call evaluate_solution ONLY on variants with probe score > current best

Step 4: Iterate
- If a variant beats the record: continue refining it (small mutations)
- If NO variant beats record after trying 3 different seed patterns: go to Phase 2

## Phase 2: Architecture Rewrite (iterations 21-40)

Only if Pattern Exploration fails:
1. Call analyze_patterns on current best
2. Call generate_new_architectures to create 5 NEW diverse patterns from scratch
3. These should be COMPLETELY NEW step patterns (different number of levels, asymmetries)
4. Probe all, evaluate top 2
5. If still no improvement after 5 iterations: stop and report best found

## Mathematical Guidelines
- For step functions: C₂ depends on how L2 norm distributes relative to sup norm
- Widening support → increases L2 more than sup (good if sup dominates)
- Adding intermediate plateaus → can smooth the convolution profile
- Asymmetry → may create interference patterns that improve the ratio
- Keep f(x) ≥ 0 (use jax.nn.softplus or max(0, f))

## Key Rule
- NEVER try to replace step functions with entirely different families (edit_solution can't do it)
- ALWAYS start by editing EXISTING patterns with small, targeted changes
- Use probes to explore 5-8 variants before any full evaluation
- Only rewrite architectures after exhausting pattern variations
