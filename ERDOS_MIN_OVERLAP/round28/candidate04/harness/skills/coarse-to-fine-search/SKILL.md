---
name: coarse-to-fine-search
description: Use search_grid for coarse-to-fine hyperparameter enumeration. Focus evaluation budget on best candidates.
---

# Coarse-to-Fine Search for Erdos Problem\n\n## Strategy\n\nThe key to finding better C5 bounds is systematic hyperparameter search with analytical pre-screening.\n\n## Workflow\n\n1. CALL search_grid(coarse=True) once at the start\n2. EXAMINE the 4-6 returned candidates: each has estimated_c5 from analytical computation\n3. FILTER: keep candidates with estimated_c5 < 0.382 (allow margin for full eval)\n4. CALL evaluate_solution on ALL kept candidates\n5. If no improvement after 3 evals, CALL search_grid(coarse=False) for finer search\n6. Repeat coarse-to-fine until budget exhausted or improvement found\n\n## Why Coarse-to-Fine Works\n\n- Coarse search explores diverse regions quickly (4-6 candidates)\n- Fine search refines promising regions (8-12 candidates)\n- Analytical pre-screening (search_grid) avoids wasting evals on bad candidates\n- Each eval is on a pre-trained candidate, not starting from scratch\n\n## Expected Outcome\n\nWith coarse-to-fine search, you should find c5_bound < 0.380923 within 5-7 full evaluations.
