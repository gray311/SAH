You are an expert mathematician optimizing a 29x29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

CRITICAL: Use ONLY ONE construction method per evaluation - correct Paley construction with quadratic residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.

STRATEGY: Multi-stage hill climbing WITHIN TIME BUDGET (max 250s, leave 100s margin):

PHASE 1 - Multiple Cooling Schedules (BREADTH):
  Run 3 COMPLETE searches with different cooling schedules:
  - Schedule A: T=8.0, cool_rate=0.995, 5000 iters
  - Schedule B: T=3.0, cool_rate=0.997, 15000 iters  
  - Schedule C: T=1.0, cool_rate=0.998, 20000 iters
  Keep BEST result across all 3 schedules.

PHASE 2 - Seed Diversity (DEPTH):
  For the BEST schedule from Phase 1, run with 3 DIFFERENT SEEDS:
  - Seed 1: 42
  - Seed 2: 12345
  - Seed 3: 9998877
  Keep overall BEST.

PHASE 3 - Targeted Escape (REFINEMENT):
  From Phase 2 best, run 2 targeted escapes:
  - Escape A: Flip 100 random positions, run 5000 iters with T=10.0, cool_rate=0.999
  - Escape B: Flip checkerboard pattern where (i+j)%4==0, run 5000 iters with T=5.0, cool_rate=0.997

TOTAL WORKFLOW: 3 schedules × 3 seeds + 2 escapes = 11 complete searches
Expected time: ~10-12 searches × 20s = 220-240 seconds (within 250s budget)

TOOLS:
- probe_solution: Test 2-3 cooling schedule variations BEFORE full evaluation. Use subsampling to rank schedules.
- edit_solution: Provide COMPLETE working code implementing exactly the workflow above.
- evaluate_solution: Call ONLY once with the single best probe-ranked variant.

CRITICAL SUCCESS FACTORS:
✓ Implement ONLY Paley construction (no random matrices, no perturbed variants)
✓ Use 3 cooling schedules with COMPLETE searches (don't truncate)
✓ Use 3 seeds per best schedule (not 4+ families)
✓ Run targeted escapes on the BEST result only
✓ Total time MUST be <250s (enforce in code with progress printing)
✓ Use numpy.linalg.det for ALL iterations (fast, reliable for search)
✓ Print progress every 5000 iterations so you can verify completion

START by implementing the 3-schedule, 3-seed workflow with 2 escape attempts. Call edit_solution with complete code.
