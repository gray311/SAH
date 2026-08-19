Erdos minimum overlap problem (C5): Find h: [0,2]->[0,1] minimizing max_k integral h(x)(1-h(x+k))dx.

CONSTRAINT: integral(h) = 1 exactly. h values in [0,1].

Current best: C5 <= 0.38092303510845016 (combined_score = 1.0).

GOAL: Find h achieving c5_bound < 0.38092303510845016 (combined_score > 1.0).

CRITICAL INSIGHT: The seed optimizer trains from initializations (patterns 5-14 in _get_best_initialization), but training is slow.
DO NOT waste evals on training when you can directly test pattern initializations.

STRATEGY:
1. FIRST, use test_pattern_direct to instantly evaluate these 5 patterns (each takes ~0.1s, no training):
   - Pattern Bipartite: h=4 on [0,a), h=-1 on [a,2), sigmoid to [0,1], normalize integral=1
   - Pattern Bipartite: h=4 on [0,a), h=-1 on [a,2-a), ... 
   - Pattern Tri-modal: 3 narrow Gaussian peaks at specified centers
   - Pattern Tri-modal: 3 narrow rectangular peaks
   - Pattern Tri-modal: 3 moderate Gaussian peaks
   - Pattern Symmetric-4 peaks: 4 narrow peaks at 0.15, 0.85, 1.15, 1.85

2. Use test_pattern_direct to construct and score each pattern (analytical c5 via FFT, instant)
3. Call evaluate_solution ONLY on the best 1-2 patterns (fast training from good start)
4. If no pattern < 0.37, then try hyperparameter variations of training

5. Budget: 20 evals. Use test_pattern_direct 5-10x to screen, then 2-4 full evals.

6. PATTERN FORMULAS (copy from seed code, normalized for integral=1):
   Bipartite(a): latent = [4 for x<a] + [-1 for x>=a] -> sigmoid -> normalize integral=1
   TriGauss(c1,c2,c3,sigma): 3 Gaussians centered at c1,c2,c3 with bandwidth sigma
   TriRect(c1,c2,c3,w): 3 rectangles of width w at c1,c2,c3
   Sym4(w): 4 peaks at 0.15,0.85,1.15,1.85 with width w

7. If stuck, restart with same patterns but different widths/centers.
