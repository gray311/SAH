---
name: expansion-strategy-playbook
description: Expand seed polygon [[0,0],[200,0],[200,200],[0,200]] in all 4 directions. Use probe_poly_expansion to test sizes 100-500 units, keep top 4-8 by probe score. Full evaluate top 1-2, hill climb with edge shifts of ±20,±50,±100.
---

# Expansion Strategy Playbook for Polygon Optimization

## Why This Strategy?

The seed outputs a tiny 200x200 rectangle at origin. This captures limited fish.
We MUST expand it aggressively - up to 800-1200 units in each direction - to capture more mackerels.

## Step-by-Step Method

### Step 1: Analyze Seed Limitation

Seed polygon: [[0,0],[200,0],[200,200],[0,200]]
Area: 40,000 square units

This is too small. The evaluation budget (30 evals) and time budget (2s per eval)
let us explore multiple directions efficiently with probes.

### Step 2: Generate Expansion Candidates

For each cardinal direction (N, S, E, W):

- Create expansions: 100, 200, 300, 400, 500 units in that direction
- Example for North: [[0,0],[200,0],[200,700],[0,700]] (200+500=700 height)

Total candidates: 4 directions × 5 sizes = 20 candidates

### Step 3: Probe All Candidates

Use probe_poly_expansion to score each candidate:
- Call probe_solution for each
- Record (direction, size, score)

This uses the cheap probe budget (up to 30 per eval), not the expensive evaluation budget.

### Step 4: Select Top Candidates

Keep top 4-8 candidates by probe score.
These are your best bets for full evaluation.

### Step 5: Full Evaluate Top Candidates

For the top 1-2 candidates:
- Call evaluate_solution to get real score
- Record actual score

### Step 6: Hill Climb (Optional)

For the best candidate:
- Try shifting each edge by ±20, ±50, ±100 units
- Use probe_poly_expansion to check each shifted version
- Keep shifts that improve score

### Step 7: Multiple Restarts

Run 5-8 restarts with different strategies:
- Start expansion from different base sizes (200x200, 300x300, 400x400)
- Try bidirectional expansions (expand both N and S simultaneously)
- Try corner expansions (expand N+E, N+W, etc.)

### Step 8: Final Output

Output the polygon with best real score:
- First line: m (number of vertices, 4-1000)
- Next m lines: "x y" coordinates (integers, axis-aligned, no self-intersection)

## Key Success Factors

1. Probe 15-30 variants before full evaluation
2. Full evaluate only 1-2 best candidates
3. Use 5-8 restarts to explore diverse strategies
4. Ensure valid output: 4-1000 vertices, coords [0,100000], perimeter<=400000
