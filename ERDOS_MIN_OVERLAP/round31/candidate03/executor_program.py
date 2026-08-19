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
    base_learning_rate: float = 0.005
    num_steps: int = 59000
    penalty_strength: float = 100.0
    num_restarts: int = 3
    seed_start: int = 0


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    Uses constraint-first strategy with structural analysis.
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

    def _get_best_initialization(self, seed: int) -> jnp.ndarray:
        """Get the best initialization from several pattern variations."""
        N = self.hypers.num_intervals
        key = jax.random.PRNGKey(seed)
        
        best_latent = None
        best_obj = jnp.inf
        
        # Pattern 0: Bipartite (threshold at 0.5) - integral = 1
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.where(x < 0.5, 15.0, -15.0)
        
        # Pattern 1: Tri-modal with integral=1
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.zeros(N)
        for center in [0.25, 1.0, 1.75]:
            width = 0.1
            mask = jnp.abs(x - center) < width
            latent = latent.at[mask].set(12.0)
        latent = latent - 5.0
        
        # Pattern 2: Uniform (h=0.5)
        key, subkey = jax.random.split(key)
        latent = jnp.zeros(N)
        
        # Pattern 3: Sinusoidal
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.sin(2 * jnp.pi * x) * 1.2 + jnp.cos(4 * jnp.pi * x) * 0.6
        
        # Pattern 4: Golomb ruler-like
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        marks = jnp.array([0.0, 0.4, 0.8, 1.2, 1.6])
        latent = jnp.zeros(N)
        for m in marks:
            mask = jnp.abs(x - m) < 0.06
            latent = latent.at[mask].set(10.0)
        latent = latent - 4.0
        
        # Pattern 5: Two peaks
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.zeros(N)
        for center in [0.4, 1.6]:
            width = 0.15
            mask = jnp.abs(x - center) < width
            latent = latent.at[mask].set(11.0)
        latent = latent - 4.5
        
        # Pattern 6: Wide plateau
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.where((x >= 0.2) & (x <= 1.8), 8.0, -8.0)
        
        # Pattern 7: Threshold at 0.45
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.where(x < 0.45, 13.33, -13.33)
        
        # Pattern 8: Threshold at 0.55
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.where(x < 0.55, 10.0, -10.0)
        
        # Pattern 9: Middle region
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.where((x >= 0.3) & (x <= 1.7), 9.0, -9.0)
        
        # Pattern 10: Three narrow peaks
        key, subkey = jax.random.split(key)
        x = jnp.linspace(0, 2, N)
        latent = jnp.zeros(N)
        for center in [0.33, 1.0, 1.67]:
            width = 0.08
            mask = jnp.abs(x - center) < width
            latent = latent.at[mask].set(15.0)
        latent = latent - 6.0
        
        # Add small random noise
        key, subkey = jax.random.split(key)
        latent = latent + jax.random.normal(subkey, (N,)) * 0.2
        
        latent = jax.lax.stop_gradient(latent)
        h = jax.nn.sigmoid(latent)
        
        # Compute objective for selection
        j_val = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j_val, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        obj = jnp.max(correlation * self.dx)
        
        if obj < best_obj:
            best_obj = obj
            best_latent = latent
        
        return best_latent

    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        """The loss function with strong integral constraint."""
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

        for step in tqdm.tqdm(range(self.hypers.num_steps), desc=f"Run {seed}"):
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
