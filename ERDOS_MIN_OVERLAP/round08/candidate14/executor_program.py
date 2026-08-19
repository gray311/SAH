# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
import tqdm


@dataclass
class Hyperparameters:
    num_intervals: int = 600  # Higher resolution
    base_learning_rate: float = 0.015
    num_steps: int = 22000
    penalty_strength: float = 8000.0
    num_restarts: int = 8
    seed_start: int = 0


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    Uses strategic block placements with refinement.
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

    def _construct_two_blocks_optimal(self, intervals: int) -> jnp.ndarray:
        """h = 1 on [0, 0.5] U [1, 1.5] (two intervals of length 0.5 each)"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.where((x <= 0.5) | (x > 1.0) & (x <= 1.5), 1.0, 0.0)
        return h

    def _construct_two_blocks_shifted(self, intervals: int, shift: float = 0.25) -> jnp.ndarray:
        """h = 1 on [shift, 0.5+shift] U [1+shift, 1.5+shift]"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        h = h.at[(x >= shift) & (x < 0.5 + shift)].set(1.0)
        h = h.at[(x >= 1 + shift) & (x < 1.5 + shift)].set(1.0)
        return h

    def _construct_three_blocks_optimal(self, intervals: int) -> jnp.ndarray:
        """h = 1 on three blocks of total length 1"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        h = h.at[(x >= 0.0) & (x < 0.333)].set(1.0)
        h = h.at[(x >= 0.667) & (x < 1.0)].set(1.0)
        h = h.at[(x >= 1.333) & (x < 1.667)].set(1.0)
        return h

    def _construct_four_blocks_optimal(self, intervals: int) -> jnp.ndarray:
        """h = 1 on four blocks of total length 1"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        h = h.at[(x >= 0.0) & (x < 0.25)].set(1.0)
        h = h.at[(x >= 0.75) & (x < 1.0)].set(1.0)
        h = h.at[(x >= 1.25) & (x < 1.5)].set(1.0)
        h = h.at[(x >= 1.75) & (x < 2.0)].set(1.0)
        return h

    def _construct_five_blocks_optimal(self, intervals: int) -> jnp.ndarray:
        """h = 1 on five blocks of total length 1"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        h = h.at[(x >= 0.0) & (x < 0.2)].set(1.0)
        h = h.at[(x >= 0.4) & (x < 0.6)].set(1.0)
        h = h.at[(x >= 0.8) & (x < 1.0)].set(1.0)
        h = h.at[(x >= 1.2) & (x < 1.4)].set(1.0)
        h = h.at[(x >= 1.6) & (x < 1.8)].set(1.0)
        return h

    def _construct_six_blocks_optimal(self, intervals: int) -> jnp.ndarray:
        """h = 1 on six blocks of total length 1"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        block_width = 1/6
        h = h.at[(x >= 0.0) & (x < block_width)].set(1.0)
        h = h.at[(x >= block_width) & (x < 2*block_width)].set(1.0)
        h = h.at[(x >= 2*block_width) & (x < 3*block_width)].set(1.0)
        h = h.at[(x >= 3*block_width) & (x < 4*block_width)].set(1.0)
        h = h.at[(x >= 4*block_width) & (x < 5*block_width)].set(1.0)
        h = h.at[(x >= 5*block_width) & (x < 6*block_width)].set(1.0)
        return h

    def _construct_seven_blocks_optimal(self, intervals: int) -> jnp.ndarray:
        """h = 1 on seven blocks of total length 1"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        block_width = 1/7
        h = h.at[(x >= 0.0) & (x < block_width)].set(1.0)
        h = h.at[(x >= block_width) & (x < 2*block_width)].set(1.0)
        h = h.at[(x >= 2*block_width) & (x < 3*block_width)].set(1.0)
        h = h.at[(x >= 3*block_width) & (x < 4*block_width)].set(1.0)
        h = h.at[(x >= 4*block_width) & (x < 5*block_width)].set(1.0)
        h = h.at[(x >= 5*block_width) & (x < 6*block_width)].set(1.0)
        h = h.at[(x >= 6*block_width) & (x < 7*block_width)].set(1.0)
        return h

    def _construct_eight_blocks_optimal(self, intervals: int) -> jnp.ndarray:
        """h = 1 on eight blocks of total length 1"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.zeros(N)
        block_width = 1/8
        h = h.at[(x >= 0.0) & (x < block_width)].set(1.0)
        h = h.at[(x >= block_width) & (x < 2*block_width)].set(1.0)
        h = h.at[(x >= 2*block_width) & (x < 3*block_width)].set(1.0)
        h = h.at[(x >= 3*block_width) & (x < 4*block_width)].set(1.0)
        h = h.at[(x >= 4*block_width) & (x < 5*block_width)].set(1.0)
        h = h.at[(x >= 5*block_width) & (x < 6*block_width)].set(1.0)
        h = h.at[(x >= 6*block_width) & (x < 7*block_width)].set(1.0)
        h = h.at[(x >= 7*block_width) & (x < 8*block_width)].set(1.0)
        return h

    def _construct_optimal_candidate(self, intervals: int) -> jnp.ndarray:
        """Best mathematical candidate: two blocks at edges"""
        N = intervals
        x = jnp.linspace(0, 2, N)
        h = jnp.where((x <= 0.5) | (x > 1.0) & (x <= 1.5), 1.0, 0.0)
        return h

    def _get_best_initialization(self, seed: int) -> jnp.ndarray:
        """Get the best initialization from direct construction."""
        N = self.hypers.num_intervals
        key = jax.random.PRNGKey(seed)
        
        constructions = [
            ("two_blocks_optimal", self._construct_two_blocks_optimal(N)),
            ("two_blocks_shifted_0.25", self._construct_two_blocks_shifted(N, 0.25)),
            ("two_blocks_shifted_0.5", self._construct_two_blocks_shifted(N, 0.5)),
            ("two_blocks_shifted_0.33", self._construct_two_blocks_shifted(N, 0.33)),
            ("three_blocks_optimal", self._construct_three_blocks_optimal(N)),
            ("four_blocks_optimal", self._construct_four_blocks_optimal(N)),
            ("five_blocks_optimal", self._construct_five_blocks_optimal(N)),
            ("six_blocks_optimal", self._construct_six_blocks_optimal(N)),
            ("seven_blocks_optimal", self._construct_seven_blocks_optimal(N)),
            ("eight_blocks_optimal", self._construct_eight_blocks_optimal(N)),
            ("optimal_candidate", self._construct_optimal_candidate(N)),
        ]
        
        best_latent = None
        best_obj = jnp.inf
        
        for name, h in constructions:
            h_clamped = jnp.clip(h, 1e-6, 1-1e-6)
            latent = jnp.log(h_clamped / (1 - h_clamped))
            
            key, subkey = jax.random.split(key)
            latent = latent + jax.random.normal(subkey, (N,)) * 0.1
            
            j = 1.0 - h
            h_padded = jnp.pad(h, (0, N))
            j_padded = jnp.pad(j, (0, N))
            corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
            correlation = jnp.fft.ifft(corr_fft).real
            obj = jnp.max(correlation * self.dx)
            
            if obj < best_obj:
                best_obj = obj
                best_latent = latent
        
        return best_latent

    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        """The loss function."""
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
