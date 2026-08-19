---
name: step-fine-tuning
description: When the seed's 1.03431 score plateaus, use probe_solution to test incremental parameter changes in peak heights (1.6-2.0), interval widths (0.2-0.8 fractions), and step counts (2-6 levels). Build on existing improvements.
---

# Step-function fine-tuning guide

## Current Best: 1.03431 (seed multi-level steps)

## Parameter Tweaks to Test with PROBE SOLUTION

### Height Adjustments (HIGH IMPACT)
- Central peak: 1.62 → 1.70 → 1.78 → 1.85
- Symmetric dual peaks: test both equal (1.52, 1.52) and asymmetric (1.42, 1.62)
- Wing heights: 0.72 → 0.82 → 0.92 (softer decay)

### Width Adjustments (MEDIUM IMPACT)
- Central width: 0.40 → 0.45 → 0.50 → 0.55
- Left wing: 0.15 → 0.12 → 0.10 (more compact)
- Right wing: 0.15 → 0.12 → 0.10 (more compact)

### Multi-level Patterns (EXPLORATION)
- Add intermediate level: 3-level → 4-level function
- Pyramid shape: test 5-level pyramidal (0.5, 1.0, 1.5, 1.0, 0.5)
- Asymmetric pyramid: 0.6, 1.2, 1.8, 1.4, 0.7

## Workflow
1. Call extract_step_params to see current configuration
2. Choose ONE parameter class to tweak (heights OR widths OR levels)
3. Edit with targeted SEARCH/REPLACE
4. Call probe_solution immediately
5. If probe > 1.03431, evaluate; else try different tweak
6. Repeat until no probes > 1.03431, then finish
