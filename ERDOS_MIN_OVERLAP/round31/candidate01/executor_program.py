# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
from dataclasses import dataclass
import tqdm


@dataclass
class Hyperparameters:
    num_intervals: int = 800
    base_learning_rate: float = 0.005
    num_steps: int = 50000
    penalty_strength: float = 80.0
    num_restarts: int = 3
    seed_start: int = 0


class ErdosOptimizer:
    def __init__(self, hypers):
        self.hypers = hypers
        self.dx = 2.0 / self.hypers.num_intervals
        self.N = self.hypers.num_intervals

    def _compute_c5_bound(self, h):
        j_val = 1.0 - h
        h_padded = jnp.pad(h, (0, self.N))
        j_padded = jnp.pad(j_val, (0, self.N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        return float(jnp.max(correlation * self.dx))

    def _create_valid_h(self, pattern, x=None):
        """Create a valid step function with integral=1 exactly."""
        if x is None:
            x = jnp.linspace(0, 2, self.N)
        
        if pattern == "half":
            h = jnp.where(x < 1.0, 1.0, 0.0)
        elif pattern == "third":
            h = jnp.where(x < 0.33, 1.0, 0.0)
        elif pattern == "two_thirds":
            h = jnp.where(x < 0.66, 1.0, 0.0)
        elif pattern == "quarter_both":
            h = jnp.zeros(self.N)
            h = h.at[(x >= 0) & (x < 0.4)].set(1.0)
            h = h.at[(x >= 1.6) & (x < 2.0)].set(1.0)
        elif pattern == "uniform":
            h = jnp.ones(self.N) * 0.5
        elif pattern == "two_peaks":
            h = jnp.zeros(self.N)
            h = h.at[(x >= 0.2) & (x < 0.4)].set(1.0)
            h = h.at[(x >= 1.6) & (x < 1.8)].set(1.0)
        elif pattern == "three_peaks":
            h = jnp.zeros(self.N)
            h = h.at[(x >= 0.2) & (x < 0.35)].set(1.0)
            h = h.at[(x >= 0.85) & (x < 1.0)].set(1.0)
            h = h.at[(x >= 1.65) & (x < 1.8)].set(1.0)
        elif pattern == "four_peaks":
            h = jnp.zeros(self.N)
            h = h.at[(x >= 0.2) & (x < 0.28)].set(1.0)
            h = h.at[(x >= 0.62) & (x < 0.7)].set(1.0)
            h = h.at[(x >= 1.0) & (x < 1.08)].set(1.0)
            h = h.at[(x >= 1.4) & (x < 1.48)].set(1.0)
        else:
            h = jnp.where(x < 1.0, 1.0, 0.0)
        
        # Normalize to get integral=1
        integral = jnp.sum(h) * self.dx
        if integral > 1e-10:
            h = h / integral
        
        # Clip to [0,1]
        h = jnp.clip(h, 0.0, 1.0)
        
        # Renormalize
        integral = jnp.sum(h) * self.dx
        if integral > 1e-10:
            h = h / integral
        
        return h

    def _get_best_initialization(self, seed):
        x = jnp.linspace(0, 2, self.N)
        
        # Start with the best pattern from previous success
        h = self._create_valid_h("half", x)
        
        # Evaluate all patterns and pick best
        patterns = [
            "half", "third", "two_thirds", "quarter_both", "uniform",
            "two_peaks", "three_peaks", "four_peaks"
        ]
        
        best_latent = None
        best_obj = jnp.inf
        
        for pattern in patterns:
            h = self._create_valid_h(pattern, x)
            
            j_val = 1.0 - h
            h_padded = jnp.pad(h, (0, self.N))
            j_padded = jnp.pad(j_val, (0, self.N))
            corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
            correlation = jnp.fft.ifft(corr_fft).real
            obj = jnp.max(correlation * self.dx)
            
            if obj < best_obj:
                best_obj = obj
                h_safe = jnp.clip(h, 0.0001, 0.9999)
                best_latent = jnp.log(h_safe / (1.0 - h_safe))
        
        return best_latent

    def _objective_fn(self, latent_h_values):
        h = jax.nn.sigmoid(latent_h_values)
        j_val = 1.0 - h
        h_padded = jnp.pad(h, (0, self.N))
        j_padded = jnp.pad(j_val, (0, self.N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        objective_loss = jnp.max(correlation * self.dx)
        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2
        return objective_loss + self.hypers.penalty_strength * constraint_loss

    def _optimize_single_run(self, seed):
        initial_latent = self._get_best_initialization(seed)
        
        if initial_latent is None:
            return 10.0, jnp.zeros(self.N)
        
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

        for step in tqdm.tqdm(range(self.hypers.num_steps), desc=f"Run {seed}", leave=False):
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

        return best_h, float(best_c5_bound)


def run():
    hypers = Hyperparameters()
    optimizer = ErdosOptimizer(hypers)
    final_h_values, c5_bound = optimizer.run_optimization()
    return final_h_values, c5_bound, hypers.num_intervals
# EVOLVE-BLOCK-END
