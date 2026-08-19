# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Hyperparameters optimized for TRUE step function search."""
    num_intervals: int = 400
    learning_rate: float = 0.18
    num_steps: int = 35000
    warmup_steps: int = 3500
    best_c2: float = 0.8962799441554086
    stagnation_window: int = 100
    reinit_fraction: float = 0.12
    reinit_std: float = 0.02
    reinit_interval: int = 200


class C2Optimizer:
    def __init__(self, hypers: OptimizerHyperparameters):
        self.hypers = hypers
        self.best_f = None
        self.best_c2 = hypers.best_c2

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        f_non_negative = jax.nn.relu(f_values)
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real

        num_conv_points = len(convolution)
        h = 1.0 / (num_conv_points + 1)
        y_points = jnp.concatenate([jnp.array([0.0]), convolution, jnp.array([0.0])])
        y1, y2 = y_points[:-1], y_points[1:]
        l2_norm_squared = jnp.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))

        norm_1 = jnp.sum(jnp.abs(convolution)) / (len(convolution) + 1)
        norm_inf = jnp.max(jnp.abs(convolution))
        denominator = norm_1 * norm_inf
        c2_ratio = l2_norm_squared / denominator
        return -c2_ratio

    def _create_step_initializer(self, n, pattern_idx):
        """Create TRUE piecewise-constant step functions - final optimized variants."""
        f = jnp.zeros(n)
        
        if pattern_idx == 0:
            # High peak single step - height 1.25
            start = int(0.25 * n)
            end = int(0.75 * n)
            f = f.at[start:end].set(1.25)
        elif pattern_idx == 1:
            # Higher peak - height 1.35
            start = int(0.28 * n)
            end = int(0.72 * n)
            f = f.at[start:end].set(1.35)
        elif pattern_idx == 2:
            # Very high narrow peak - height 1.5
            start = int(0.30 * n)
            end = int(0.70 * n)
            f = f.at[start:end].set(1.5)
        elif pattern_idx == 3:
            # Multi-level with high middle - heights 0.8, 1.8, 0.8
            f = f.at[int(0.15*n):int(0.25*n)].set(0.8)
            f = f.at[int(0.25*n):int(0.75*n)].set(1.8)
            f = f.at[int(0.75*n):int(0.85*n)].set(0.8)
        elif pattern_idx == 4:
            # Three-level asymmetric - heights 1.0, 2.2, 1.3
            f = f.at[int(0.1*n):int(0.2*n)].set(1.0)
            f = f.at[int(0.2*n):int(0.5*n)].set(2.2)
            f = f.at[int(0.5*n):int(0.7*n)].set(1.3)
        elif pattern_idx == 5:
            # Two high steps - height 1.4
            f = f.at[int(0.2*n):int(0.4*n)].set(1.4)
            f = f.at[int(0.5*n):int(0.8*n)].set(1.4)
        elif pattern_idx == 6:
            # Four-level function - heights 0.6, 1.2, 1.6, 0.9
            f = f.at[int(0.05*n):int(0.2*n)].set(0.6)
            f = f.at[int(0.2*n):int(0.35*n)].set(1.2)
            f = f.at[int(0.35*n):int(0.65*n)].set(1.6)
            f = f.at[int(0.65*n):int(0.95*n)].set(0.9)
        elif pattern_idx == 7:
            # Narrow high peak with wings - heights 0.7, 1.9, 0.7
            f = f.at[int(0.1*n):int(0.3*n)].set(0.7)
            f = f.at[int(0.3*n):int(0.7*n)].set(1.9)
            f = f.at[int(0.7*n):int(0.9*n)].set(0.7)
        elif pattern_idx == 8:
            # Staircase pattern - heights 0.5, 0.9, 1.4, 1.1
            f = f.at[int(0.05*n):int(0.25*n)].set(0.5)
            f = f.at[int(0.25*n):int(0.45*n)].set(0.9)
            f = f.at[int(0.45*n):int(0.65*n)].set(1.4)
            f = f.at[int(0.65*n):int(0.95*n)].set(1.1)
        elif pattern_idx == 9:
            # Very high central peak - height 1.6
            f = f.at[int(0.22*n):int(0.78*n)].set(1.6)
        elif pattern_idx == 10:
            # Another high peak variant - height 1.55
            start = int(0.24 * n)
            end = int(0.76 * n)
            f = f.at[start:end].set(1.55)
        elif pattern_idx == 11:
            # Pyramid with very high peak - heights 0.6, 1.4, 2.0, 1.4, 0.6
            f = f.at[int(0.05*n):int(0.20*n)].set(0.6)
            f = f.at[int(0.20*n):int(0.40*n)].set(1.4)
            f = f.at[int(0.40*n):int(0.60*n)].set(2.0)
            f = f.at[int(0.60*n):int(0.80*n)].set(1.4)
            f = f.at[int(0.80*n):int(0.95*n)].set(0.6)
        elif pattern_idx == 12:
            # Ultra-stretched pyramid - heights 0.5, 1.2, 1.9, 1.2, 0.5
            f = f.at[int(0.03*n):int(0.18*n)].set(0.5)
            f = f.at[int(0.18*n):int(0.38*n)].set(1.2)
            f = f.at[int(0.38*n):int(0.62*n)].set(1.9)
            f = f.at[int(0.62*n):int(0.82*n)].set(1.2)
            f = f.at[int(0.82*n):int(0.97*n)].set(0.5)
        elif pattern_idx == 13:
            # High plateau with sharp edges - height 1.58
            start = int(0.23 * n)
            end = int(0.77 * n)
            f = f.at[start:end].set(1.58)
        elif pattern_idx == 14:
            # Even higher plateau - height 1.62
            start = int(0.22 * n)
            end = int(0.78 * n)
            f = f.at[start:end].set(1.62)
        elif pattern_idx == 15:
            # Five-level symmetric - heights 0.4, 0.9, 1.5, 1.6, 0.4
            f = f.at[int(0.02*n):int(0.15*n)].set(0.4)
            f = f.at[int(0.15*n):int(0.28*n)].set(0.9)
            f = f.at[int(0.28*n):int(0.42*n)].set(1.5)
            f = f.at[int(0.42*n):int(0.58*n)].set(1.6)
            f = f.at[int(0.58*n):int(0.85*n)].set(0.9)
            f = f.at[int(0.85*n):int(0.98*n)].set(0.4)
        elif pattern_idx == 16:
            # Seven-level fine-grained
            f = f.at[int(0.01*n):int(0.10*n)].set(0.3)
            f = f.at[int(0.10*n):int(0.20*n)].set(0.6)
            f = f.at[int(0.20*n):int(0.30*n)].set(1.0)
            f = f.at[int(0.30*n):int(0.40*n)].set(1.3)
            f = f.at[int(0.40*n):int(0.50*n)].set(1.7)
            f = f.at[int(0.50*n):int(0.60*n)].set(1.3)
            f = f.at[int(0.60*n):int(0.90*n)].set(0.6)
        elif pattern_idx == 17:
            # Eight-level ultra-fine
            f = f.at[int(0.01*n):int(0.08*n)].set(0.25)
            f = f.at[int(0.08*n):int(0.16*n)].set(0.5)
            f = f.at[int(0.16*n):int(0.24*n)].set(0.9)
            f = f.at[int(0.24*n):int(0.32*n)].set(1.2)
            f = f.at[int(0.32*n):int(0.40*n)].set(1.5)
            f = f.at[int(0.40*n):int(0.48*n)].set(1.6)
            f = f.at[int(0.48*n):int(0.64*n)].set(1.2)
            f = f.at[int(0.64*n):int(0.90*n)].set(0.5)
        elif pattern_idx == 18:
            # High plateau with optimized width - height 1.65
            start = int(0.21 * n)
            end = int(0.79 * n)
            f = f.at[start:end].set(1.65)
        elif pattern_idx == 19:
            # Optimized plateau - height 1.52
            start = int(0.25 * n)
            end = int(0.75 * n)
            f = f.at[start:end].set(1.52)
        elif pattern_idx == 20:
            # Two-step asymmetric - heights 1.0, 1.8, 1.2
            f = f.at[int(0.1*n):int(0.4*n)].set(1.0)
            f = f.at[int(0.4*n):int(0.6*n)].set(1.8)
            f = f.at[int(0.6*n):int(0.9*n)].set(1.2)
        elif pattern_idx == 21:
            # Three-step symmetric - heights 0.7, 1.7, 0.7
            f = f.at[int(0.1*n):int(0.3*n)].set(0.7)
            f = f.at[int(0.3*n):int(0.7*n)].set(1.7)
            f = f.at[int(0.7*n):int(0.9*n)].set(0.7)
        elif pattern_idx == 22:
            # Four-step symmetric - heights 0.5, 1.1, 1.5, 1.1, 0.5
            f = f.at[int(0.05*n):int(0.2*n)].set(0.5)
            f = f.at[int(0.2*n):int(0.35*n)].set(1.1)
            f = f.at[int(0.35*n):int(0.65*n)].set(1.5)
            f = f.at[int(0.65*n):int(0.8*n)].set(1.1)
            f = f.at[int(0.8*n):int(0.95*n)].set(0.5)
        elif pattern_idx == 23:
            # Five-step fine - heights 0.4, 0.8, 1.4, 1.4, 0.8, 0.4
            f = f.at[int(0.02*n):int(0.14*n)].set(0.4)
            f = f.at[int(0.14*n):int(0.26*n)].set(0.8)
            f = f.at[int(0.26*n):int(0.38*n)].set(1.4)
            f = f.at[int(0.38*n):int(0.50*n)].set(1.4)
            f = f.at[int(0.50*n):int(0.62*n)].set(0.8)
            f = f.at[int(0.62*n):int(0.98*n)].set(0.4)
        else:
            # Default: standard high step
            start = int(0.3*n)
            end = int(0.7*n)
            f = f.at[start:end].set(1.3)
        
        return f

    def _create_multi_start(self, num_starts=25):
        """Create diverse TRUE step function initializations."""
        initializations = []
        for i in range(num_starts):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_step_initializer(0, i)  # n passed later
            initializations.append((init, key))
        return initializations

    def _local_reinitialization(self, f_values: jnp.ndarray, key) -> jnp.ndarray:
        n = len(f_values)
        num_reinit = int(self.hypers.reinit_fraction * n)
        key, subkey = jax.random.split(key)
        reinit_indices = jax.random.permutation(subkey, n)[:num_reinit]
        perturbation = jax.random.normal(subkey, f_values.shape) * self.hypers.reinit_std
        f_new = f_values.at[reinit_indices].set(f_values[reinit_indices] + perturbation[reinit_indices])
        f_new = jax.nn.relu(f_new)
        return f_new

    def _check_stagnation(self, c2_history: list, step_count: int) -> bool:
        if step_count < self.hypers.stagnation_window:
            return False
        recent_c2s = c2_history[-self.hypers.stagnation_window:]
        improvement = recent_c2s[-1] - recent_c2s[0]
        if improvement > 1e-6:
            return False
        return True

    def _train_step(self, f_values: jnp.ndarray, opt_state, optimizer) -> Tuple:
        loss, grads = jax.value_and_grad(self._objective_fn)(f_values)
        updates, opt_state = optimizer.update(grads, opt_state, f_values)
        f_values = optax.apply_updates(f_values, updates)
        return f_values, opt_state, loss, grads

    def run_optimization(self) -> Tuple:
        # Create initializations with proper n
        initializations = []
        n = self.hypers.num_intervals
        
        for i in range(25):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_step_initializer(n, i)
            initializations.append((init, key))
        
        best_f = None
        best_c2 = 0.0
        
        for idx, (init_f, seed_key) in enumerate(initializations):
            print(f"\n=== Starting optimization from step function {idx + 1}/25 ===")
            schedule1 = optax.warmup_cosine_decay_schedule(
                init_value=0.0,
                peak_value=self.hypers.learning_rate * 1.4,
                warmup_steps=self.hypers.warmup_steps,
                decay_steps=self.hypers.num_steps // 2 - self.hypers.warmup_steps,
                end_value=self.hypers.learning_rate * 0.10,
            )
            optimizer1 = optax.adam(learning_rate=schedule1, eps=1e-8)
            key = jax.random.PRNGKey(42 + idx * 100)
            f_values = init_f + 0.05 * jax.random.normal(key, init_f.shape)
            opt_state = optimizer1.init(f_values)
            reinit_key = jax.random.PRNGKey(42 + idx * 1000)
            c2_history = []
            
            train_step_jit1 = jax.jit(lambda fv, os: self._train_step(fv, os, optimizer1))
            for step in range(self.hypers.num_steps // 2):
                f_values, opt_state, loss, grads = train_step_jit1(f_values, opt_state)
                step_count = step + 1
                current_c2 = -loss
                c2_history.append(float(current_c2))
                if self._check_stagnation(c2_history, step_count):
                    if step_count % self.hypers.reinit_interval == 0:
                        f_values = self._local_reinitialization(f_values, reinit_key)
                        reinit_key, _ = jax.random.split(reinit_key)
                if float(current_c2) > float(best_c2):
                    best_c2 = current_c2
                    best_f = f_values.copy()
                if step % 5000 == 0 or step == self.hypers.num_steps // 2 - 1:
                    print(f"  Step {step:5d} | C2 ≈ {-loss:.8f} | Best: {best_c2:.8f}")
            
            schedule2 = optax.warmup_cosine_decay_schedule(
                init_value=0.0,
                peak_value=self.hypers.learning_rate * 0.35,
                warmup_steps=500,
                decay_steps=self.hypers.num_steps // 2 - 500,
                end_value=self.hypers.learning_rate * 1e-4,
            )
            optimizer2 = optax.adam(learning_rate=schedule2, eps=1e-8)
            key = jax.random.PRNGKey(43 + idx * 100)
            f_values = best_f + 0.04 * jax.random.normal(key, best_f.shape)
            opt_state = optimizer2.init(f_values)
            
            print(f"\n=== Phase 2 fine-tuning for step function {idx + 1} ===")
            train_step_jit2 = jax.jit(lambda fv, os: self._train_step(fv, os, optimizer2))
            step_count = 0
            reinit_key = jax.random.PRNGKey(43 + idx * 1000)
            c2_history = []
            
            for step in range(self.hypers.num_steps // 2):
                f_values, opt_state, loss, grads = train_step_jit2(f_values, opt_state)
                step_count = step + 1
                current_c2 = -loss
                c2_history.append(float(current_c2))
                if self._check_stagnation(c2_history, step_count):
                    if step_count % self.hypers.reinit_interval == 0:
                        f_values = self._local_reinitialization(f_values, reinit_key)
                        reinit_key, _ = jax.random.split(reinit_key)
                if float(current_c2) > float(best_c2):
                    best_c2 = current_c2
                    best_f = f_values.copy()
                if step % 5000 == 0 or step == self.hypers.num_steps // 2 - 1:
                    print(f"  Step {step:5d} | C2 ≈ {-loss:.8f} | Best: {best_c2:.8f}")

        return jax.nn.relu(best_f), best_c2 if best_f is not None else 0.0


def run():
    hypers = OptimizerHyperparameters(best_c2=0.8962799441554086)
    optimizer = C2Optimizer(hypers)
    optimized_f, final_c2_val = optimizer.run_optimization()
    f_values_np = np.array(optimized_f)
    return f_values_np, float(final_c2_val), float(-final_c2_val), hypers.num_intervals
# EVOLVE-BLOCK-END
