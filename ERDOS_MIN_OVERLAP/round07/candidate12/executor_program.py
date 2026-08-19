# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
import tqdm


@dataclass
class Hyperparameters:
    num_intervals: int = 100
    base_learning_rate: float = 0.1
    num_steps: int = 10000
    penalty_strength: float = 500.0
    num_restarts: int = 5
    seed_start: int = 0


class ErdosOptimizer:
    """
    Direct piecewise-constant construction for C5 bound optimization.
    Uses simple patterns with explicit index handling.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h: jnp.ndarray) -> jnp.ndarray:
        """Compute the C5 bound from h without penalty. Returns jnp array."""
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return c5_bound

    def _validate_constraints(self, h: jnp.ndarray) -> tuple:
        """Check if h satisfies constraints."""
        valid_range = (h >= 0.0).all() and (h <= 1.0).all()
        integral = jnp.sum(h) * self.dx
        valid_integral = jnp.abs(integral - 1.0) < 1e-3
        return valid_range, valid_integral, float(integral)

    def _project_to_valid(self, h: jnp.ndarray) -> jnp.ndarray:
        """Project h to [0,1] and normalize to integral=1."""
        # First clamp to [0,1]
        h_clipped = jnp.clip(h, 0.0, 1.0)
        # Then normalize to integral = 1
        current_integral = jnp.sum(h_clipped) * self.dx
        # Use where to avoid division by zero
        ifactor = jnp.where(current_integral > 1e-10, 1.0 / current_integral, 1.0)
        h_normalized = h_clipped * ifactor
        # Final clamp to ensure [0,1]
        return jnp.clip(h_normalized, 0.0, 1.0)

    def _construct_single_plateau(self, seed: int) -> jnp.ndarray:
        """Construct h = c on [a, b], 0 elsewhere, normalized."""
        N = self.hypers.num_intervals
        key = jax.random.PRNGKey(seed)
        
        key, subkey1 = jax.random.split(key)
        a = jax.random.uniform(subkey1, ()) * 0.4
        b = jax.random.uniform(subkey1, ()) * 0.5 + 0.3
        key, subkey2 = jax.random.split(key)
        c = jax.random.uniform(subkey2, ()) * 0.8 + 0.2
        
        start_idx = int(a * N)
        end_idx = int(b * N)
        h = jnp.zeros(N)
        h = h.at[start_idx:end_idx].set(c)
        
        total = jnp.sum(h)
        h = h / jnp.where(total > 1e-10, total, 1.0)
        # Final clamp
        return jnp.clip(h, 0.0, 1.0)

    def _construct_two_plateaus(self, seed: int) -> jnp.ndarray:
        """Construct two separate plateaus."""
        N = self.hypers.num_intervals
        key = jax.random.PRNGKey(seed)
        
        key, subkey1 = jax.random.split(key)
        a1 = jax.random.uniform(subkey1, ()) * 0.3
        b1 = jax.random.uniform(subkey1, ()) * 0.2 + 0.2
        key, subkey2 = jax.random.split(key)
        a2 = jax.random.uniform(subkey2, ()) * 0.3 + 0.5
        b2 = jax.random.uniform(subkey2, ()) * 0.2 + 0.4
        key, subkey3 = jax.random.split(key)
        c1 = jax.random.uniform(subkey3, ()) * 0.8 + 0.2
        c2 = jax.random.uniform(subkey3, ()) * 0.8 + 0.2
        
        start1, end1 = int(a1 * N), int(b1 * N)
        start2, end2 = int(a2 * N), int(b2 * N)
        h = jnp.zeros(N)
        h = h.at[start1:end1].set(c1)
        h = h.at[start2:end2].set(c2)
        
        total = jnp.sum(h)
        h = h / jnp.where(total > 1e-10, total, 1.0)
        return jnp.clip(h, 0.0, 1.0)

    def _construct_symmetric(self, seed: int) -> jnp.ndarray:
        """Construct symmetric: h = c on [0, a] and [2-a, 2]."""
        N = self.hypers.num_intervals
        key = jax.random.PRNGKey(seed)
        
        key, subkey = jax.random.split(key)
        a = jax.random.uniform(subkey, ()) * 0.4 + 0.2
        
        n_a = int(a * N)
        h = jnp.zeros(N)
        h = h.at[:n_a].set(1.0)
        h = h.at[N - n_a:].set(1.0)
        
        total = jnp.sum(h)
        h = h / jnp.where(total > 1e-10, total, 1.0)
        return jnp.clip(h, 0.0, 1.0)

    def _construct_uniform_block(self, seed: int) -> jnp.ndarray:
        """Uniform block of width 1: h = 1 on [0,1]."""
        N = self.hypers.num_intervals
        n_half = int(N / 2)
        h = jnp.zeros(N)
        h = h.at[:n_half].set(1.0)
        return h

    def _optimize_h_direct(self, initial_h: jnp.ndarray) -> tuple:
        """Optimize h values directly with projection."""
        N = self.hypers.num_intervals
        
        optimizer = optax.adam(self.hypers.base_learning_rate)
        opt_state = optimizer.init(initial_h)
        
        def loss_fn(h):
            h_valid = self._project_to_valid(h)
            c5_bound = self._compute_c5_bound(h_valid)
            return c5_bound
        
        @jax.jit
        def train_step(h_values, opt_state):
            loss = loss_fn(h_values)
            grads = jax.grad(loss_fn)(h_values)
            updates, opt_state = optimizer.update(grads, opt_state)
            h_values = optax.apply_updates(h_values, updates)
            return h_values, opt_state, loss
        
        best_h = initial_h.copy()
        best_loss = jnp.inf
        current_h = initial_h.copy()
        current_opt_state = opt_state
        
        for step in tqdm.tqdm(range(self.hypers.num_steps), desc="Optimizing h"):
            current_h, current_opt_state, loss = train_step(current_h, current_opt_state)
            current_h = self._project_to_valid(current_h)
            current_loss = self._compute_c5_bound(current_h)
            if current_loss < best_loss:
                best_loss = current_loss
                best_h = current_h.copy()
        
        return best_h, best_loss

    def _get_smart_initializations(self, seed: int) -> list:
        """Generate multiple structurally different initial h functions."""
        inits = []
        inits.append(self._construct_single_plateau(seed))
        inits.append(self._construct_two_plateaus(seed))
        inits.append(self._construct_symmetric(seed))
        inits.append(self._construct_uniform_block(seed))
        return inits

    def _optimize_single_run(self, seed: int) -> tuple:
        """Run optimization from multiple smart initializations."""
        initializations = self._get_smart_initializations(seed)
        
        best_h = None
        best_c5 = jnp.inf
        
        for i, init_h in enumerate(initializations):
            h, c5 = self._optimize_h_direct(init_h)
            if c5 < best_c5:
                best_c5 = c5
                best_h = h
        
        return float(best_c5), best_h

    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None

        print(f"Running {self.hypers.num_restarts} restarts with direct construction...")
        for restart in range(self.hypers.num_restarts):
            seed = self.hypers.seed_start + restart
            c5_bound, final_h = self._optimize_single_run(seed)
            
            if c5_bound < best_c5_bound:
                best_c5_bound = c5_bound
                best_h = final_h
            
            valid_range, valid_integral, integral_val = self._validate_constraints(best_h)
            print(f"Restart {seed}: c5_bound = {c5_bound:.8f}, integral = {integral_val:.8f}, valid_range={valid_range}")

        print(f"Optimization complete. Best C5 upper bound: {best_c5_bound:.8f}")
        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()

    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
