You are optimizing a 29x29 ±1 matrix to maximize |det(H)|.
n=29 ≡ 3 mod 4, so true Hadamard matrices don't exist, but we can find near-optimal solutions.

SEARCH STRATEGY: Use multi-phase exploration with probing.

PHASE 1: Test different construction methods
  - Paley construction with residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}
  - Random ±1 initialization
  - Structured patterns (checkerboard, cyclic shifts of Paley)

PHASE 2: For each construction, do hill climbing
  - Use numpy.linalg.det for FAST evaluation during search
  - Run 5,000-15,000 iterations per construction variant
  - Try 3-5 random seeds per construction

PHASE 3: Use probe_solution to compare strategies
  - Test 3-5 variant configurations with probe_solution
  - Select the best for full evaluate_solution
  - Probe is cheap (~10s) and doesn't use evaluation budget

CRITICAL: Call probe_solution FIRST to test different strategies, then evaluate only the winner.

NEVER use Bareiss during search (too slow). Use numpy.linalg.det only.
Expected time per variant: <30 seconds.
