You are an expert algorithm engineer solving the APPLE ARTIS machine hierarchy optimization problem.

TASK: Manage N=10 machine IDs across L=4 levels for T=500 turns, starting with K=1 apple.
Machine j^0 produces A_j apples/turn. Higher-level machines multiply counts of lower levels.
Score = round(10^5 * log2(final_apples)). Higher is better.

CRITICAL GAME MECHANICS:
- Each turn: Choose ONE action (strengthen a machine or do nothing)
- Then all machines cascade in order: Level 0 → 1 → 2 → 3
- Level 0: apples += A_j * B[0][j] * P[0][j]
- Level i>0: B[i-1][j] += B[i][j] * P[i][j] (multiplies count of level below)

THE STRATEGY SEARCH PROBLEM:
The seed program's simple greedy policy with 25-turn lookahead is suboptimal.
You must experiment with DIFFERENT POLICY REGIMES, not just better search within one regime.

TRY THESE POLICY VARIANTS IN YOUR SEARCH:
1. "Early L0 Builder": Invest heavily in level 0 for first 50-100 turns to build apple base, then switch to level 3
2. "Aggressive L3": Start investing in level 3 as soon as you can afford it (even with 200-500 apples)
3. "Balanced Cascade": Alternate between level 0 and level 3 each turn once affordable
4. "Threshold-based": Only invest in level 3 when apples >= 5000 (higher threshold than seed's 1000)
5. "Deep Horizon": Use 150-200 turn lookahead with multi-policy comparison

IMPLEMENTATION APPROACH (C++):
1. At each turn, generate 15-20 candidate actions
2. For EACH candidate, simulate 100-150 turns with DIFFERENT POLICIES
3. For each policy, track final apple count
4. Pick the candidate-action that, when simulated with its best policy variant, gives highest projection
5. Always output exactly 500 lines with "\\n" for newlines

POLICY IMPLEMENTATION DURING SIMULATION:
- Early game (apples < 500): 70% level 0 actions, 30% idle (save apples for L3)
- Mid game (500 <= apples < 5000): 40% level 0, 40% level 3, 20% idle
- Late game (apples >= 5000): 30% level 0, 60% level 3, 10% idle

NEVER exit early. Always run all 500 turns. Use long long for all apple counts.
Output exactly 500 lines. Always use "\\n" (double backslash) in C++ code.
