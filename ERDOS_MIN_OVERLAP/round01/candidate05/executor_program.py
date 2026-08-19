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
    learning_rate: float = 0.0035
    num_steps: int = 100000  # Maximum steps
    penalty_strength: float = 1500.0


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
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

    def run_optimization(self):
        optimizer = optax.adam(self.hypers.learning_rate)
        
        best_h, best_c5, best_integral = None, float('inf'), float('inf')
        x = jnp.arange(self.hypers.num_intervals) * self.dx
        
        # Half-half strategy (best so far)
        latent1 = jnp.zeros(self.hypers.num_intervals).at[:self.hypers.num_intervals//2].set(1.0)
        
        # Two-step
        latent2 = jnp.zeros(self.hypers.num_intervals)
        latent2 = latent2.at[:self.hypers.num_intervals//3].set(2.0)
        latent2 = latent2.at[self.hypers.num_intervals//3:].set(-0.5)
        
        # Asymmetric
        latent3 = jnp.zeros(self.hypers.num_intervals)
        latent3 = latent3.at[:self.hypers.num_intervals//4].set(3.0)
        
        # Center-concentrated
        latent4 = jnp.zeros(self.hypers.num_intervals)
        latent4 = latent4.at[self.hypers.num_intervals//4:3*self.hypers.num_intervals//4].set(2.0)
        
        strategies = [latent1, latent2, latent3, latent4]
        strategy_names = ['half-half', 'two-step', 'asymmetric', 'center']
        
        for name, latent_init in zip(strategy_names, strategies):
            opt_state = optimizer.init(latent_init)
            
            @jax.jit
            def train_step(latent_h_values, opt_state):
                loss, grads = jax.value_and_grad(self._objective_fn)(latent_h_values)
                updates, opt_state = optimizer.update(grads, opt_state)
                latent_h_values = optax.apply_updates(latent_h_values, updates)
                return latent_h_values, opt_state, loss

            latent_init = latent_init.copy()
            for step in tqdm.tqdm(range(self.hypers.num_steps), desc=f"Optimizing {name}"):
                latent_init, opt_state, loss = train_step(latent_init, opt_state)
            
            final_h = jax.nn.sigmoid(latent_init)
            j = 1.0 - final_h
            N = self.hypers.num_intervals
            h_padded = jnp.pad(final_h, (0, N))
            j_padded = jnp.pad(j, (0, N))
            corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
            correlation = jnp.fft.ifft(corr_fft).real
            c5_bound = jnp.max(correlation * self.dx)
            integral_h = jnp.sum(final_h) * self.dx
            
            if c5_bound < best_c5 and 0.999 <= integral_h <= 1.001:
                best_h = final_h
                best_c5 = c5_bound
                best_integral = integral_h
                print(f"{name}: C5={c5_bound:.8f}, integral={integral_h:.6f} [NEW BEST]")
            elif 0.999 <= integral_h <= 1.001:
                print(f"{name}: C5={c5_bound:.8f} (weak), integral={integral_h:.6f}")
        
        print(f"=== COMPLETE ===")
        print(f"Best C5 bound: {best_c5:.8f}")
        print(f"Best integral: {best_integral:.6f}")
        
        return np.array(best_h), float(best_c5), self.hypers.num_intervals


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound, n_points = optimizer.run_optimization()

    return final_h_values, c5_bound, n_points
# EVOLVE-BLOCK-END
