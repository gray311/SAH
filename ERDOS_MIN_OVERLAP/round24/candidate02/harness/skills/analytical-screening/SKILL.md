---
name: analytical-screening
description: Use generate_ready_candidates for cheap integral-constrained initialization screening.
---

# Analytical Screening for Erdos Problem\n\n## Workflow\n\n1. CALL generate_ready_candidates(temperature=0.5)\n\ \n2. EXAMINE the 3 returned candidates:\n   - Each has precomputed integral and c5_bound\n   - Candidates\ \ are already sigmoid-scaled (h in [0,1])\n   - Candidates are integral-normalized (sum ~ 1)\n\n3.\ \ FILTER candidates:\n   - SKIP if integral != 1.0 (constraint violation)\n   - SKIP if c5_bound >=\ \ 0.375 (too bad for full eval)\n   - KEEP if c5_bound < 0.37\n\n4. CALL evaluate_solution on ALL\ \ kept candidates\n\n5. If no improvement, repeat with temperature=0.8\n\n## Why Analytical Screening\ \ Works\n\n- No training needed: c5_bound computed via FFT (analytical)\n- Integral check: exact,\ \ no approximation\n- Fast: generates all 3 in one tool call\n- Budget-efficient: 1 tool call, 2-3\ \ evals max\n\n## Expected Results\n\nWith this tool, you should find c5_bound < 0.37 candidates quickly,\n\ then spend only 2-3 evals to confirm improvements.
