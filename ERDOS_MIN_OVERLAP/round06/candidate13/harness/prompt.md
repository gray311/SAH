You are an expert in harmonic analysis. Your task: find a step function h:[0,2]->[0,1] minimizing max_k ∫ h(x)(1-h(x+k))dx.

**GOAL**: Beat current best C5 bound of 0.38092303510845016. Current score: 0.999641 (SEED ONLY - you must improve!)

**WHY SEED FAILS**: The seed uses sigmoid+Adam on 800 intervals, producing SMOOTH functions. The optimal h is PIECEWISE CONSTANT with SHARP JUMPS.

**STRATEGY - COMPLETE OPTIMIZER REWRITE**:

Edit the EVOLVE-BLOCK to:
1. Use num_intervals=100 (coarse)
2. Replace sigmoid+Adam with direct construction of piecewise constant h using explicit breakpoints
3. Optimize OVER BREAKPOINT POSITIONS

**TEMPLATE**:
```python
class ErdosOptimizerNew:
    def __init__(self, N=100): self.N = N; self.dx = 2.0/self.N
    
    def construct_h(self, breakpoints):
        x = jnp.linspace(0, 2, self.N)
        h = jnp.zeros(self.N)
        for start, end, height in breakpoints:
            h = h.at[(x >= start) & (x < end)].set(height)
        integral = jnp.sum(h) * self.dx
        h = h * (1.0 / integral)
        h = h.clip(0, 1)
        return h
    
    def optimize(self, restarts=10):
        best_c5 = jnp.inf; best_h = None
        for _ in range(restarts):
            key = jax.random.PRNGKey(_)
            n = jax.random.randint(key, (1,), 3, 15)
            breaks = jnp.sort(jax.random.uniform(key, n))
            breaks = jnp.concatenate([jnp.array([0.05]), breaks, jnp.array([1.95])])
            h = self.construct_h([(b[i], b[i+1], 1.0) for i in range(len(breaks)-1)])
            c5 = self.compute_c5(h)
            if c5 < best_c5:
                best_c5, best_h = c5, h
        return best_h, best_c5
```

**USE TOOLS**: Call generate_candidates to see examples, then call edit_solution to REPLACE the EVOLVE-BLOCK entirely.
