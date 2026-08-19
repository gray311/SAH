---
name: discovery-optimization
description: "Structured pattern mutation for C\u2082 maximization. Use analyze_patterns to parse current patterns and generate mathematically-informed mutations. Focus on asymmetric structures, non-uniform spacing, and multi-scale features."
---

# C₂ Maximizer: Structured Pattern Mutation Protocol

## Core Principle

The seed's step patterns are LOCAL optima. To beat them, use SYSTEMATIC MUTATIONS based on mathematical insights, not random tweaks.

## Phase 1: Pattern Analysis (Iteration 1)

1. Call analyze_patterns ONCE to parse the EVOLVE-BLOCK and extract:
   - Number of intervals, pattern types present
   - Current heights, widths, positions
   - Symmetry properties, spacing regularity

2. Analyze output to identify mutation opportunities:
   - Are heights symmetric? (try asymmetric)
   - Is spacing uniform? (try non-uniform)
   - Missing multi-scale features? (add nested bumps)
   - Boundary handling optimal? (add tapering)

## Phase 2: Structured Mutation Generation

Generate mutations in this order of mathematical promise:

**Mutation Type A: Asymmetric Height Distribution**
- For symmetric patterns, create asymmetric heights
- Example: change [1.40, 1.40, 1.40] → [1.38, 1.42, 1.35]
- Rationale: Breaking symmetry can reduce ||f★f||_∞

**Mutation Type B: Non-Uniform Spacing**
- Replace uniform intervals with non-uniform spacing
- Example: 0.20n → 0.18n, 0.18n → 0.22n
- Rationale: Clustering features in certain regions can improve L2/∞ ratio

**Mutation Type C: Multi-Scale Features**
- Add nested bumps within existing features
- Example: base step + small bump on top of large bump
- Rationale: Captures finer structure in convolution

**Mutation Type D: Boundary Tapering**
- Add smooth decay at edges instead of sharp cutoffs
- Example: linear ramp from base_height to 0 over last 5%
- Rationale: Reduces Gibbs-like artifacts in convolution

**Mutation Type E: Edge Case Enhancement**
- Add small features near domain boundaries
- Rationale: May capture convolution contributions missed by central focus

## Phase 3: Probe-Based Selection

1. For each mutation type, generate 2-3 concrete implementations
2. Call probe_solution for ALL of them (use the 30-probe budget)
3. Rank by probe score, select top 3-5
4. Call evaluate_solution ONLY on top candidates

## Phase 4: Iteration and Diversification

If stuck after 10 iterations:
- Call analyze_patterns with different seed parameters
- Try completely different mutation order (A→E instead of E→A)
- Focus on mutation types that worked partially before

Key: Structured, mathematically-motivated mutations beat random changes.
