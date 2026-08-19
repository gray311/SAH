Erdos minimum overlap: find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.
Constraint: integral(h) = 1 exactly. Target: combined_score > 1.0 (c5_bound < 0.380923).
Strategy: 1. CALL systematic_scan to explore candidate space with multi-peak patterns 2. systematic_scan returns 6 candidates with different peak configurations, all integral-normalized 3. Analyze c5_bound estimates - candidates with c5_bound < 0.36 are high-priority 4. CALL evaluate_solution on the 2 best candidates (lowest c5_bound) 5. If no improvement, CALL systematic_scan with temperature=0.7 for more diversity 6. Use probe_solution ONLY if you need to verify a candidate before full eval
Key: systematic_scan systematically varies peak positions to find configurations that minimize overlap.
