---
name: discovery-optimization
description: "Explore multiple seed patterns in parallel with drastic structural changes, rank variants with probe_solution, and only evaluate the most promising ones. Avoid local refinement of saturated patterns."
---

# C₂ Maximizer: Parallel Pattern Exploration Protocol
## Overview
The seed's 13 step patterns are locally saturated. Tiny mutations won't help. Instead, systematically explore DRASTIC changes to EACH pattern before moving to new architectures.
## Phase 1: Parallel Exploration (Primary Strategy)
For EACH of the 13 seed patterns (indices 0-12), create ONE mutation with a DRASTIC structural change:
### Mutation Strategies (choose based on pattern type):
**For patterns 0-3 (simple multi-level):** - Merge two adjacent levels into one → creates a 2-level pattern - OR: Split the largest interval into two → creates more levels
**For patterns 4-7 (asymmetric multi-level):** - Reverse the entire pattern (swap start/end positions, reverse height order) - OR: Rotate heights (apply heights in cyclic order: h_n, h_0, h_1, ...)
**For patterns 8-12 (complex multi-level):** - Invert the shape: change all heights to (max_height - height + epsilon) - OR: Create a complementary pattern using (total_width - current_width) intervals
## Phase 2: Rapid Screening
1. After generating mutations for all 13 patterns, use probe_solution on ALL of them (30 probes available) 2. Rank by probe score 3. Evaluate only the TOP 2-3 variants with evaluate_solution
## Phase 3: Deep Dive (if Phase 2 succeeds)
If any variant improves: - Generate 2-3 MORE MUTATIONS of that same STRUCTURAL TYPE (not small tweaks) - Evaluate each with probe first, then evaluate the best
If no improvement after Phase 2: - Move to Phase 4: completely new pattern classes
## Phase 4: New Architectures (last resort)
Only explore after exhausting Phase 1-2 on all 13 seed patterns: - Double-peaked functions (two Gaussian-like bumps) - Triangular/Pyramid functions with optimized base and peak - Exponential decay with adjustable decay rate - Hybrid: step + smooth transition
## Key Rules
1. DON't refine a single pattern exhaustively — explore all 13 first 2. USE probe_solution to screen — don't spend evals on obvious failures 3. Make DRASTIC changes (structural), not tiny tweaks 4. Track which pattern indices produced improvements — they reveal architectural directions
