---
name: discovery-optimization
description: "Maximize C\u2082 by exploring novel step function patterns. Use design_pattern to generate\nstructurally different candidates, then probe and evaluate. Focus on architectural\ninnovation over parameter tweaking."
---

# C₂ Optimization: Pattern Innovation Strategy

## Core Principle
Current 13-pattern seed is likely a local optimum. Break free by designing NEW pattern
architectures, not tweaking old ones.

## Phase 1: Diagnose Current Limitations
Call analyze_current() once to understand what's missing from current patterns.

## Phase 2: Generate Novel Patterns
Call design_pattern to create 3-5 fundamentally different patterns with:
- Different number of levels (3-7 vs current 3-5)
- Extreme height contrasts (e.g., 2.0 vs 0.5 vs 1.8)
- Asymmetric distributions (left-skewed, right-skewed)
- Multi-modal shapes (bimodal peaks, valley between peaks)
- Different support regions (concentrated center, spread edges)

For each design:
1. Use probe_solution to get approximate C₂
2. Compare with current best
3. If probe > best, save pattern
4. Call evaluate_solution on top 1-2 probes

## Phase 3: Refine if Needed
If a new pattern class shows promise, do targeted fine-tuning with small edits.

## Pattern Design Guidelines
- Start with 4-6 levels for flexibility
- Use heights: 1.8-2.2 (peaks), 0.6-1.2 (transitions), 1.4-1.7 (mid-levels)
- Try asymmetric: left side heights ≠ right side heights
- Consider bimodal: two peaks with a valley between
- Test concentrated vs spread distributions

## Budget Discipline
- Generate 3-5 patterns per iteration
- Probe all, evaluate only top 1-2
- If no improvement after 3 iterations, try completely different approach
