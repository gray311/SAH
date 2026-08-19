# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 800
    base_learning_rate: float = 0.004
    num_steps: int = 60000
    penalty_strength: float = 100.0
    num_restarts: int = 3
    seed_start: int = 0


class ErdosOptimizer:
    def __init__(self, hypers):
        self.hypers = hypers
        self.dx = 2.0 / self.hypers.num_intervals

    def _compute_c5_bound(self, h):
        j_val = 1.0 - h
        h_padded = jnp.pad(h, (0, self.hypers.num_intervals))
        j_padded = jnp.pad(j_val, (0, self.hypers.num_intervals))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        return float(jnp.max(correlation * self.dx))

    def _get_initialization(self, seed):
        N = self.hypers.num_intervals
        x = jnp.linspace(0, 2, N)
        key = jax.random.PRNGKey(seed)
        
        # Try multiple patterns and pick the best
        best_latent = None
        best_obj = jnp.inf
        
        # Pattern 1: Bipartite at t=1.0
        latent = jnp.zeros(N)
        latent = latent.at[(x < 1.0)].set(3.0)
        latent = latent.at[(x >= 1.0)].set(-3.0)
        
        # Pattern 2: Bipartite at t=0.5
        key, subkey = jax.random.split(key)
        latent = jnp.zeros(N)
        latent = latent.at[(x < 0.5)].set(3.0)
        latent = latent.at[(x >= 0.5)].set(-3.0)
        
        # Pattern 3: Two peaks
        key, subkey = jax.random.split(key)
        latent = jnp.zeros(N)
        latent = latent.at[(x >= 0.2) & (x < 0.4)].set(4.0)
        latent = latent.at[(x >= 1.6) & (x < 1.8)].set(4.0)
        latent = latent - 2.0
        
        # Pattern 4: Three peaks
        key, subkey = jax.random.split(key)
        latent = jnp.zeros(N)
        for center in [0.4, 1.0, 1.6]:
            mask = jnp.abs(x - center) < 0.1
            latent = latent.at[mask].set(4.0)
        latent = latent - 1.8
        
        # Pattern 5: Random normal
        key, subkey = jax.random.split(key)
        latent = jax.random.normal(subkey, (N,))
        
        # Evaluate each pattern
        patterns = [latent, latent, latent, latent, latent]
        for i, latent in enumerate(patterns):
            key, subkey = jax.random.split(key)
            latent = latent + jax.random.normal(subkey, (N,)) * 0.15
            
            h = jax.nn.sigmoid(latent)
            j_val = 1.0 - h
            h_padded = jnp.pad(h, (0, N))
            j_padded = jnp.pad(j_val, (0, N))
            corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
            correlation = jnp.fft.ifft(corr_fft).real
            obj = jnp.max(correlation * self.dx)
            
            if obj < best_obj:
                best_obj = obj
                best_latent = latent.copy()
        
        return best_latent

    def _objective_fn(self, latent_h_values):
        h = jax.nn.sigmoid(latent_h_values)
        j_val = 1.0 - h
        h_padded = jnp.pad(h, (0, self.hypers.num_intervals))
        j_padded = jnp.pad(j_val, (0, self.hypers.num_intervals))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        objective_loss = jnp.max(correlation * self.dx)

        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2

        return objective_loss + self.hypers.penalty_strength * constraint_loss

    def _optimize_single_run(self, seed):
        initial_latent = self._get_initialization(seed)
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
        return self._compute_c5_bound(final_h), final_h

    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None

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
