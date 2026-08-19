---
name: piecewise-h-generation
description: Generate complete h(x) vectors with diverse structures. Replace seed initialization entirely.
---

# Piecewise h(x) Generation Strategy
## Core Idea The seed's 12 initialization patterns all produce similar sigmoidal h(x). Break through by generating COMPLETE h(x) vectors with DIFFERENT structures.
## Workflow 1. Call create_piecewise_h to get 5 ready-to-use h(x) vectors 2. For each h(x), EDIT _get_best_initialization to return ONLY that h(x) 3. Call probe_solution to verify: integral ~ 1, c5_bound < 0.37 4. Evaluate top 2-3 candidates 5. Call analyze_structure on current best to guide next design
## Pattern Library - piecewise_constant_3: High-low-medium-high structure - golomb_5_marks: Optimal spacing for 5 marks - golomb_7_marks: More marks, different spacing - asymmetric_triangular: Asymmetric step function - multi_peak_3: Three peaks of different heights
## Success Criteria - c5_bound < 0.37 (score > 1.027) - integral(h) = 1.0 (within 5%)
