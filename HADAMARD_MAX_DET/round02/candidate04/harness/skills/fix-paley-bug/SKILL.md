---
name: fix-paley-bug
description: Critical skill - The seed's Paley construction is mathematically WRONG. Must use Legendre symbol approach. Quadratic residues mod 29 - 0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28. Use these for H[i][j] where offset equals (i-j) mod 29.
---

# FIX THE PALEY CONSTRUCTION BUG - CRITICAL!

The seed program's Paley construction is MATHEMATICALLY INCORRECT and must be fixed.

## The Bug
Seed code computes residues as {(i*i) % 29 for i in 1 to 28} which is WRONG.
For Paley construction with n=29 (prime, n congruent to 3 mod 4), we need the actual quadratic residues.

## The Fix
Quadratic residues mod 29 (numbers that are perfect squares mod 29):
{0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}

Verify: 1 squared equals 1, 2 squared equals 4, 3 squared equals 9, 4 squared equals 16, 5 squared equals 25, 
6 squared equals 36 which is 7 mod 29, 7 squared equals 49 which is 20 mod 29, 8 squared equals 64 which is 6 mod 29, 
9 squared equals 81 which is 24 mod 29, 10 squared equals 100 which is 13 mod 29, 11 squared equals 121 which is 5 mod 29, 
12 squared equals 144 which is 28 mod 29.

## Correct Construction
For each entry H[i][j]:
- Compute offset = (i - j) mod 29
- If offset is in {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}: H[i][j] = +1
- Otherwise: H[i][j] = -1

## Implementation
residues = {0, 1, 4, 5, 6, 7, 9, 13, 16, 20, 22, 23, 24, 25, 28}
def create_paley_correct(n):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            offset = (i - j) % n
            row.append(1 if offset in residues else -1)
        matrix.append(row)
    return matrix

## After fixing Paley
1. Run 15 to 20 hill climbing trials from correct Paley
2. Use 15000 to 18000 iterations per trial
3. Better annealing: T equals 3.0, cool_rate equals 0.9985
4. Use probe_solution to rank top trials before full eval
5. Expected: Much better scores than seed's buggy Paley
