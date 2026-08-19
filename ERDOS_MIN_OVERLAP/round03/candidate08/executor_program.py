# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
import tqdm


@dataclass
class Hyperparameters:
    num_intervals: int = 800
    base_learning_rate: float = 0.0053
    num_steps: int = 59000
    penalty_strength: float = 1370.0
    num_restarts: int = 6
    seed_start: int = 0


class ErdosOptimizer:
    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.num_intervals = hypers.num_intervals
        self.dx = jnp.array(2.0, dtype=jnp.float64) / hypers.num_intervals
        
    def _compute_c5_loss(self, h: jnp.ndarray) -> jnp.ndarray:
        """Compute C5 loss component (returns jnp array for JIT compatibility)."""
        h = jnp.asarray(h, dtype=jnp.float64)
        if h.ndim != 1:
            h = jnp.reshape(h, (-1,))
        if len(h) == 0:
            return jnp.array(1.0, dtype=jnp.float64)
        j_arr = jnp.ones_like(h, dtype=jnp.float64) - h
        N = self.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j_arr, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5 = jnp.max(correlation * self.dx)
        return c5
    
    def _compute_loss(self, latent: jnp.ndarray) -> jnp.ndarray:
        h = jax.nn.sigmoid(latent)
        c5 = self._compute_c5_loss(h)
        integral = jnp.sum(h) * self.dx
        constraint_loss = (integral - 1.0) ** 2
        loss = c5 + self.hypers.penalty_strength * constraint_loss
        return loss
    
    def _compute_c5_final(self, h: jnp.ndarray) -> float:
        """Compute final C5 bound (called outside JIT)."""
        return float(self._compute_c5_loss(jnp.asarray(h, dtype=jnp.float64)))
    
    def _optimize_single_run(self, initial_latent: jnp.ndarray, seed: int) -> Tuple[float, jnp.ndarray]:
        optimizer = optax.adam(self.hypers.base_learning_rate)
        opt_state = optimizer.init(initial_latent)
        
        @jax.jit
        def train_step(latent, opt_state):
            loss, grads = jax.value_and_grad(self._compute_loss)(latent)
            updates, opt_state = optimizer.update(grads, opt_state)
            latent = optax.apply_updates(latent, updates)
            return latent, opt_state, loss
        
        latent, opt_state = initial_latent, opt_state
        for step in tqdm.tqdm(range(self.hypers.num_steps), desc=f"Seed {seed}", leave=False):
            latent, opt_state, loss = train_step(latent, opt_state)
        
        final_h = jax.nn.sigmoid(latent)
        c5 = self._compute_c5_final(final_h)
        return c5, final_h
    
    def run_optimization(self):
        best_c5_bound = jnp.inf
        best_h = None
        
        print("\n" + "="*60)
        print("MULTI-RESTART OPTIMIZATION")
        print("="*60)
        
        for restart in range(self.hypers.num_restarts):
            key = jax.random.PRNGKey(self.hypers.seed_start + restart)
            
            # Generate initial latent
            latent = jax.random.normal(key, (self.num_intervals,), dtype=jnp.float64)
            
            c5, final_h = self._optimize_single_run(latent, self.hypers.seed_start + restart)
            
            print(f"Restart {restart + 1}: C5 = {c5:.8f}")
            
            if c5 < best_c5_bound:
                best_c5_bound = c5
                best_h = final_h
            
            if c5 < 0.380923:
                print(f"  *** NEW BEST: {c5:.8f} ***")
        
        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()
    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
