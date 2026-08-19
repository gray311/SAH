# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Hyperparameters with optimized reinitialization for fine-tuning."""
    num_intervals: int = 450
    learning_rate: float = 0.18
    num_steps: int = 20000
    warmup_steps: int = 2000
    best_c2: float = 0.927976
    stagnation_window: int = 100
    reinit_fraction: float = 0.16
    reinit_std: float = 0.026
    reinit_interval: int = 190


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
        """Create TRUE piecewise-constant step functions - optimized heights."""
        f = jnp.zeros(n)
        
        if pattern_idx == 0:
            # High peak single step - height 1.40
            start = int(0.25 * n)
            end = int(0.75 * n)
            f = f.at[start:end].set(1.40)
        elif pattern_idx == 1:
            # Higher peak - height 1.50
            start = int(0.27 * n)
            end = int(0.73 * n)
            f = f.at[start:end].set(1.50)
        elif pattern_idx == 2:
            # Very high narrow peak - height 1.60
            start = int(0.30 * n)
            end = int(0.70 * n)
            f = f.at[start:end].set(1.60)
        elif pattern_idx == 3:
            # Multi-level with high middle - heights 0.90, 1.90, 0.90
            f = f.at[int(0.15*n):int(0.25*n)].set(0.90)
            f = f.at[int(0.25*n):int(0.75*n)].set(1.90)
            f = f.at[int(0.75*n):int(0.85*n)].set(0.90)
        elif pattern_idx == 4:
            # Three-level asymmetric - heights 1.10, 2.30, 1.40
            f = f.at[int(0.11*n):int(0.21*n)].set(1.10)
            f = f.at[int(0.21*n):int(0.49*n)].set(2.30)
            f = f.at[int(0.49*n):int(0.71*n)].set(1.40)
        elif pattern_idx == 5:
            # Two high steps - height 1.50
            f = f.at[int(0.22*n):int(0.38*n)].set(1.50)
            f = f.at[int(0.52*n):int(0.82*n)].set(1.50)
        elif pattern_idx == 6:
            # Four-level function - heights 0.70, 1.30, 1.70, 1.00
            f = f.at[int(0.06*n):int(0.20*n)].set(0.70)
            f = f.at[int(0.20*n):int(0.34*n)].set(1.30)
            f = f.at[int(0.34*n):int(0.64*n)].set(1.70)
            f = f.at[int(0.64*n):int(0.94*n)].set(1.00)
        elif pattern_idx == 7:
            # Narrow high peak with wings - heights 0.80, 2.00, 0.80
            f = f.at[int(0.12*n):int(0.28*n)].set(0.80)
            f = f.at[int(0.28*n):int(0.72*n)].set(2.00)
            f = f.at[int(0.72*n):int(0.88*n)].set(0.80)
        elif pattern_idx == 8:
            # Staircase pattern - heights 0.60, 1.00, 1.50, 1.20
            f = f.at[int(0.06*n):int(0.24*n)].set(0.60)
            f = f.at[int(0.24*n):int(0.44*n)].set(1.00)
            f = f.at[int(0.44*n):int(0.64*n)].set(1.50)
            f = f.at[int(0.64*n):int(0.94*n)].set(1.20)
        elif pattern_idx == 9:
            # Very high central peak - height 1.70
            start = int(0.23 * n)
            end = int(0.77 * n)
            f = f.at[start:end].set(1.70)
        elif pattern_idx == 10:
            # Another high peak variant - height 1.65
            start = int(0.25 * n)
            end = int(0.75 * n)
            f = f.at[start:end].set(1.65)
        elif pattern_idx == 11:
            # Pyramid with very high peak - heights 0.70, 1.50, 2.10, 1.50, 0.70
            f = f.at[int(0.06*n):int(0.19*n)].set(0.70)
            f = f.at[int(0.19*n):int(0.40*n)].set(1.50)
            f = f.at[int(0.40*n):int(0.60*n)].set(2.10)
            f = f.at[int(0.60*n):int(0.80*n)].set(1.50)
            f = f.at[int(0.80*n):int(0.94*n)].set(0.70)
        elif pattern_idx == 12:
            # Ultra-stretched pyramid - heights 0.60, 1.30, 2.00, 1.30, 0.60
            f = f.at[int(0.04*n):int(0.17*n)].set(0.60)
            f = f.at[int(0.17*n):int(0.37*n)].set(1.30)
            f = f.at[int(0.37*n):int(0.63*n)].set(2.00)
            f = f.at[int(0.63*n):int(0.83*n)].set(1.30)
            f = f.at[int(0.83*n):int(0.96*n)].set(0.60)
        elif pattern_idx == 13:
            # High plateau with sharp edges - height 1.65
            start = int(0.24 * n)
            end = int(0.76 * n)
            f = f.at[start:end].set(1.65)
        elif pattern_idx == 14:
            # Even higher plateau - height 1.70
            start = int(0.23 * n)
            end = int(0.77 * n)
            f = f.at[start:end].set(1.70)
        elif pattern_idx == 15:
            # Five-level symmetric - heights 0.50, 1.00, 1.60, 1.70, 1.00
            f = f.at[int(0.03*n):int(0.14*n)].set(0.50)
            f = f.at[int(0.14*n):int(0.28*n)].set(1.00)
            f = f.at[int(0.28*n):int(0.42*n)].set(1.60)
            f = f.at[int(0.42*n):int(0.58*n)].set(1.70)
            f = f.at[int(0.58*n):int(0.84*n)].set(1.00)
            f = f.at[int(0.84*n):int(0.97*n)].set(0.50)
        elif pattern_idx == 16:
            # Seven-level fine-grained
            f = f.at[int(0.02*n):int(0.09*n)].set(0.40)
            f = f.at[int(0.09*n):int(0.19*n)].set(0.80)
            f = f.at[int(0.19*n):int(0.29*n)].set(1.20)
            f = f.at[int(0.29*n):int(0.39*n)].set(1.55)
            f = f.at[int(0.39*n):int(0.49*n)].set(1.95)
            f = f.at[int(0.49*n):int(0.59*n)].set(1.55)
            f = f.at[int(0.59*n):int(0.89*n)].set(0.80)
            f = f.at[int(0.89*n):int(0.94*n)].set(0.40)
        elif pattern_idx == 17:
            # Eight-level ultra-fine
            f = f.at[int(0.02*n):int(0.07*n)].set(0.32)
            f = f.at[int(0.07*n):int(0.15*n)].set(0.62)
            f = f.at[int(0.15*n):int(0.23*n)].set(1.02)
            f = f.at[int(0.23*n):int(0.31*n)].set(1.40)
            f = f.at[int(0.31*n):int(0.39*n)].set(1.70)
            f = f.at[int(0.39*n):int(0.47*n)].set(1.75)
            f = f.at[int(0.47*n):int(0.63*n)].set(1.40)
            f = f.at[int(0.63*n):int(0.89*n)].set(0.62)
            f = f.at[int(0.89*n):int(0.94*n)].set(0.32)
        elif pattern_idx == 18:
            # High plateau with optimized width - height 1.73
            start = int(0.22 * n)
            end = int(0.78 * n)
            f = f.at[start:end].set(1.73)
        elif pattern_idx == 19:
            # ASYMMETRIC 3-PEAK: Highly asymmetric with three distinct peaks
            f = f.at[int(0.05*n):int(0.12*n)].set(0.22)
            f = f.at[int(0.12*n):int(0.35*n)].set(3.10)
            f = f.at[int(0.35*n):int(0.42*n)].set(0.29)
            f = f.at[int(0.42*n):int(0.68*n)].set(2.53)
            f = f.at[int(0.68*n):int(0.85*n)].set(0.19)
        elif pattern_idx == 20:
            # VARIANT 1: Slightly different asymmetric 3-peak
            f = f.at[int(0.05*n):int(0.12*n)].set(0.25)
            f = f.at[int(0.12*n):int(0.35*n)].set(3.00)
            f = f.at[int(0.35*n):int(0.42*n)].set(0.30)
            f = f.at[int(0.42*n):int(0.68*n)].set(2.40)
            f = f.at[int(0.68*n):int(0.85*n)].set(0.20)
        elif pattern_idx == 21:
            # VARIANT 2: Different peak positions
            f = f.at[int(0.04*n):int(0.11*n)].set(0.20)
            f = f.at[int(0.11*n):int(0.33*n)].set(3.20)
            f = f.at[int(0.33*n):int(0.40*n)].set(0.25)
            f = f.at[int(0.40*n):int(0.66*n)].set(2.60)
            f = f.at[int(0.66*n):int(0.83*n)].set(0.15)
        elif pattern_idx == 22:
            # VARIANT 3: More balanced asymmetric
            f = f.at[int(0.06*n):int(0.13*n)].set(0.30)
            f = f.at[int(0.13*n):int(0.34*n)].set(2.90)
            f = f.at[int(0.34*n):int(0.41*n)].set(0.28)
            f = f.at[int(0.41*n):int(0.67*n)].set(2.30)
            f = f.at[int(0.67*n):int(0.84*n)].set(0.22)
        elif pattern_idx == 23:
            # VARIANT 4: Extreme asymmetry
            f = f.at[int(0.04*n):int(0.10*n)].set(0.18)
            f = f.at[int(0.10*n):int(0.32*n)].set(3.50)
            f = f.at[int(0.32*n):int(0.39*n)].set(0.15)
            f = f.at[int(0.39*n):int(0.65*n)].set(2.80)
            f = f.at[int(0.65*n):int(0.82*n)].set(0.12)
        elif pattern_idx == 24:
            # VARIANT 5: Moderate asymmetry
            f = f.at[int(0.06*n):int(0.14*n)].set(0.38)
            f = f.at[int(0.14*n):int(0.33*n)].set(2.70)
            f = f.at[int(0.33*n):int(0.40*n)].set(0.32)
            f = f.at[int(0.40*n):int(0.64*n)].set(2.00)
            f = f.at[int(0.64*n):int(0.81*n)].set(0.26)
        elif pattern_idx == 25:
            # VARIANT 6: Left-skewed asymmetric
            f = f.at[int(0.05*n):int(0.12*n)].set(0.35)
            f = f.at[int(0.12*n):int(0.34*n)].set(3.00)
            f = f.at[int(0.34*n):int(0.41*n)].set(0.28)
            f = f.at[int(0.41*n):int(0.66*n)].set(2.20)
            f = f.at[int(0.66*n):int(0.83*n)].set(0.20)
        elif pattern_idx == 26:
            # VARIANT 7: Right-skewed asymmetric
            f = f.at[int(0.07*n):int(0.15*n)].set(0.28)
            f = f.at[int(0.15*n):int(0.37*n)].set(2.80)
            f = f.at[int(0.37*n):int(0.44*n)].set(0.25)
            f = f.at[int(0.44*n):int(0.70*n)].set(2.40)
            f = f.at[int(0.70*n):int(0.87*n)].set(0.18)
        elif pattern_idx == 27:
            # VARIANT 8: Three very distinct peaks
            f = f.at[int(0.05*n):int(0.11*n)].set(0.22)
            f = f.at[int(0.11*n):int(0.33*n)].set(3.30)
            f = f.at[int(0.33*n):int(0.40*n)].set(0.20)
            f = f.at[int(0.40*n):int(0.66*n)].set(2.70)
            f = f.at[int(0.66*n):int(0.83*n)].set(0.16)
        elif pattern_idx == 28:
            # VARIANT 9: Asymmetric with wider middle peak
            f = f.at[int(0.06*n):int(0.13*n)].set(0.25)
            f = f.at[int(0.13*n):int(0.36*n)].set(2.95)
            f = f.at[int(0.36*n):int(0.43*n)].set(0.27)
            f = f.at[int(0.43*n):int(0.69*n)].set(2.35)
            f = f.at[int(0.69*n):int(0.86*n)].set(0.21)
        elif pattern_idx == 29:
            # VARIANT 10: Asymmetric with narrower side peaks
            f = f.at[int(0.05*n):int(0.11*n)].set(0.20)
            f = f.at[int(0.11*n):int(0.34*n)].set(3.15)
            f = f.at[int(0.34*n):int(0.41*n)].set(0.18)
            f = f.at[int(0.41*n):int(0.67*n)].set(2.55)
            f = f.at[int(0.67*n):int(0.84*n)].set(0.14)
        elif pattern_idx == 30:
            # NEW MUTATED PATTERN: Ultra-high narrow peak with optimized wings
            # Main peak: 3.80 (higher than 3.50), narrower width (0.22n instead of 0.32n)
            # Left wing: 0.20, Right wing: 0.20
            f = f.at[int(0.05*n):int(0.10*n)].set(0.20)
            f = f.at[int(0.10*n):int(0.32*n)].set(3.80)
            f = f.at[int(0.32*n):int(0.39*n)].set(0.20)
            f = f.at[int(0.39*n):int(0.65*n)].set(2.60)
            f = f.at[int(0.65*n):int(0.82*n)].set(0.15)
        else:
            # Default: standard high step - height 1.38
            start = int(0.30 * n)
            end = int(0.70 * n)
            f = f.at[start:end].set(1.38)
        
        return f

    def _create_multi_start(self, num_starts=20):
        """Create diverse TRUE step function initializations."""
        initializations = []
        for i in range(num_starts):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_step_initializer(0, i)
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
        
        for i in range(31):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_step_initializer(n, i)
            initializations.append((init, key))
        
        best_f = None
        best_c2 = 0.0
        
        for idx, (init_f, seed_key) in enumerate(initializations):
            print(f"\n=== Starting optimization from step function {idx + 1}/31 ===")
            schedule1 = optax.warmup_cosine_decay_schedule(
                init_value=0.0,
                peak_value=self.hypers.learning_rate * 1.5,
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
                peak_value=self.hypers.learning_rate * 0.4,
                warmup_steps=500,
                decay_steps=self.hypers.num_steps // 2 - 500,
                end_value=self.hypers.learning_rate * 8e-5,
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
    hypers = OptimizerHyperparameters(best_c2=0.927976)
    optimizer = C2Optimizer(hypers)
    optimized_f, final_c2_val = optimizer.run_optimization()
    f_values_np = np.array(optimized_f)
    return f_values_np, float(final_c2_val), float(-final_c2_val), hypers.num_intervals
# EVOLVE-BLOCK-END
