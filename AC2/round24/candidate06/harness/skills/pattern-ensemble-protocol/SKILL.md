---
name: pattern-ensemble-protocol
description: Pattern ensemble search - leverage the 12 seed patterns to generate diverse hybrid architectures. Focus on MIXING patterns rather than refining one pattern's parameters.
---

# Pattern Ensemble Protocol for C2 Maximization

## Core Principle
The seed provides 12 step patterns with diverse architectures (1-3 peaks, symmetric/asymmetric,
varying heights). The current best (pattern_idx ~4-10) may already be optimal for its class.
To escape, we must EXPLORE NEW ARCHITECTURES by hybridizing patterns.

## Phase 1: Pattern Survey + Hybrid Exploration (iterations 1-12)

Step 1: Catalog Available Patterns
- Call list_step_patterns to see all 12 patterns
- Note which are symmetric (0,1,2,3,5,7,9,10,11) vs asymmetric (4,6,8)
- Note peak counts: 1-peak (most), 2-peak (5,7,11), 3-peak (10)

Step 2: Generate DIVERSE Hybrids (NOT parameter tweaks!)

Create 4-6 candidates using these strategies:

Strategy A: Height Merge
- Take pattern_idx=4 (asymmetric: [1.10, 2.30, 1.40]) and pattern_idx=5 (symmetric: [1.50, 1.50])
- Merge: heights = [1.10, 1.50, 2.30, 1.40, 1.50] (alternating)
- Use pattern 4's ranges to test if asymmetric heights work on asymmetric structure

Strategy B: Range Swap (Height Independence Test)
- Take pattern_idx=10's heights [1.50, 2.50, 1.50] (3-peak) with pattern_idx=9's ranges [0.10-0.90, 0.35-0.65]
- This tests if 3-peak structure works with wider base

Strategy C: Asymmetry Injection
- Take symmetric pattern (e.g., idx=3: [0.90, 1.90, 0.90])
- Make asymmetric: [0.90, 2.10, 0.70] (raise right, lower left)

Strategy D: Multi-level Concat
- Take pattern 4's first 2 levels [1.10, 2.30] and pattern 6's last 2 levels [1.70, 1.00]
- Concatenate: [1.10, 2.30, 1.70, 1.00] (4-level pattern)

Step 3: Probe All Candidates
- Use all 30 probes to rank 4-6 hybrids
- Call evaluate_solution on top 2 only

Step 4: Select Winner
- If combined_score > 1.05: continue refining
- If < 1.02: try Strategy B or C

## Phase 2: Structural Refinement (iterations 13-20)

Step 1: Identify Structural Weakness
- If single-peak: try bi-modal (split peak into 2)
- If symmetric: try asymmetric variant
- If narrow: try wide-base (expand ranges to 0.10-0.90)

Step 2: Generate 3 Structural Variants
- Variant A: Flip symmetry
- Variant B: Split peak (1 to 2 peaks)
- Variant C: Expand base width by 30%

Step 3: Probe All, Evaluate Best

## Phase 3: Aggressive Rearchitecture (iterations 21-30)

Step 1: Combine Best Features
- Take top 2 hybrids from Phase 1
- Merge their height profiles
- Try 4-peak configuration

Step 2: Final Probe & Eval
- Probe 3-5 variants
- Evaluate best
- Submit if c2 > 0.8962799441554086

## Key Rules
- DIVERSIFY: Never generate only perturbations of the same pattern
- HYBRIDIZE: Primary mutation = combine 2 patterns
- PROBE-HEAVY: Use all 30 probes before wasting evals
- STRUCTURE OVER PARAMETERS: Change architecture, not heights by 0.1
