# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
import tqdm


@dataclass
class Hyperparameters:
    num_intervals: int = 1200
    base_learning_rate: float = 0.015
    num_steps: int = 35000
    penalty_strength: float = 5000.0
    num_restarts: int = 8
    seed_start: int = 0
    ref_learning_rate: float = 0.0015
    ref_steps: int = 15000
    ref_penalty: float = 30000.0


# Diverse initialization construction with all 12 patterns
def init_diverse_construct(n_int):
    """Generate diverse starting points for h using 12 patterns."""
    diverse_construct = {
        'gaussian': jax.random.normal,
        'uniform': jax.random.uniform,
        'sin_cos': lambda x: jnp.sin(2 * jnp.pi * x) * 2.0 + jnp.cos(4 * jnp.pi * x) * 1.0,
        'gaussian_scale': lambda x, k: jax.random.normal(k, (n_int,)) * 1.5,
        'uniform_shift': lambda x, k: jax.random.uniform(k, (n_int,), minval=-1, maxval=1),
        'bimodal_05': lambda x: jnp.where(x > 0.5, 3.0, -3.0),
        'bimodal_10': lambda x: jnp.where(x < 1.0, 3.0, -3.0),
        'gaussian_small': lambda x, k: jax.random.normal(k, (n_int,)) * 0.5,
        'plateau_067': lambda x: jnp.where(x < 2/3, 3.0, -3.0),
        'plateau_033': lambda x: jnp.where(x > 1/3, 3.0, -3.0),
        'centered': lambda x: jnp.where((x >= 0.5) & (x < 1.0), 3.0, -1.0),
        'wide_centered': lambda x: jnp.where((x >= 0.25) & (x <= 1.75), 2.5, -2.5),
    }
    return diverse_construct


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    Uses multi-restart strategy with diverse initialization.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h: jnp.ndarray) -> float:
        """Compute the C5 bound from h without penalty."""
        j_ = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j_, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound)

    def _get_diverse_init(self, seed: int) -> jnp.ndarray:
        """Get diverse initializations using all 12 patterns."""
        N = self.hypers.num_intervals
        x = jnp.linspace(0, 2, N)
        key = jax.random.PRNGKey(seed)
        
        diverse_construct = init_diverse_construct(N)
        
        best_latent = None
        best_obj = jnp.inf
        
        for idx, (name, base_func) in enumerate(diverse_construct.items()):
            if base_func is jax.random.normal:
                latent = base_func(key, (N,))
                key, subkey = jax.random.split(key)
            elif base_func is jax.random.uniform:
                latent = base_func(key, (N,), minval=-1, maxval=1)
                key, subkey = jax.random.split(key)
            elif name in ['sin_cos', 'bimodal_05', 'bimodal_10', 'plateau_067', 'plateau_033', 'centered', 'wide_centered']:
                latent = base_func(x)
                key, subkey = jax.random.split(key)
            elif name in ['gaussian_scale', 'uniform_shift', 'gaussian_small']:
                key, subkey = jax.random.split(key)
                latent = base_func(x, subkey)
            
            latent = latent + jax.random.normal(key, (N,)) * 0.4
            
            latent = jax.lax.stop_gradient(latent)
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
        """The loss function with integral constraint."""
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
        """Two-phase optimization: exploration then refinement."""
        initial_latent = self._get_diverse_init(seed)
        
        # Phase 1: Exploration
        optimizer1 = optax.adam(self.hypers.base_learning_rate)
        opt_state1 = optimizer1.init(initial_latent)

        latent = initial_latent
        
        @jax.jit
        def train_step1(latent, opt_state):
            loss, grads = jax.value_and_grad(lambda v: self._objective_fn(v))(latent)
            updates, opt_state = optimizer1.update(grads, opt_state)
            new_latent = optax.apply_updates(latent, updates)
            return new_latent, opt_state, loss

        latent, opt_state, _ = train_step1(latent, opt_state1)
        for step in tqdm.tqdm(range(self.hypers.num_steps), desc=f"Run {seed} Phase1"):
            latent, opt_state, loss = train_step1(latent, opt_state)

        # Phase 2: Refinement
        optimizer2 = optax.adam(self.hypers.ref_learning_rate)
        opt_state2 = optimizer2.init(latent)

        @jax.jit
        def refine_step(latent, opt_state):
            integral_h = jnp.sum(jax.nn.sigmoid(latent)) * self.dx
            latent_loss, grads = jax.value_and_grad(
                lambda v: self._objective_fn(v) + self.hypers.ref_penalty * (jnp.sum(jax.nn.sigmoid(v)) * self.dx - 1.0)**2
            )(latent)
            updates, opt_state = optimizer2.update(grads, opt_state)
            new_latent = optax.apply_updates(latent, updates)
            return new_latent, opt_state, latent_loss

        for step in tqdm.tqdm(range(self.hypers.ref_steps), desc=f"Run {seed} Phase2"):
            latent, opt_state, loss = refine_step(latent, opt_state2)

        final_h = jax.nn.sigmoid(latent)
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
