---
name: discovery-optimization
description: "Iteratively optimize a program's EVOLVE-BLOCK to maximize an automatic evaluator score, under a fixed evaluation budget. Use for construction, algorithm-speed, and heuristic discovery tasks scored by combined_score (higher is better) through the edit_solution / evaluate_solution / finish tools. Prefer probe-based exploration to rank variants cheaply."
---

# Discovery optimization

One tool call per turn: `edit_solution` to stage a full new EVOLVE-BLOCK, then

`evaluate_solution` to score it. `combined_score` is higher-is-better; the best

version is retained automatically, so you never lose progress.

**CRITICAL: Use analyze_init extensively!** The task evaluator is slow and

your budget is limited. Test 3-5 different construction strategies using

analyze_init first, then only do full evaluate_solution on your top 1-2.

Start by reading what the score rewards. Restate the objective (maximize or

minimize the underlying quantity), the hard constraints the evaluator checks

(validity is 0 when a constraint is violated or the program errors), and the

per-evaluation time limit. Identify the entry function the evaluator calls — its

name and signature are fixed and must survive every edit.

For this Erdős overlap minimization task: the seed uses gradient descent on a

sigmoid-activated representation. Consider trying:

- Different numbers of intervals (coarser may converge faster)
- Different initialization patterns (random, sinusoidal, piecewise)
- Different optimizer settings (learning rate, penalty strength)
- Explicit construction strategies (e.g., specific step function patterns)

Spend evaluations like a budget. Each edit must encode one concrete hypothesis,

not a guess: change the construction/algorithm, not cosmetics. After an

evaluation, treat the returned score, validity, and error text as the only

evidence — reason from them before the next edit.

**Use analyze_init to test variants cheaply!** Modify the program to include

probe-based testing, or use analyze_init with different code variants.

Prefer **targeted SEARCH/REPLACE diffs** over rewriting the whole region: locate

the few lines that carry your idea and replace exactly those, so working code is

preserved. Reserve a full-block rewrite for a genuine structural change. Keep the

fixed entry function's inputs and outputs identical — only the internal

implementation may change.

When `evaluations_left` is low, consolidate: make your remaining edits count on

the most promising line, then submit. When the budget is exhausted or you cannot

beat `best_so_far`, call `finish` with a one-line summary of the winning

approach and its score. Never fabricate a score — only a returned

`evaluate_solution` result counts.

When stuck, fundamentally change your approach: try explicit constructions instead

of gradient descent, or adjust the mathematical representation of h(x).
