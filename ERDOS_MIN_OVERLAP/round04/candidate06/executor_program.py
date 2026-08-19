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
    base_learning_rate: float = 0.04
    num_steps: int = 17000
    penalty_strength: float = 650.0
    num_restarts: int = 5
    seed_start: int = 0


class ErdosOptimizer:
    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h: jnp.ndarray) -> float:
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound)

    def _get_best_initialization(self, seed: int) -> jnp.ndarray:
        N = self.hypers.num_intervals
        key = jax.random.PRNGKey(seed)
        
        best_latent = None
        best_obj = jnp.inf
        
        # Focus on patterns similar to what worked before but slightly refined
        patterns = [
            ('refined1', lambda x: jnp.where(x < 0.45, 3.28,
                    jnp.where(x < 1.06, -1.56, -2.85))),
            ('refined2', lambda x: jnp.where(x < 0.44, 3.38,
                    jnp.where(x < 1.08, -1.48, -2.88))),
            ('refined3', lambda x: jnp.where(x < 0.42, 3.52,
                    jnp.where(x < 1.1, -1.42, -2.92))),
            ('refined4', lambda x: jnp.where(x < 0.47, 3.18,
                    jnp.where(x < 1.05, -1.62, -2.82))),
            ('refined5', lambda x: jnp.where(x < 0.46, 3.22,
                    jnp.where(x < 1.07, -1.58, -2.86))),
            ('refined6', lambda x: jnp.where(x < 0.435, 3.45,
                    jnp.where(x < 1.065, -1.54, -2.89))),
            ('refined7', lambda x: jnp.where(x < 0.48, 3.15,
                    jnp.where(x < 1.06, -1.64, -2.80))),
            ('refined8', lambda x: jnp.where(x < 0.455, 3.32,
                    jnp.where(x < 1.075, -1.52, -2.87))),
            ('balanced_lesser', lambda x: jnp.where(x < 0.5, 2.95,
                    jnp.where(x < 1.0, -1.2, -2.6))),
        ]
        
        for _, pattern_fn in patterns:
            x = jnp.linspace(0, 2, N)
            key, subkey = jax.random.split(key)
            latent = pattern_fn(x) + jax.random.normal(subkey, (N,)) * 0.1
            
            h = jax.nn.sigmoid(latent)
            j_ = 1.0 - h
            h_padded = jnp.pad(h, (0, N))
            j_padded = jnp.pad(j_, (0, N))
            corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
            correlation = jnp.fft.ifft(corr_fft).real
            obj = jnp.max(correlation * self.dx)
            
            if obj < best_obj:
                best_obj = obj
                best_latent = latent
        
        return best_latent

    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        h = jax.nn.sigmoid(latent_h_values)
        j_ = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j_, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        scaled_correlation = correlation * self.dx
        objective_loss = jnp.max(scaled_correlation)
        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2
        total_loss = objective_loss + self.hypers.penalty_strength * constraint_loss
        return total_loss

    def _optimize_single_run(self, seed: int):
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
