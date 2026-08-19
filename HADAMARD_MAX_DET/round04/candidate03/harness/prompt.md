You are optimizing a 29×29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

## SINGLE-FOCUSED STRATEGY

Use ONLY the Paley construction with quadratic residues mod 29:
QR = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}

For H[i][j]: diff = (i-j) mod 29, H[i][j] = 1 if diff ∈ QR else -1

## SIMULATED ANNEALING SEARCH

From the Paley base matrix, run simulated annealing to improve the determinant:

- Start with ALL 29×29 entries randomly flipped (±50% chance each)
- Or start from the base Paley matrix
- Run EXACTLY 15,000 iterations with:
  * Initial temperature: T = 8.0
  * Cooling rate: cool_rate = 0.9975
  * At each step: randomly pick one cell (i,j), flip its sign, accept if det increases or with prob exp(Δdet/T)
- Use numpy.linalg.det for ALL determinant calculations (fast, ~0.001s per call)
- NEVER use Bareiss during search

## SEED STRATEGY

Use a SINGLE deterministic seed sequence: 42, 123, 456, 789, 1011, 1213, 1415, 1617, 1819, 2021
Run one search for each seed, keep the best result.

## TIME BUDGET

Total runtime MUST be under 200 seconds. 15,000 iterations × numpy.det (~0.001s) ≈ 15 seconds per seed.
With 10 seeds: ~150 seconds, leaving 150 seconds buffer.

## OUTPUT

Return ONLY the best matrix found (as a 29×29 array of ±1). Do not print intermediate results.
