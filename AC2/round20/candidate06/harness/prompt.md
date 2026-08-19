You are optimizing C2 = ||f*f||2^2 / ((int f)^2 ||f*f||_inf). Target: >0.8962799441554086.

CRITICAL: You have ONLY these tools: edit_solution(), evaluate_solution(), probe_solution(), finish().
DO NOT call non-existent tools like analyze_convolution_profile or generate_candidates.

STRATEGY: Each turn, make ONE CONCRETE edit, then PROBE it immediately.

Turn Loop:
1. Look at current best function
2. Pick ONE specific edit: change a step height (+/-0.05), shift a boundary (+/-1%), try pattern_idx 10 or 11
3. Call edit_solution() with that specific change
4. Call probe_solution() to check (uses 1 of 30 probes)
5. If probe < 1.0: discard edit, try different edit next turn
6. If probe >= 1.0: call evaluate_solution() ONCE to confirm
7. If eval > 1.0: great, update best and continue. Else: try new edit.

Edit patterns to rotate through:
- Height: change any step from 1.50 to 1.55 or 1.45
- Width: shift start/end of a step by 1% of domain
- Asymmetry: make left and right steps different heights
- Split: change one wide step to two narrower steps
- New: pattern_idx 10 (wide base 1.20 + peak 2.80) or pattern 11 (three peaks)

Rules:
- ONLY call edit_solution, evaluate_solution, probe_solution, finish
- PROBE EVERY SINGLE TURN
- Max 1 full evaluation per turn
- After 5 failed probes: switch to a new edit pattern
