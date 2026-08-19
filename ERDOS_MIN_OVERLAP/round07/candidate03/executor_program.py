# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 5
    seed_start: int = 0


class ErdosOptimizer:
    """
    Constructive search for C5 bound minimization.
    Generate diverse piecewise constant functions and evaluate directly.
    No gradient descent - just test many constructions.
    """

    def __init__(self, hypers):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h):
        """Compute the C5 bound from h."""
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound)

    def _get_constructed_initializations(self, seed):
        """Generate diverse piecewise constant initializations."""
        N = self.hypers.num_intervals
        constructions = []
        
        # Pattern 1: Uniform distribution h(x) = 0.5 everywhere
        h_uniform = jnp.full(N, 0.5)
        constructions.append(("uniform", h_uniform))
        
        # Pattern 2: Single block h=1 on [0,1]
        h_single = jnp.zeros(N).at[0:N//2].set(1.0)
        constructions.append(("single_block", h_single))
        
        # Pattern 3: Two blocks [0, 0.5] and [1.5, 2]
        h_two = jnp.zeros(N)
        s1, e1 = int(0 * N / 2), int(0.5 * N / 2)
        h_two = h_two.at[s1:e1].set(1.0)
        s2, e2 = int(1.5 * N / 2), int(2 * N / 2)
        h_two = h_two.at[s2:e2].set(1.0)
        constructions.append(("two_blocks", h_two))
        
        # Pattern 4: Centered mass on [0.5, 1.5]
        h_center = jnp.zeros(N)
        s, e = int(0.5 * N / 2), int(1.5 * N / 2)
        h_center = h_center.at[s:e].set(1.0)
        constructions.append(("centered", h_center))
        
        # Pattern 5: Left-heavy [0, 1]
        h_left = jnp.zeros(N).at[0:N//2].set(1.0)
        constructions.append(("left_heavy", h_left))
        
        # Pattern 6: Right-heavy [1, 2]
        h_right = jnp.zeros(N).at[N//2:N].set(1.0)
        constructions.append(("right_heavy", h_right))
        
        # Pattern 7: Three equal blocks
        width = N // 3
        h_three = jnp.zeros(N)
        h_three = h_three.at[0:width].set(1.0).at[width*2:width*2+width].set(1.0)
        constructions.append(("three_blocks", h_three))
        
        # Pattern 8: Trapezoidal - high in middle
        x = jnp.linspace(0, 2, N)
        h_trap = jnp.where((x >= 0.25) & (x <= 1.75), 1.0, 0.0)
        constructions.append(("trapezoid", h_trap))
        
        # Pattern 9: Two-level - high on left, low on right
        h_twostep = jnp.zeros(N)
        h_twostep = h_twostep.at[0:int(N//3)].set(2.0).at[int(2*N//3):].set(0.5)
        constructions.append(("twostep", h_twostep))
        
        # Pattern 10: Inverse trapezoid - low in middle
        h_invtrap = jnp.where((x >= 0.25) & (x <= 1.75), 0.5, 2.0)
        constructions.append(("inv_trapezoid", h_invtrap))
        
        # Pattern 11: Concentrated at center
        h_spike = jnp.zeros(N)
        h_spike = h_spike.at[N//2-1:N//2+2].set(4.0)
        constructions.append(("spike", h_spike))
        
        # Pattern 12: Concentrated at edges
        h_edges = jnp.zeros(N)
        h_edges = h_edges.at[0:2].set(4.0).at[N-2:N].set(4.0)
        constructions.append(("edges", h_edges))
        
        return constructions

    def run(self, seed):
        """Run constructive search with given seed."""
        constructions = self._get_constructed_initializations(seed)
        
        best_c5_bound = jnp.inf
        best_h = None
        
        for name, h_init in constructions:
            # Project to [0,1] and normalize to ensure integral = 1
            h = jnp.clip(h_init, 0.0, 1.0)
            integral = jnp.sum(h) * self.dx
            if integral > 0:
                h = h / integral
            
            c5_bound = self._compute_c5_bound(h)
            
            if c5_bound < best_c5_bound:
                best_c5_bound = c5_bound
                best_h = h
        
        return float(best_c5_bound), best_h

    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None

        print(f"Running constructive search...")
        for restart in range(self.hypers.seed_start, self.hypers.seed_start + 30):
            c5_bound, final_h = self.run(restart)
            
            if c5_bound < best_c5_bound:
                best_c5_bound = c5_bound
                best_h = final_h
            
            print(f"Seed {restart}: c5_bound = {c5_bound:.8f}")

        print(f"Optimization complete. Best C5 upper bound: {best_c5_bound:.8f}")
        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()

    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
