# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
import tqdm


@dataclass
class Hyperparameters:
    num_intervals: int = 200
    base_learning_rate: float = 0.005
    num_steps: int = 30000
    penalty_strength: float = 10000.0
    num_restarts: int = 20
    seed_start: int = 0


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    Uses piecewise constant construction with multi-restart strategy.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h: jnp.ndarray) -> float:
        """Compute the C5 bound from h without penalty."""
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound)

    def _get_piecewise_constant_init(self, key, pattern_idx):
        """Generate piecewise constant initialization patterns - CLIPPED to [0,1]."""
        N = self.hypers.num_intervals
        
        # Pattern 0: Single block in middle
        x = jnp.linspace(0, 2, self.hypers.num_intervals)
        h = jnp.zeros(N).clip(0.0, 1.0)
        if pattern_idx == 0:
            # Single step: h=1 on [0.5, 1.5] (integral=1)
            h = h.at[(x >= 0.5) & (x < 1.5)].set(1.0)
        elif pattern_idx == 1:
            # Double step: h=0.5 on two blocks
            h = h.at[(x >= 0.0) & (x < 1.0)].set(0.5)
            h = h.at[(x >= 1.0) & (x <= 2.0)].set(0.5)
        elif pattern_idx == 2:
            # Asymmetric: h=1 on [0, 1], h=0 on [1, 2]
            h = h.at[(x >= 0.0) & (x < 1.0)].set(1.0)
        elif pattern_idx == 3:
            # High-low-high
            h = h.at[(x >= 0.0) & (x < 0.5)].set(1.0)
            h = h.at[(x >= 0.5) & (x < 1.5)].set(0.0)
            h = h.at[(x >= 1.5) & (x < 2.0)].set(1.0)
        elif pattern_idx == 4:
            # Three blocks
            h = h.at[(x >= 0.0) & (x < 0.5)].set(1.0)
            h = h.at[(x >= 1.0) & (x < 1.5)].set(1.0)
        elif pattern_idx == 5:
            # Shifted single block
            h = h.at[(x >= 0.3) & (x < 1.3)].set(1.0)
        elif pattern_idx == 6:
            # W-shaped
            h = h.at[(x >= 0.0) & (x < 0.4)].set(1.0)
            h = h.at[(x >= 0.4) & (x < 1.6)].set(0.5)
            h = h.at[(x >= 1.6) & (x < 2.0)].set(1.0)
        elif pattern_idx == 7:
            # U-shaped with gap in middle
            h = h.at[(x >= 0.0) & (x < 0.6)].set(1.0)
            h = h.at[(x >= 0.6) & (x < 1.4)].set(0.0)
            h = h.at[(x >= 1.4) & (x < 2.0)].set(1.0)
        elif pattern_idx == 8:
            # Narrow middle block
            h = h.at[(x >= 0.4) & (x < 1.6)].set(1.0)
        
        # Normalize to integral = 1
        integral = jnp.sum(h) * self.dx
        if integral > 0:
            h = h / integral
            # Re-clip after normalization
            h = h.clip(0.0, 1.0)
        
        return h

    def _objective_fn(self, h_values: jnp.ndarray) -> jnp.ndarray:
        """The loss function with strong bounds enforcement."""
        # Clip to [0,1]
        h_clipped = h_values.clip(0.0, 1.0)
        
        integral_h = jnp.sum(h_clipped) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2
        
        # Compute C5 bound
        h = h_clipped
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        scaled_correlation = correlation * self.dx
        objective_loss = jnp.max(scaled_correlation)

        total_loss = objective_loss + self.hypers.penalty_strength * constraint_loss
        return total_loss

    def _optimize_from_init(self, h_init):
        """Optimize starting from an initial piecewise constant function."""
        key = jax.random.PRNGKey(0)
        
        optimizer = optax.adam(self.hypers.base_learning_rate)
        
        @jax.jit
        def train_step(h, opt_state):
            loss, grads = jax.value_and_grad(lambda x: self._objective_fn(x))(h)
            updates, opt_state = optimizer.update(grads, opt_state)
            h = optax.apply_updates(h, updates)
            # Project to [0,1] after each step
            h = h.clip(0.0, 1.0)
            return h, opt_state, loss

        h = h_init.copy()
        opt_state = optimizer.init(h)
        
        for step in tqdm.tqdm(range(self.hypers.num_steps), desc="Optimizing", leave=False):
            h, opt_state, loss = train_step(h, opt_state)
        
        final_h = h
        return final_h

    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None

        print(f"Running {self.hypers.num_restarts} restarts...")
        
        for restart in range(self.hypers.num_restarts):
            key = jax.random.PRNGKey(restart)
            h_init = self._get_piecewise_constant_init(key, restart % 9)
            
            # Normalize to ensure integral = 1
            integral = jnp.sum(h_init) * self.dx
            h_init = h_init / integral
            h_init = h_init.clip(0.0, 1.0)
            
            h_final = self._optimize_from_init(h_init)
            c5_bound = self._compute_c5_bound(h_final)
            
            print(f"Restart {restart}: c5_bound = {c5_bound:.8f}, integral = {jnp.sum(h_final)*self.dx:.6f}, range = [{jnp.min(h_final):.3f}, {jnp.max(h_final):.3f}]")
            
            if c5_bound < best_c5_bound:
                best_c5_bound = c5_bound
                best_h = h_final
        
        print(f"Optimization complete. Best C5 upper bound: {best_c5_bound:.8f}")
        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()
    
    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
