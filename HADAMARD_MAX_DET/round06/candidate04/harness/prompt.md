Optimize a 29×29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

The PALEY construction gives a good starting point: H[i][j] = 1 if (i-j) mod 29 in {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}, else -1.

However, the base Paley matrix may be stuck in a local optimum. You MUST try MULTIPLE strategies:

STRATEGY 1: Multiple SA restarts with DIFFERENT mutations:
  - Start from Paley base
  - Run SA with T=2.0, cool=0.996 for 50,000 iterations
  - At each step: flip ONE random element
  - Accept if det improves OR with probability exp(delta/T)
  - Try seeds: 1000,2000,3000,4000,5000 (5 different seeds)
  - Keep the BEST determinant across all seeds

STRATEGY 2: BLOCK-level search:
  - Start from Paley base
  - For 10,000 iterations:
    * With 70%: flip ONE random element (fine-grained)
    * With 30%: flip ALL elements in a random 2×2 block (coarse-grained)
  - T=1.5, cool=0.995
  - Keep best result

STRATEGY 3: RANDOM start with SA:
  - Generate random ±1 matrix (NOT from Paley)
  - Run SA: T=3.0, cool=0.997, 30,000 iterations
  - Try 2 random seeds

STRATEGY 4: PALEY + ROW/COLUMN PERTURBATION:
  - Start from Paley base
  - Swap 2 random rows (repeat 10 times, reverting each time)
  - Swap 2 random columns (repeat 10 times, reverting each time)
  - Run SA: T=1.0, cool=0.998, 20,000 iterations
  - 2 seeds

Implementation rules:
- Use numpy.linalg.det for ALL determinant calculations (fast, accurate)
- Total runtime MUST be < 180 seconds per evaluation
- Try 2-3 strategies per evaluation
- Return the matrix with highest determinant

Budget: 20 evaluations total. Each ~100-150 seconds.
Probe before evaluate: Use probe_solution to test 2-3 parameter variations, then evaluate the winner.
