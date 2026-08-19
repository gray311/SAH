# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Hyperparameters for enhanced step function optimization."""
    num_intervals: int = 400
    learning_rate: float = 0.25
    num_steps: int = 30000
    warmup_steps: int = 3000
    best_c2: float = 0.0
    stagnation_window: int = 100
    reinit_fraction: float = 0.18
    reinit_std: float = 0.04
    reinit_interval: int = 150


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

    def _create_enhanced_initializer(self, key, pattern_idx):
        """Create enhanced step function patterns with more diversity."""
        n = self.hypers.num_intervals
        midpoint = int(n / 2)
        
        f = jnp.zeros(n)
        
        if pattern_idx == 0:
            # Original baseline
            f = f.at[100:200].set(1.0)
            f = f.at[240:300].set(1.0)
        elif pattern_idx == 1:
            # Enhanced 3-level centered
            f = f.at[midpoint-75:midpoint+75].set(1.45)
            f = f.at[midpoint-95:midpoint-75].set(1.22)
            f = f.at[midpoint+75:midpoint+95].set(1.18)
        elif pattern_idx == 2:
            # Asymmetric 3-level with gradient
            f = f.at[midpoint-80:midpoint-60].set(1.32)
            f = f.at[midpoint-60:midpoint+60].set(1.58)
            f = f.at[midpoint+60:midpoint+80].set(1.28)
        elif pattern_idx == 3:
            # Multi-plateau enhanced
            f = f.at[95:135].set(1.12)
            f = f.at[135:175].set(1.52)
            f = f.at[175:215].set(1.15)
            f = f.at[215:255].set(1.02)
        elif pattern_idx == 4:
            # Peak with enhanced shoulders
            f = f.at[midpoint-68:midpoint+68].set(1.62)
            f = f.at[midpoint-88:midpoint-68].set(1.32)
            f = f.at[midpoint+68:midpoint+88].set(1.28)
        elif pattern_idx == 5:
            # Two-step with optimized spacing
            f = f.at[105:145].set(1.2)
            f = f.at[145:185].set(1.55)
            f = f.at[185:225].set(1.15)
        elif pattern_idx == 6:
            # Staggered multi-level
            f = f.at[midpoint-72:midpoint-48].set(1.2)
            f = f.at[midpoint-48:midpoint+48].set(1.6)
            f = f.at[midpoint+48:midpoint+72].set(1.25)
        elif pattern_idx == 7:
            # Low-high-staircase enhanced
            f = f.at[110:150].set(0.95)
            f = f.at[150:190].set(1.52)
            f = f.at[190:230].set(1.48)
        elif pattern_idx == 8:
            # Symmetric multi-level enhanced
            f = f.at[midpoint-62:midpoint-38].set(1.15)
            f = f.at[midpoint-38:midpoint+38].set(1.52)
            f = f.at[midpoint+38:midpoint+62].set(1.15)
        elif pattern_idx == 9:
            # Wide narrow pattern
            f = f.at[midpoint-85:midpoint-55].set(1.18)
            f = f.at[midpoint-55:midpoint+55].set(1.58)
            f = f.at[midpoint+55:midpoint+85].set(1.18)
        elif pattern_idx == 10:
            # Offset peaks
            f = f.at[120:160].set(1.25)
            f = f.at[160:200].set(1.62)
            f = f.at[200:240].set(1.22)
        else:
            # Default enhanced
            f = f.at[midpoint-65:midpoint+65].set(1.42)
            f = f.at[midpoint-85:midpoint-65].set(1.2)
            f = f.at[midpoint+65:midpoint+85].set(1.2)
        
        return f

    def _create_multi_start(self, num_starts=12):
        initializations = []
        for i in range(num_starts):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_enhanced_initializer(key, i)
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
        initializations = self._create_multi_start(num_starts=12)
        best_f = None
        best_c2 = 0.0
        
        for idx, (init_f, seed_key) in enumerate(initializations):
            print(f"\n=== Starting optimization from profile {idx + 1}/12 (Enhanced Steps) ===")
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
            
            print(f"\n=== Phase 2 fine-tuning for profile {idx + 1} ===")
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
