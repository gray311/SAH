Task: Find a 29×29 ±1 matrix maximizing |det(H)|. n=29≡3 (mod 4), so use Paley construction with quadratic residues: {0,1,4,5,6,7,9,13,16,20,22,23,24,25,28}.

Strategy: Don't try multiple construction methods. The seed's Paley construction is correct. DO THIS INSTEAD:

1. START with the seed's Paley base matrix (it's correct, don't reinvent it).
2. Run SIMULATED ANNEALING on this base with DIFFERENT COOLING SCHEDULES:
   - Schedule A: 50k iterations, temp=5.0, cool_rate=0.998
   - Schedule B: 50k iterations, temp=4.0, cool_rate=0.9975
   - Schedule C: 60k iterations, temp=3.0, cool_rate=0.9965
   - Schedule D: 40k iterations, temp=2.0, cool_rate=0.997
   - Schedule E: 50k iterations, temp=1.5, cool_rate=0.9985
3. Keep the BEST result across ALL 5 schedules.
4. Optionally do ONE targeted escape: flip a checkerboard pattern ((i+j)%4==0), then run 20k iterations with temp=10.0.
5. Use numpy.linalg.det for ALL iterations (FAST, ~0.001s per call). NEVER use Bareiss during search.
6. Use Bareiss ONLY for final verification of the best result.

Total expected time: ~150k-200k iterations × 0.001s ≈ 150-200 seconds. Well under 350s budget.

CRITICAL: Write COMPLETE, WORKING CODE that implements ONE base matrix + 5 cooling schedules. Don't add extra methods - depth over breadth.
