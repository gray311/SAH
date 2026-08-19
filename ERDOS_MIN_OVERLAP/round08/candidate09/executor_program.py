# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 100
    base_learning_rate: float = 0.01
    num_steps: int = 10000
    penalty_strength: float = 5000.0
    num_restarts: int = 5
    seed_start: int = 0


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    Uses direct step construction with piecewise constant functions.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5_bound(self, h: jnp.ndarray) -> float:
        """Compute the C5 bound from h without penalty."""
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        c5_bound = jnp.max(correlation * self.dx)
        return float(c5_bound)

    def _make_single_block(self, N):
        """h = 1 on [0,1], h = 0 on (1,2]. Integral = 1."""
        mid = N // 2
        return jnp.concatenate([jnp.ones(mid), jnp.zeros(N - mid)])

    def _make_double_block(self, N):
        """h = 1 on [0,0.5] U [1.5,2], h = 0 elsewhere. Integral = 1."""
        n_block = N // 4
        return jnp.concatenate([jnp.ones(n_block), jnp.zeros(N - 2*n_block), jnp.ones(n_block)])

    def _make_centered(self, N):
        """h = 1 on [0.3, 1.7], h = 0 elsewhere. Scale to integral=1."""
        left = int(N * 0.3)
        right = int(N * 0.7)
        width = right - left
        if width <= 0:
            width = 1
        height = 1.0 / width
        return jnp.concatenate([jnp.zeros(left), jnp.ones(width) * height, jnp.zeros(N - right)])

    def _make_uniform(self, N):
        """h = 0.5 everywhere. Integral = 1."""
        return jnp.ones(N) * 0.5

    def _get_best_initialization(self, seed: int) -> jnp.ndarray:
        """Get the best initialization from several pattern variations."""
        key = jax.random.PRNGKey(seed)
        
        patterns = [self._make_single_block, self._make_double_block, 
                   self._make_centered, self._make_uniform]
        
        best_h = None
        best_score = jnp.inf
        
        for make_h in patterns:
            h = make_h(self.hypers.num_intervals)
            h = jnp.clip(h, 0.0, 1.0)
            score = self._compute_c5_bound(h)
            if score < best_score:
                best_score = score
                best_h = h.copy()
        
        return best_h

    def _objective_fn(self, h_values: jnp.ndarray) -> jnp.ndarray:
        """The loss function for optimizing step heights."""
        h = jnp.clip(h_values, 0.0, 1.0)
        
        # Compute C5 bound
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        scaled_correlation = correlation * self.dx
        objective_loss = jnp.max(scaled_correlation)

        # Compute integral constraint loss
        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2

        total_loss = objective_loss + self.hypers.penalty_strength * constraint_loss
        return total_loss

    def _normalize_h(self, h: jnp.ndarray) -> jnp.ndarray:
        """Normalize h to have integral = 1 and values in [0,1]."""
        integral_h = jnp.sum(h) * self.dx
        if integral_h <= 0:
            return h
        
        h_norm = h / integral_h
        
        # Scale down if any value exceeds 1
        max_val = jnp.max(h_norm)
        if max_val > 1.0:
            h_norm = h_norm / max_val
        
        # Re-normalize
        integral_after = jnp.sum(h_norm) * self.dx
        if integral_after > 0:
            h_norm = h_norm / integral_after
        
        return h_norm

    def _optimize_single_run(self, seed: int):
        """Run a single optimization with given seed."""
        initial_h = self._get_best_initialization(seed)
        
        optimizer = optax.adam(self.hypers.base_learning_rate)
        opt_state = optimizer.init(initial_h)

        @jax.jit
        def train_step(h_values, opt_state):
            loss, grads = jax.value_and_grad(lambda v: self._objective_fn(v))(h_values)
            updates, opt_state = optimizer.update(grads, opt_state)
            h_values = optax.apply_updates(h_values, updates)
            h_values = jnp.clip(h_values, 0.0, 1.0)
            return h_values, opt_state, loss

        best_h = initial_h.copy()
        current_h = initial_h
        current_opt_state = opt_state

        for step in range(self.hypers.num_steps):
            current_h, current_opt_state, loss = train_step(current_h, current_opt_state)
            
            h_norm = self._normalize_h(current_h)
            obj_current = self._compute_c5_bound(h_norm)
            
            h_best_norm = self._normalize_h(best_h)
            obj_best = self._compute_c5_bound(h_best_norm)
            
            if obj_current < obj_best:
                best_h = current_h.copy()

        h_final = self._normalize_h(best_h)
        return float(self._compute_c5_bound(h_final)), h_final

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
