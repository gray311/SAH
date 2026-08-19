# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
import tqdm


@dataclass
class Hyperparameters:
    num_intervals: int = 800
    learning_rate: float = 0.015
    num_steps: int = 250000
    penalty_strength: float = 1e6
    warmup_steps: int = 25000


class ErdosOptimizer:
    """
    Optimized optimizer for Erdos minimum overlap problem.
    Uses very aggressive 6-block construction.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        """
        The loss function includes the objective and a penalty for the constraint.
        """
        # Enforce h(x) in [0, 1] via sigmoid (hard constraint)
        h = jax.nn.sigmoid(latent_h_values)

        # Calculate the primary objective (max correlation)
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        scaled_correlation = correlation * self.dx
        objective_loss = jnp.max(scaled_correlation)

        # Calculate the penalty for the integral constraint
        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2

        # Combine the objective with the penalty
        total_loss = objective_loss + self.hypers.penalty_strength * constraint_loss
        return total_loss

    def _get_6block_initialization(self, key):
        """
        Generate initial guess using a very aggressive 6-block construction.
        Uses extremely high contrast between high and low regions.
        """
        N = self.hypers.num_intervals
        
        # Create a 6-block pattern
        block_pattern = jnp.zeros(N)
        
        # Divide into 6 blocks
        block_size = N // 6
        
        # Block heights - extremely high contrast
        heights = [4.0, -3.0, 4.0, -3.0, 4.0, -3.0]
        
        for i, height in enumerate(heights):
            start = i * block_size
            end = (i + 1) * block_size
            block_pattern = block_pattern.at[start:end].set(height)
        
        # Add some random noise
        noise = jax.random.normal(key, (N,)) * 0.1
        latent = block_pattern + noise
        
        # Adjust to get integral = 1
        current_integral = jnp.sum(jax.nn.sigmoid(latent)) * self.dx
        scale_factor = 1.0 / current_integral
        latent = latent * scale_factor
        
        return latent

    def _get_4block_initialization(self, key):
        """
        Generate initial guess using a 4-block construction.
        This is a known good heuristic for this problem.
        """
        N = self.hypers.num_intervals
        
        # Create a block pattern: high, low, high, low
        block_pattern = jnp.zeros(N)
        
        # Divide into 4 blocks
        block_size = N // 4
        
        # Block heights optimized for minimum overlap
        heights = [2.0, -1.0, 2.0, -1.0]
        
        for i, height in enumerate(heights):
            start = i * block_size
            end = (i + 1) * block_size
            block_pattern = block_pattern.at[start:end].set(height)
        
        # Add some random noise
        noise = jax.random.normal(key, (N,)) * 0.1
        latent = block_pattern + noise
        
        # Adjust to get integral = 1
        current_integral = jnp.sum(jax.nn.sigmoid(latent)) * self.dx
        scale_factor = 1.0 / current_integral
        latent = latent * scale_factor
        
        return latent

    def run_optimization(self):
        optimizer = optax.adam(self.hypers.learning_rate)

        key = jax.random.PRNGKey(42)
        
        # Try multiple initializations and pick the best
        latent_candidates = []
        
        # 6-block initialization with extreme contrast
        latent_6block = self._get_6block_initialization(key)
        latent_candidates.append(('6block', latent_6block))
        
        # 4-block initialization
        latent_4block = self._get_4block_initialization(key)
        latent_candidates.append(('4block', latent_4block))
        
        # Random initialization
        latent_random = jax.random.normal(key, (self.hypers.num_intervals,))
        latent_candidates.append(('random', latent_random))
        
        # Pick the best initial candidate based on a quick evaluation
        best_candidate = None
        best_loss = jnp.inf
        
        for name, latent in latent_candidates:
            loss = self._objective_fn(latent)
            if loss < best_loss:
                best_loss = loss
                best_candidate = latent
        
        latent_h_values = best_candidate
        
        opt_state = optimizer.init(latent_h_values)

        @jax.jit
        def train_step(latent_h_values, opt_state):
            loss, grads = jax.value_and_grad(self._objective_fn)(latent_h_values)
            updates, opt_state = optimizer.update(grads, opt_state)
            latent_h_values = optax.apply_updates(latent_h_values, updates)
            return latent_h_values, opt_state, loss

        print(f"Optimizing a step function with {self.hypers.num_intervals} intervals...")
        
        # Warmup phase with lower learning rate
        for step in tqdm.tqdm(range(self.hypers.warmup_steps), desc="Warmup"):
            latent_h_values, opt_state, loss = train_step(latent_h_values, opt_state)
        
        # Main optimization with higher learning rate
        for step in tqdm.tqdm(range(self.hypers.num_steps - self.hypers.warmup_steps), desc="Optimizing"):
            latent_h_values, opt_state, loss = train_step(latent_h_values, opt_state)

        # Final h is just the sigmoid of the latent values
        final_h = jax.nn.sigmoid(latent_h_values)

        # Re-calculate final objective loss without the penalty for the report
        j = 1.0 - final_h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(final_h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)

        print(f"Optimization complete. Final C5 upper bound: {c5_bound:.8f}")
        return np.array(final_h), float(c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()

    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
