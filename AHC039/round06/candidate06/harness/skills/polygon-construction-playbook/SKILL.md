---
name: polygon-construction-playbook
description: Systematic approach to constructing candidate orthogonal polygons - enumerate rectangles, add cuts, merge regions. Use probe to filter before full evaluation.
---

# Systematic Polygon Construction Playbook

## Phase 1: Baseline Rectangle
Start with a simple rectangle. Best practices:
- Use analyze_input_ranges to find mackerel coordinate ranges
- Center rectangle on mackerel range, extend by margin (50-100 units)
- Try multiple sizes: small (100x100), medium (500x500), large (2000x2000)
- Try different positions relative to mackerel bounds

## Phase 2: Add Cuts
If baseline rectangle has too many sardines:
- Identify sardine clusters within the rectangle (use sardine ranges from analyze_input_ranges)
- Cut out sub-rectangles where sardines are dense
- Use probe to test each cut before full evaluation

## Phase 3: Multi-Region
If single region can't capture enough mackerels:
- Create multiple disconnected regions connected by thin corridors
- Focus on high-density mackerel patches
- Use probe to rank different region combinations

## Phase 4: Refinement
Once you have a working polygon:
- Try small boundary adjustments (±50-200 units)
- Add/remove single cuts
- Try merging nearby regions

## Budget Management
- Phase 1: 2-3 full evaluations
- Phase 2-3: Use probe for most candidates, evaluate only top 2-3
- Phase 4: 1-2 full evaluations if plateauing

## When to Change Strategy
- Score unchanged after 3 full evals: try a fundamentally different shape
- All rectangles score poorly: try multi-region approach
- Score is high but not optimal: fine-tune boundaries
- Time running out: submit best result, don't force exploration

## Key Insight
- The evaluator computes score on ALL 150 test cases - even if one fails, score is 0
- Your polygon must be VALID for all test cases (non-self-intersecting, integer coords)
- Focus on robust, simple shapes that generalize well
