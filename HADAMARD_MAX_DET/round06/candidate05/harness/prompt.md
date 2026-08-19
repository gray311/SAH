You are optimizing a 29x29 ±1 matrix to maximize |det(H)|. n=29 ≡ 3 mod 4.

The seed uses Paley construction with quadratic residues {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}, but this likely converges to a suboptimal local optimum.

YOUR JOB: Explore multiple strategies to escape local optima:

1. Try MULTIPLE construction methods in parallel:
   - Paley construction (as in seed)
   - Random ±1 matrix as starting point
   - Perturbed Paley (flip random entries from Paley base)
   - Diagonal perturbations

2. Tune search parameters:
   - Try different initial temperatures (T=1.0, 2.0, 5.0, 10.0)
   - Try different cooling rates (0.992, 0.995, 0.997, 0.999)
   - Try different iteration counts per seed (10k, 25k, 50k, 100k)
   - Try different numbers of seeds (3, 5, 8, 12)

3. Use the probe_solution tool EXTENSIVELY:
   - Test 5-10 variants with probe (cheap, ~10s each)
   - Compare approximate scores
   - Pick the 1-2 best variants for full evaluate (expensive, ~350s each)
   - With 30 probe budget, you can test 30 variants before spending eval budget!

4. For each evaluation, implement code that:
   - Runs multiple construction methods
   - Uses numpy.linalg.det for ALL determinants during search (fast)
   - Stops within 300 seconds (leave buffer)
   - Returns the BEST matrix found across all methods

5. strategy: Use probe_solution to test parameter combinations, then evaluate only the best variant.

Expected approach: Run 3-5 probe evaluations testing different (construction_method, temperature, iterations, num_seeds) combinations. Pick the winner. Use remaining probes to fine-tune. Then evaluate the best variant.

Total time MUST be <300s per evaluate call.
