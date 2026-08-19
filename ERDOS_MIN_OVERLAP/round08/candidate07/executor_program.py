# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 200
    base_learning_rate: float = 0.025
    num_steps: int = 20000
    penalty_strength: float = 10000.0
    num_restarts: int = 5
    seed_start: int = 0


class ErdosOptimizer:
    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h: jnp.ndarray) -> float:
        j = 1.0 - h
        N = len(h)
        dx = self.domain_width / N
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        return float(jnp.max(correlation * dx))

    def _objective_fn(self, h: jnp.ndarray, dx: float) -> jnp.ndarray:
        j = 1.0 - h
        N = len(h)
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        scaled_correlation = correlation * dx
        objective_loss = jnp.max(scaled_correlation)
        integral_h = jnp.sum(h) * dx
        constraint_loss = (integral_h - 1.0) ** 2
        return objective_loss + self.hypers.penalty_strength * constraint_loss

    def _optimize_with_adam(self, h_init, dx):
        optimizer = optax.adam(self.hypers.base_learning_rate)
        opt_state = optimizer.init(h_init)

        @jax.jit
        def train_step(h_values, opt_state):
            loss, grads = jax.value_and_grad(lambda v: self._objective_fn(v, dx))(h_values)
            updates, opt_state = optimizer.update(grads, opt_state)
            h_values = optax.apply_updates(h_values, updates)
            return h_values, opt_state, loss

        current_h = h_init.copy()
        current_opt_state = opt_state
        
        for step in range(self.hypers.num_steps):
            current_h, current_opt_state, loss = train_step(current_h, current_opt_state)
            current_h = jnp.clip(current_h, 0.0, 1.0)
            integral = jnp.sum(current_h) * dx
            if integral > 0:
                current_h = current_h * (1.0 / integral)
        
        return current_h

    def _create_staircase(self, N, steps, positions, heights=None):
        """Create a staircase function with multiple steps."""
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        
        if heights is None:
            heights = [1.0] + [0.5] * (steps - 1) + [0.0]
        
        for i, pos in enumerate(positions[:steps-1]):
            end_pos = positions[i+1]
            h = h.at[(x >= pos) & (x < end_pos)].set(heights[i])
        
        integral = jnp.sum(h) * self.dx
        h = h / integral * self.hypers.num_intervals if integral > 0 else h
        
        return h

    def _optimize_coarse_to_fine(self):
        best_c5 = jnp.inf
        best_h = None
        
        print(f"Phase 1: Best 2-step configurations (N={self.hypers.num_intervals})...")
        
        # Focus on configurations that performed well
        configs = [
            ((0.15, 0.5), (1.0, 0.5)),
            ((0.16, 0.5), (1.0, 0.5)),
            ((0.18, 0.55), (1.0, 0.5)),
            ((0.18, 0.5), (1.0, 0.5)),
            ((0.20, 0.6), (1.0, 0.5)),
            ((0.15, 0.48), (1.0, 0.5)),
            ((0.16, 0.52), (1.0, 0.5)),
            ((0.18, 0.52), (1.0, 0.5)),
            ((0.15, 0.5), (1.0, 0.45)),
            ((0.16, 0.5), (1.0, 0.45)),
        ]
        
        for (left1, left2), (val1, val2) in configs:
            h_init = self._create_staircase(self.hypers.num_intervals, 2, [left1, left2], [val1, val2])
            h_opt = self._optimize_with_adam(h_init, self.dx)
            c5 = self._compute_c5_bound(h_opt)
            
            if c5 < best_c5:
                best_c5 = c5
                best_h = h_opt.copy()
                print(f"  2-step [{left1}, {left2}, v2={val2}]: c5 = {c5:.6f}")
        
        print(f"Phase 2: Best 3-step configurations...")
        
        # Focus on promising 3-step configs
        configs3 = [
            ((0.14, 0.45, 0.7), (1.0, 0.45, 0.3)),
            ((0.15, 0.45, 0.7), (1.0, 0.45, 0.3)),
            ((0.15, 0.48, 0.7), (1.0, 0.45, 0.3)),
            ((0.16, 0.45, 0.72), (1.0, 0.45, 0.3)),
            ((0.14, 0.45, 0.72), (1.0, 0.5, 0.3)),
            ((0.15, 0.45, 0.7), (1.0, 0.5, 0.3)),
        ]
        
        for (left1, left2, left3), (v1, v2, v3) in configs3:
            h_init = self._create_staircase(self.hypers.num_intervals, 3, [left1, left2, left3], [v1, v2, v3])
            h_opt = self._optimize_with_adam(h_init, self.dx)
            c5 = self._compute_c5_bound(h_opt)
            
            if c5 < best_c5:
                best_c5 = c5
                best_h = h_opt.copy()
                print(f"  3-step [{left1}, {v2}], [{left2}, {v3}], [{left3}]: c5 = {c5:.6f}")
        
        print(f"Final C5 bound: {best_c5:.8f}")
        return best_h, float(best_c5), self.hypers.num_intervals


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound, num_intervals = optimizer._optimize_coarse_to_fine()

    return final_h_values, c5_bound, num_intervals
# EVOLVE-BLOCK-END
