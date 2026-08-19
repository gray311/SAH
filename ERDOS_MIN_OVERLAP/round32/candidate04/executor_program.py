# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 800
    base_learning_rate: float = 0.003
    num_steps: int = 70000
    penalty_strength: float = 150.0
    num_restarts: int = 5
    seed_start: int = 0


class ErdosOptimizer:
    """
    Optimizer with fine-tuned step functions and more restarts.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h: jnp.ndarray) -> float:
        """Compute the C5 bound from h without penalty."""
        j_val = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j_val, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound)

    def _create_step_function(self, x, pattern):
        """Create a step function directly (values in [0,1])."""
        h = jnp.zeros(self.hypers.num_intervals)
        
        if pattern == "half":
            h = h.at[(x < 0.5)].set(1.0)
        elif pattern == "third":
            h = h.at[(x < 0.33)].set(1.0)
        elif pattern == "two_thirds":
            h = h.at[(x < 0.66)].set(1.0)
        elif pattern == "quarter_both":
            h = h.at[(x >= 0) & (x < 0.4)].set(1.0)
            h = h.at[(x >= 1.6) & (x < 2.0)].set(1.0)
        elif pattern == "uniform":
            h = jnp.ones(self.hypers.num_intervals) * 0.5
        elif pattern == "two_peaks":
            h = h.at[(x >= 0.2) & (x < 0.4)].set(1.0)
            h = h.at[(x >= 1.6) & (x < 1.8)].set(1.0)
        elif pattern == "three_peaks":
            h = h.at[(x >= 0.2) & (x < 0.35)].set(1.0)
            h = h.at[(x >= 0.85) & (x < 1.0)].set(1.0)
            h = h.at[(x >= 1.65) & (x < 1.8)].set(1.0)
        elif pattern == "four_peaks":
            h = h.at[(x >= 0.2) & (x < 0.28)].set(1.0)
            h = h.at[(x >= 0.62) & (x < 0.7)].set(1.0)
            h = h.at[(x >= 1.0) & (x < 1.08)].set(1.0)
            h = h.at[(x >= 1.4) & (x < 1.48)].set(1.0)
        elif pattern == "asymmetric_two":
            h = h.at[(x >= 0.15) & (x < 0.35)].set(1.0)
            h = h.at[(x >= 1.5) & (x < 1.85)].set(1.0)
        elif pattern == "asymmetric_three":
            h = h.at[(x >= 0.1) & (x < 0.25)].set(1.0)
            h = h.at[(x >= 0.7) & (x < 0.85)].set(1.0)
            h = h.at[(x >= 1.55) & (x < 1.75)].set(1.0)
        else:
            h = h.at[(x < 0.5)].set(1.0)
        
        # Normalize to get integral=1
        integral = jnp.sum(h) * self.dx
        if integral > 1e-10:
            h = h / integral
        
        return h

    def _latent_from_step(self, h):
        """Convert step function to latent (log-odds)."""
        h_safe = jnp.clip(h, 0.0001, 0.9999)
        return jnp.log(h_safe / (1.0 - h_safe))

    def _get_best_initialization(self, seed: int) -> jnp.ndarray:
        """Get initialization from diverse step function patterns."""
        N = self.hypers.num_intervals
        x = jnp.linspace(0, 2, N)
        
        patterns = [
            "half", "third", "two_thirds", "quarter_both", "uniform",
            "two_peaks", "three_peaks", "four_peaks",
            "asymmetric_two", "asymmetric_three"
        ]
        
        best_latent = None
        best_obj = jnp.inf
        
        for pattern in patterns:
            h = self._create_step_function(x, pattern)
            j_val = 1.0 - h
            h_padded = jnp.pad(h, (0, N))
            j_padded = jnp.pad(j_val, (0, N))
            corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
            correlation = jnp.fft.ifft(corr_fft).real
            obj = jnp.max(correlation * self.dx)
            
            if obj < best_obj:
                best_obj = obj
                best_latent = self._latent_from_step(h)
        
        return best_latent

    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        """The loss function."""
        h = jax.nn.sigmoid(latent_h_values)
        j_val = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j_val, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        scaled_correlation = correlation * self.dx
        objective_loss = jnp.max(scaled_correlation)

        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2

        total_loss = objective_loss + self.hypers.penalty_strength * constraint_loss
        return total_loss

    def _optimize_single_run(self, seed: int):
        """Run a single optimization with given seed."""
        initial_latent = self._get_best_initialization(seed)
        
        optimizer = optax.adam(self.hypers.base_learning_rate)
        opt_state = optimizer.init(initial_latent)

        @jax.jit
        def train_step(latent_h_values, opt_state):
            loss, grads = jax.value_and_grad(lambda v: self._objective_fn(v))(latent_h_values)
            updates, opt_state = optimizer.update(grads, opt_state)
            latent_h_values = optax.apply_updates(latent_h_values, updates)
            return latent_h_values, opt_state, loss

        best_latent = initial_latent.copy()
        current_latent = initial_latent
        current_opt_state = opt_state

        for step in range(self.hypers.num_steps):
            current_latent, current_opt_state, loss = train_step(current_latent, current_opt_state)
            
            if loss < self._objective_fn(best_latent):
                best_latent = current_latent.copy()

        final_h = jax.nn.sigmoid(best_latent)
        return float(self._compute_c5_bound(final_h)), final_h

    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None

        print(f"Running {self.hypers.num_restarts} restarts...")
        for restart in range(self.hypers.num_restarts):
            seed = self.hypers.seed_start + restart
            c5_bound, final_h = self._optimize_single_run(seed)
            
            if c5_bound < best_c5_bound:
                best_c5_bound = c5_bound
                best_h = final_h
            
            print(f"Restart {seed}: c5_bound = {c5_bound:.8f}")

        print(f"Optimization complete. Best C5 upper bound: {best_c5_bound:.8f}")
        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()

    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
