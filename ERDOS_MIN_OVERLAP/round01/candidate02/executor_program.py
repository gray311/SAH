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
    learning_rate: float = 0.005
    num_steps: int = 30000
    penalty_strength: float = 300000.0


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    Uses multiple random restarts with different initialization patterns.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        h = jax.nn.sigmoid(latent_h_values)

        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        scaled_correlation = correlation * self.dx
        objective_loss = jnp.max(scaled_correlation)

        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2

        total_loss = objective_loss + self.hypers.penalty_strength * constraint_loss
        return total_loss

    def optimize_from_start(self, key, init_scale=1.0):
        optimizer = optax.adam(self.hypers.learning_rate)
        latent_h_values = jax.random.normal(key, (self.hypers.num_intervals,)) * init_scale
        opt_state = optimizer.init(latent_h_values)

        @jax.jit
        def train_step(latent_h_values, opt_state):
            loss, grads = jax.value_and_grad(self._objective_fn)(latent_h_values)
            updates, opt_state = optimizer.update(grads, opt_state)
            latent_h_values = optax.apply_updates(latent_h_values, updates)
            return latent_h_values, opt_state, loss

        for step in tqdm.tqdm(range(self.hypers.num_steps), desc="Optimizing", leave=False):
            latent_h_values, opt_state, loss = train_step(latent_h_values, opt_state)

        final_h = jax.nn.sigmoid(latent_h_values)

        j = 1.0 - final_h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(final_h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound), final_h

    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None
        
        # Try different initialization scales
        scales = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
        for scale in scales:
            for seed in range(5):
                key = jax.random.PRNGKey(int(seed + scale * 100))
                c5_bound, h = self.optimize_from_start(key, init_scale=scale)
                if c5_bound < best_c5_bound:
                    best_c5_bound = c5_bound
                    best_h = h

        print(f"Optimization complete. Final C5 upper bound: {best_c5_bound:.8f}")
        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()

    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
