---
name: discovery-optimization
description: "Optimize C2 via STRUCTURAL pattern exploration. Call generate_pattern_variants to sample diverse step function architectures, rank via probe, evaluate top candidates."
---

# C2 Step Function Optimization - Structural Pattern Search
Goal: Beat 1.03492 by discovering NEW pattern classes, not tweaking existing ones.
## Phase 1: Pattern Generation
1. Call generate_pattern_variants to generate 50-100 diverse patterns. - Request variety: single_peak, multi_peak, plateau, staircase, asymmetric, pyramid - Vary interval counts: 300, 450, 600, 800 - Vary height ranges: try both high-peaks (1.5-2.5) and moderate-peaks (1.0-1.5)
2. Review the generated patterns. Note structural differences: - Number of level changes - Peak-to-base height ratio - Peak width (fraction of domain) - Symmetry/asymmetry
## Phase 2: Probing and Ranking
3. For the top 10 structurally different patterns: - Call probe_solution on each - Rank by probe score (higher is better) - This costs ~10 probes but saves evaluation budget
4. If probe scores are similar, still proceed to eval - small differences matter.
## Phase 3: Evaluation and Iteration
5. Evaluate the top 2-3 patterns from Phase 2. - Record the best full score - Note which pattern class won
6. If best score < 1.03492: - Regenerate patterns with MORE variety - Try different interval counts - Try completely different pattern families
7. If best score > 1.03492: - Run another generate_pattern_variants with the winning pattern as seed - Make focused mutations around the winner
## Pattern Classes to Explore
- Single Peak: One high plateau in the center - Multi-Peak: 2-4 peaks of varying heights - Plateau: Wide flat regions with transitions - Staircase: Monotonic increase/decrease with steps - Asymmetric: Different left/right asymmetries - Pyramid: Triangular-like with rising/falling edges - Winged: Central peak with side shoulders
## Key Principles
- STRUCTURE drives C2 more than exact heights - Budget: 30 evals - spend wisely. 10 probes + 3 evals is ideal per iteration - If 5 iterations with no improvement, try a COMPLETELY different approach - Diversity is key - do not get stuck in one pattern family
