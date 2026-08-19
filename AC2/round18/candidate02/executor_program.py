# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Hyperparameters for high-resolution step-function optimization."""
    num_intervals: int = 600
    learning_rate: float = 0.15
    num_steps: int = 30000
    warmup_steps: int = 3000
    best_c2: float = 0.8962799441554086
    stagnation_window: int = 100
    reinit_fraction: float = 0.12
    reinit_std: float = 0.025
    reinit_interval: int = 200


class C2Optimizer:
    def __init__(self, hypers: OptimizerHyperparameters):
        self.hypers = hypers
        self.best_f = jnp.zeros(hypers.num_intervals)
        self.best_c2 = hypers.best_c2

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        f_non_negative = jax.nn.softplus(f_values)
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real

        num_conv_points = len(convolution)
        h = 1.0 / num_conv_points
        y_points = jnp.concatenate([jnp.array([0.0]), convolution, jnp.array([0.0])])
        y1, y2 = y_points[:-1], y_points[1:]
        l2_norm_squared = jnp.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))

        norm_1 = jnp.sum(jnp.abs(convolution)) / len(convolution)
        norm_inf = jnp.max(jnp.abs(convolution))
        denominator = norm_1 * norm_inf
        c2_ratio = l2_norm_squared / denominator
        return -c2_ratio

    def _create_step_initializer(self, n, pattern_idx):
        """Create TRUE piecewise-constant step functions - high-resolution patterns."""
        f = jnp.zeros(n)
        
        if pattern_idx == 0:
            start = int(0.25 * n)
            end = int(0.75 * n)
            f = f.at[start:end].set(1.40)
        elif pattern_idx == 1:
            start = int(0.27 * n)
            end = int(0.73 * n)
            f = f.at[start:end].set(1.50)
        elif pattern_idx == 2:
            start = int(0.30 * n)
            end = int(0.70 * n)
            f = f.at[start:end].set(1.60)
        elif pattern_idx == 3:
            f = f.at[int(0.15*n):int(0.25*n)].set(0.90)
            f = f.at[int(0.25*n):int(0.75*n)].set(1.90)
            f = f.at[int(0.75*n):int(0.85*n)].set(0.90)
        elif pattern_idx == 4:
            f = f.at[int(0.11*n):int(0.21*n)].set(1.10)
            f = f.at[int(0.21*n):int(0.49*n)].set(2.30)
            f = f.at[int(0.49*n):int(0.71*n)].set(1.40)
        elif pattern_idx == 5:
            f = f.at[int(0.22*n):int(0.38*n)].set(1.50)
            f = f.at[int(0.52*n):int(0.82*n)].set(1.50)
        elif pattern_idx == 6:
            f = f.at[int(0.06*n):int(0.20*n)].set(0.70)
            f = f.at[int(0.20*n):int(0.34*n)].set(1.30)
            f = f.at[int(0.34*n):int(0.64*n)].set(1.70)
            f = f.at[int(0.64*n):int(0.94*n)].set(1.00)
        elif pattern_idx == 7:
            f = f.at[int(0.12*n):int(0.18*n)].set(0.60)
            f = f.at[int(0.18*n):int(0.28*n)].set(1.20)
            f = f.at[int(0.28*n):int(0.72*n)].set(2.20)
            f = f.at[int(0.72*n):int(0.82*n)].set(1.20)
            f = f.at[int(0.82*n):int(0.88*n)].set(0.60)
        elif pattern_idx == 8:
            f = f.at[int(0.06*n):int(0.24*n)].set(0.60)
            f = f.at[int(0.24*n):int(0.44*n)].set(1.00)
            f = f.at[int(0.44*n):int(0.64*n)].set(1.50)
            f = f.at[int(0.64*n):int(0.94*n)].set(1.20)
        elif pattern_idx == 9:
            f = f.at[int(0.08*n):int(0.20*n)].set(0.80)
            f = f.at[int(0.20*n):int(0.35*n)].set(1.60)
            f = f.at[int(0.35*n):int(0.55*n)].set(2.00)
            f = f.at[int(0.55*n):int(0.75*n)].set(1.40)
            f = f.at[int(0.75*n):int(0.90*n)].set(0.90)
        elif pattern_idx == 10:
            f = f.at[int(0.10*n):int(0.90*n)].set(1.20)
            f = f.at[int(0.35*n):int(0.65*n)].set(2.80)
        elif pattern_idx == 11:
            f = f.at[int(0.15*n):int(0.30*n)].set(1.50)
            f = f.at[int(0.30*n):int(0.40*n)].set(2.50)
            f = f.at[int(0.40*n):int(0.50*n)].set(1.50)
            f = f.at[int(0.50*n):int(0.60*n)].set(2.50)
            f = f.at[int(0.60*n):int(0.70*n)].set(1.50)
        else:
            left_width = int(0.22 * n)
            right_width = int(0.28 * n)
            base_height = 1.50
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            center_start = int(0.35 * n)
            center_end = int(0.65 * n)
            bump_height = 0.65
            for i in range(center_start, center_end):
                dist = abs(i - int(0.5*n))
                f = f.at[i].set(jnp.maximum(0, base_height + bump_height * (1 - 2*dist/(center_end-center_start))))
        
        return f

    def _create_targeted_mutations(self, n, base_f, mutation_type, seed_idx):
        """Create targeted mutations based on mutation type."""
        f = base_f.copy()
        
        if mutation_type == 'height_increase':
            # Increase all non-zero values by 5-10%
            mask = f > 0
            f = f.at[mask].set(f[mask] * (1.05 + 0.05 * ((seed_idx % 5) - 2)))
        
        elif mutation_type == 'height_decrease':
            # Decrease all non-zero values by 5-10%
            mask = f > 0
            f = f.at[mask].set(f[mask] * (0.95 - 0.05 * ((seed_idx % 5) - 2)))
        
        elif mutation_type == 'narrow_peak':
            # Narrow the high peaks
            mask = f > 1.5
            if jnp.any(mask):
                indices = jnp.where(mask)[0]
                for idx in indices:
                    start = max(0, idx - 5)
                    end = min(n-1, idx + 5)
                    f = f.at[start:end].set(f[idx])
        
        elif mutation_type == 'wide_base':
            # Widen the base regions
            mask = (f > 0) & (f < 1.5)
            if jnp.any(mask):
                indices = jnp.where(mask)[0]
                for idx in indices:
                    start = max(0, idx - 10)
                    end = min(n-1, idx + 10)
                    f = f.at[start:end].set(f[idx])
        
        elif mutation_type == 'add_peak':
            # Add a new peak in the center
            center = int(0.5 * n)
            peak_height = 2.0 + 0.5 * ((seed_idx % 5) - 2)
            peak_width = 50 + 20 * ((seed_idx % 5) - 2)
            start = max(0, center - peak_width // 2)
            end = min(n-1, center + peak_width // 2)
            f = f.at[start:end].set(jnp.maximum(0.001, f[start:end] + peak_height))
        
        elif mutation_type == 'asymmetric_wings':
            # Add asymmetric wings
            left_start = int(0.05 * n)
            left_end = int(0.15 * n)
            right_start = int(0.85 * n)
            right_end = int(0.95 * n)
            wing_height = 0.5 + 0.2 * ((seed_idx % 5) - 2)
            f = f.at[left_start:left_end].set(jnp.maximum(0.001, f[left_start:left_end] + wing_height))
            f = f.at[right_start:right_end].set(jnp.maximum(0.001, f[right_start:right_end] + wing_height))
        
        elif mutation_type == 'flatten_center':
            # Flatten the center region
            center_start = int(0.35 * n)
            center_end = int(0.65 * n)
            f = f.at[center_start:center_end].set(jnp.maximum(0.001, f[center_start:center_end] * 0.7))
        
        return jnp.maximum(f, 0.001)

    def _create_multi_start(self, num_starts=80):
        """Create diverse initializations across different step pattern families."""
        initializations = []
        
        # Standard step patterns (primary)
        for i in range(40):
            init = self._create_step_initializer(0, i % 12)
            initializations.append((init, jax.random.PRNGKey(42 + i * 100), 'step'))
        
        # Targeted mutations of best patterns
        mutation_types = ['height_increase', 'height_decrease', 'narrow_peak', 'wide_base', 
                         'add_peak', 'asymmetric_wings', 'flatten_center']
        for i in range(20):
            base = self._create_step_initializer(0, 10)  # Use pattern 10 as base
            mutation_type = mutation_types[i % 7]
            init = self._create_targeted_mutations(0, base, mutation_type, i)
            initializations.append((init, jax.random.PRNGKey(42 + 40 + i * 100), 'mutation'))
        
        return initializations

    def _local_reinitialization(self, f_values: jnp.ndarray, key) -> jnp.ndarray:
        n = len(f_values)
        num_reinit = int(self.hypers.reinit_fraction * n)
        key, subkey = jax.random.split(key)
        reinit_indices = jax.random.permutation(subkey, n)[:num_reinit]
        perturbation = jax.random.normal(subkey, f_values.shape) * self.hypers.reinit_std
        f_new = f_values.at[reinit_indices].set(f_values[reinit_indices] + perturbation[reinit_indices])
        f_new = jax.nn.softplus(f_new)
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
        initializations = self._create_multi_start(num_starts=80)
        n = self.hypers.num_intervals
        
        best_f = jnp.zeros(n)
        best_c2 = 0.0
        
        for idx, (init_f, seed_key, family_name) in enumerate(initializations):
            print(f"\n=== Starting {family_name} variant {idx + 1}/{len(initializations)} ===")
            schedule = optax.warmup_cosine_decay_schedule(
                init_value=0.0,
                peak_value=self.hypers.learning_rate * 1.5,
                warmup_steps=self.hypers.warmup_steps,
                decay_steps=self.hypers.num_steps // 2 - self.hypers.warmup_steps,
                end_value=self.hypers.learning_rate * 0.1,
            )
            optimizer = optax.adam(learning_rate=schedule, eps=1e-8)
            key = jax.random.PRNGKey(42 + idx * 100)
            f_values = init_f + 0.05 * jax.random.normal(key, init_f.shape)
            opt_state = optimizer.init(f_values)
            reinit_key = jax.random.PRNGKey(42 + idx * 1000)
            c2_history = []
            
            train_step_jit = jax.jit(lambda fv, os: self._train_step(fv, os, optimizer))
            for step in range(self.hypers.num_steps // 2):
                f_values, opt_state, loss, grads = train_step_jit(f_values, opt_state)
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
            
            # Phase 2 fine-tuning
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
            
            print(f"\n=== Phase 2 fine-tuning for variant {idx + 1} ===")
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

        return jax.nn.softplus(best_f), best_c2 if best_f is not None else 0.0


def run():
    hypers = OptimizerHyperparameters(best_c2=0.8962799441554086)
    optimizer = C2Optimizer(hypers)
    optimized_f, final_c2_val = optimizer.run_optimization()
    f_values_np = np.array(optimized_f)
    return f_values_np, float(final_c2_val), float(-final_c2_val), hypers.num_intervals
# EVOLVE-BLOCK-END
