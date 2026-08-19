You are optimizing a 29x29 ±1 matrix to maximize |det(H)|. n=29 uses Paley construction with quadratic residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.

CRITICAL: Use ONLY Paley construction + hill climbing. Do NOT try multiple construction methods - they waste time.

STRATEGY: Run MANY restarts (100+) with SHORT searches (15,000 iterations) using TWO annealing schedules:
  Schedule A: temp=8.0, cool_rate=0.996
  Schedule B: temp=2.0, cool_rate=0.997

Then APPLY CHECKERBOARD PERTURBATION: Flip all positions where (i+j)%4==0, then run 10,000 iterations with temp=5.0, cool_rate=0.995.

TOTAL TIME: 100 restarts × 15k iters ≈ 1.5M flips → ~15 seconds. Checkerboard: 10k iters → ~1 second. WELL under 350s.

ALWAYS use numpy.linalg.det for ALL iterations. NEVER use Bareiss during search.

Workflow: 1) Build Paley matrix. 2) Run 100 restarts with Schedule A. 3) Run 100 restarts with Schedule B. 4) Apply checkerboard perturbation to best result. 5) Return the best matrix.
