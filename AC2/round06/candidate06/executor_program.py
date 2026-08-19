# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Slightly increased steps and learning rate."""
    num_intervals: int = 300
    learning_rate: float = 0.135
    num_steps: int = 38000
    warmup_steps: int = 3800
    best_c2: float = 0.0
    stagnation_window: int = 100
    reinit_fraction: float = 0.14
    reinit_std: float = 0.032
    reinit_interval: int = 155


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

    def _create_optimized_step(self, n, pattern_idx):
        """Optimized step patterns."""
        f = jnp.zeros(n)
        midpoint = n // 2
        
        if pattern_idx == 0:
            # Two blocks - key working pattern
            f = f.at[100:200].set(1.0)
            f = f.at[240:300].set(1.0)
            
        elif pattern_idx == 1:
            # Tall central - slightly adjusted
            f = f.at[midpoint-72:midpoint+72].set(1.42)
            
        elif pattern_idx == 2:
            # Offset tapered
            f = f.at[midpoint-68:midpoint+68].set(1.35)
            f = f.at[midpoint:midpoint+32].mul(0.81)
            
        elif pattern_idx == 3:
            # Three clusters
            f = f.at[118:182].set(1.0)
            f = f.at[185:225].set(1.0)
            f = f.at[230:288].set(1.0)
            
        elif pattern_idx == 4:
            # Overlapping tall
            f = f.at[midpoint-52:midpoint+52].set(1.33)
            f = f.at[midpoint-57:midpoint+57].set(1.53)
            
        elif pattern_idx == 5:
            # Central tall
            f = f.at[midpoint-47:midpoint+47].set(1.57)
            
        elif pattern_idx == 6:
            # Wide with center
            f = f.at[98:252].set(1.28)
            f = f.at[midpoint-37:midpoint+37].set(1.54)
            
        elif pattern_idx == 7:
            # Block with spike
            f = f.at[148:252].set(1.37)
            f = f.at[midpoint-4:midpoint+4].set(1.61)
            
        elif pattern_idx == 8:
            # Gap asymmetric
            f = f.at[128:168].set(0.86)
            f = f.at[197:237].set(1.67)
            
        else:
            f = f.at[midpoint-63:midpoint+63].set(1.27)
        
        return f

    def _create_multi_start(self, num_starts=9):
        initializations = []
        for i in range(num_starts):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_optimized_step(self.hypers.num_intervals, i)
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
        initializations = self._create_multi_start(num_starts=9)
        best_f = None
        best_c2 = 0.0
        
        for idx, (init_f, seed_key) in enumerate(initializations):
            print(f"\n=== Starting optimized {idx + 1}/9 ===")
            schedule1 = optax.warmup_cosine_decay_schedule(
                init_value=0.0,
                peak_value=self.hypers.learning_rate * 1.4,
                warmup_steps=self.hypers.warmup_steps,
                decay_steps=self.hypers.num_steps // 2 - self.hypers.warmup_steps,
                end_value=self.hypers.learning_rate * 0.15,
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
            
            print(f"\n=== Phase 2 fine-tuning for optimized {idx + 1} ===")
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
