# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 800
    base_learning_rate: float = 0.0003
    num_steps: int = 25000
    penalty_strength: float = 120.0
    num_restarts: int = 4
    seed_start: int = 0


class ErdosOptimizer:
    def __init__(self, hypers):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h):
        h = jnp.array(h)
        j_val = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j_val, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound)

    def _finalize_h(self, h):
        h_np = np.clip(np.array(h), 0.0, 1.0)
        if np.max(h_np) > 1.0:
            scale = 1.0 / np.max(h_np)
            h_np = h_np * scale
        h_np = np.clip(h_np, 0.0, 1.0)
        integral = np.sum(h_np) * self.dx
        if integral > 1e-10:
            h_np = h_np / integral
        return h_np

    def _optimize_h(self, h_init):
        N = self.hypers.num_intervals
        
        optimizer = optax.adam(self.hypers.base_learning_rate)
        opt_state = optimizer.init(h_init.astype(jnp.float64))

        @jax.jit
        def objective_fn(h_values):
            h_safe = jnp.clip(h_values, 0.0, 1.0)
            j_val = 1.0 - h_safe
            h_padded = jnp.pad(h_safe, (0, N))
            j_padded = jnp.pad(j_val, (0, N))
            corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
            correlation = jnp.fft.ifft(corr_fft).real
            scaled_correlation = correlation * self.dx
            objective_loss = jnp.max(scaled_correlation)
            
            integral_h = jnp.sum(h_safe) * self.dx
            constraint_loss = (integral_h - 1.0) ** 2
            return objective_loss + self.hypers.penalty_strength * constraint_loss

        @jax.jit
        def train_step(h_values, opt_state):
            loss, grads = jax.value_and_grad(objective_fn)(h_values)
            grad_norm = jnp.sqrt(jnp.sum(grads * grads))
            clipped_grads = jnp.where(grad_norm > 1.0, grads / grad_norm, grads)
            updates, opt_state = optimizer.update(clipped_grads, opt_state)
            h_values = optax.apply_updates(h_values, updates)
            return h_values, opt_state, loss

        current_h = jnp.array(h_init, dtype=jnp.float64)
        current_opt_state = opt_state
        best_loss = objective_fn(current_h)
        
        for step in range(self.hypers.num_steps):
            current_h, current_opt_state, loss = train_step(current_h, current_opt_state)
            if loss < best_loss:
                best_loss = loss
        
        final_h = self._finalize_h(current_h)
        return float(self._compute_c5_bound(final_h)), final_h

    def create_three_peak(self, centers, widths, heights):
        """Create a 3-peak function with specified parameters."""
        N = self.hypers.num_intervals
        x = np.linspace(0, 2, N)
        h = np.zeros(N)
        
        for c, w, ht in zip(centers, widths, heights):
            mask = (x >= c - w/2) & (x < c + w/2)
            h[mask] = ht
        
        # Normalize
        integral = np.sum(h) * self.dx
        if integral > 1e-10:
            h = h / integral
        
        h = np.clip(h, 0.0, 1.0)
        return h

    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None
        
        print("Testing diverse 3-peak constructions...")
        
        # Various 3-peak configurations
        configs = [
            ([0.2, 0.5, 0.8], [0.1, 0.1, 0.1], [0.5, 0.5, 0.5]),
            ([0.25, 0.5, 0.75], [0.1, 0.1, 0.1], [0.5, 0.5, 0.5]),
            ([0.22, 0.5, 0.78], [0.08, 0.1, 0.08], [0.75, 0.75, 0.75]),
            ([0.15, 0.5, 0.85], [0.1, 0.1, 0.1], [0.5, 0.5, 0.5]),
            ([0.3, 0.5, 0.7], [0.06, 0.1, 0.06], [1.0, 1.0, 1.0]),
            ([0.2, 0.5, 0.8], [0.12, 0.08, 0.12], [0.4, 1.0, 0.4]),
            ([0.25, 0.5, 0.75], [0.08, 0.1, 0.08], [0.8, 1.2, 0.8]),
        ]
        
        for centers, widths, heights in configs:
            h = self.create_three_peak(centers, widths, heights)
            
            # Optimize this h
            c5_opt, h_opt = self._optimize_h(h)
            print(f"  3peak {centers} {widths}: c5 = {c5_opt:.8f}")
            
            if c5_opt < best_c5_bound:
                best_c5_bound = c5_opt
                best_h = h_opt
        
        # Add some random perturbations to the best 3-peak
        print("\nPerturbing best 3-peak...")
        if best_h is not None:
            for restart in range(self.hypers.num_restarts):
                seed = self.hypers.seed_start + restart
                perturbation = np.random.normal(0, 0.02, best_h.shape)
                h_rand = best_h + perturbation
                h_rand = np.clip(h_rand, 0.0, 1.0)
                
                integral = np.sum(h_rand) * self.dx
                if integral > 1e-10:
                    h_rand = h_rand / integral
                
                c5_rand = self._compute_c5_bound(h_rand)
                c5_rand_opt, h_rand_opt = self._optimize_h(h_rand)
                print(f"  Perturbation {restart}: c5 = {c5_rand_opt:.8f}")
                
                if c5_rand_opt < best_c5_bound:
                    best_c5_bound = c5_rand_opt
                    best_h = h_rand_opt
        
        print(f"\nBest C5 bound: {best_c5_bound:.8f}")
        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h, c5 = optimizer.run_optimization()
    return final_h, c5, hypers.num_intervals
# EVOLVE-BLOCK-END
