Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

STRATEGY (DIVERSIFIED INITIALIZATION):

The current harness fails because it only produces STRUCTURED mutations based on correlation analysis.
This is a myopic approach that explores a narrow region around the seed.

NEW STRATEGY: FIRST, generate 5-10 DIVERSE, COMPLETE step functions from scratch using different known constructions.
Then pick the best and optimize it.

DIVERSE INITIALIZATIONS TO TRY (in order of priority):

1. BIPARTITE (single threshold): h(x) = 1 if x < 1, else 0
2. THREE-PEAK: h(x) = 1 for x in [0.25, 0.75] U [1.25, 1.75], else 0
3. FOUR-PEAK (square wave): h(x) = 1 for x in [0.2, 0.6] U [1.0, 1.4], else 0
4. GOLOMB-RULER: h(x) = 1 at discrete points {0.1, 0.3, 0.7, 1.1, 1.5, 1.9}, else 0
5. TRIANGULAR: h(x) = triangular pulse centered at 1.0 with width 1.0
6. TWO-PLATEAU: h(x) = 0.5 for x in [0.25, 0.75], else 0
7. FIVE-PEAK (finer): h(x) = 1 at {0.1, 0.4, 0.7, 1.0, 1.3, 1.6, 1.9}, else 0
8. SHIFTED-BIPARTITE: h(x) = 1 if x < 0.5, else 0
9. WIDE-PLATEAU: h(x) = 0.8 for x in [0.2, 1.0], else 0
10. MODULATED: h(x) = 0.5 + 0.3*sin(2*pi*x)

For EACH construction, compute c5_bound exactly and verify:
  - h(x) in [0,1] for all x
  - integral(h) = 1 exactly

Then OPTIMIZE the best initial construction using JAX-based gradient descent:
  - Use a small learning rate (0.001) for fine-tuning
  - Run 20000 steps maximum
  - Apply L2 regularization (strength 10.0) to prevent overfitting

KEY INSIGHT: The current harness wastes evals on structural mutations that don't change the fundamental shape.
We need to FIRST find GOOD BASE SHAPES, then OPTIMIZE them.

WORKFLOW:

1. GENERATE DIVERSE INITIALS:
   - Create 3-5 different step function constructions from scratch
   - Use ctx.probe_solution to quickly rank them (no full eval yet)
   - Keep top 2 candidates

2. VERIFY CONSTRAINTS:
   - For each candidate, verify integral(h)=1 and h in [0,1]
   - If constraints violated, the candidate is invalid

3. OPTIMIZE PROMISING CANDIDATES:
   - For the best 1-2 candidates, apply JAX optimization
   - Start with learning_rate=0.001, steps=20000
   - Use penalty_strength=15.0 for integral constraint

4. EVALUATE FINAL CANDIDATES:
   - Only call evaluate_solution if c5_bound < 0.380 (tight threshold)
   - If combined_score > 1.0, finish immediately

AVOID: Random hyperparameter tuning, structure_inspired_mutations without prior diverse initialization.

REWARD: Finding ANY construction with c5_bound < 0.38092303510845016.
