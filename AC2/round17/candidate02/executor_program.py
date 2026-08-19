# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Hyperparameters for hybrid step-function and architecture exploration."""
    num_intervals: int = 600
    learning_rate: float = 0.15
    num_steps: int = 25000
    warmup_steps: int = 2500
    best_c2: float = 0.913137
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

    def _create_refined_step_initializer(self, n, pattern_idx, mutation_type='base'):
        """Create refined step functions with targeted mutations."""
        f = jnp.zeros(n)
        
        if pattern_idx == 0:
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
            
            if mutation_type == 'bump_height_increase':
                bump_height = 0.73
                for i in range(center_start, center_end):
                    dist = abs(i - int(0.5*n))
                    f = f.at[i].set(jnp.maximum(0, base_height + bump_height * (1 - 2*dist/(center_end-center_start))))
            elif mutation_type == 'bump_height_decrease':
                bump_height = 0.60
                for i in range(center_start, center_end):
                    dist = abs(i - int(0.5*n))
                    f = f.at[i].set(jnp.maximum(0, base_height + bump_height * (1 - 2*dist/(center_end-center_start))))
        
        elif pattern_idx == 1:
            left_width = int(0.20 * n)
            right_width = int(0.25 * n)
            base_height = 1.45
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            bump1_start = int(0.08 * n)
            bump1_end = int(0.18 * n)
            bump1_height = 0.55
            for i in range(bump1_start, bump1_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump1_height))
            bump2_start = int(0.72 * n)
            bump2_end = int(0.82 * n)
            bump2_height = 0.55
            for i in range(bump2_start, bump2_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump2_height))
            
            if mutation_type == 'bump_height_increase':
                bump1_height = 0.63
                bump2_height = 0.63
                for i in range(bump1_start, bump1_end):
                    f = f.at[i].set(jnp.maximum(0, base_height + bump1_height))
                for i in range(bump2_start, bump2_end):
                    f = f.at[i].set(jnp.maximum(0, base_height + bump2_height))
        
        elif pattern_idx == 2:
            left_width = int(0.24 * n)
            right_width = int(0.26 * n)
            base_height = 1.55
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            bump1_start = int(0.05 * n)
            bump1_end = int(0.15 * n)
            bump1_height = 0.70
            for i in range(bump1_start, bump1_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump1_height))
            bump2_start = int(0.75 * n)
            bump2_end = int(0.85 * n)
            bump2_height = 0.45
            for i in range(bump2_start, bump2_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump2_height))
            
            if mutation_type == 'bump_height_increase':
                bump1_height = 0.78
                bump2_height = 0.53
                for i in range(bump1_start, bump1_end):
                    f = f.at[i].set(jnp.maximum(0, base_height + bump1_height))
                for i in range(bump2_start, bump2_end):
                    f = f.at[i].set(jnp.maximum(0, base_height + bump2_height))
        
        elif pattern_idx == 3:
            f = jnp.zeros(n)
            f = f.at[int(0.08*n):int(0.20*n)].set(0.85)
            f = f.at[int(0.20*n):int(0.55*n)].set(2.15)
            f = f.at[int(0.55*n):int(0.80*n)].set(0.95)
            for i in range(int(0.35*n), int(0.65*n)):
                dist = abs(i - int(0.5*n))
                f = f.at[i].set(jnp.maximum(0, f[i] + 0.35 * (1 - 2*dist/(int(0.30*n)))))
            
            if mutation_type == 'bump_height_increase':
                for i in range(int(0.35*n), int(0.65*n)):
                    dist = abs(i - int(0.5*n))
                    f = f.at[i].set(jnp.maximum(0, f[i] + 0.40 * (1 - 2*dist/(int(0.30*n)))))
        
        elif pattern_idx == 4:
            left_width = int(0.18 * n)
            right_width = int(0.22 * n)
            base_height = 1.40
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            for center, height, width in [(int(0.12*n), 0.45, int(0.03*n)), (int(0.48*n), 0.60, int(0.03*n)), (int(0.78*n), 0.50, int(0.03*n))]:
                start = max(0, int(center - width//2))
                end = min(n, int(center + width//2))
                for i in range(start, end):
                    dist = abs(i - center)
                    f = f.at[i].set(jnp.maximum(0, base_height + height * (1 - dist/0.03/n)))
            
            if mutation_type == 'bump_height_increase':
                for center, height, width in [(int(0.12*n), 0.53, int(0.03*n)), (int(0.48*n), 0.68, int(0.03*n)), (int(0.78*n), 0.58, int(0.03*n))]:
                    start = max(0, int(center - width//2))
                    end = min(n, int(center + width//2))
                    for i in range(start, end):
                        dist = abs(i - center)
                        f = f.at[i].set(jnp.maximum(0, base_height + height * (1 - dist/0.03/n)))
        
        else:
            left_width = int(0.22 * n)
            right_width = int(0.28 * n)
            base_height = 1.55
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            center_start = int(0.35 * n)
            center_end = int(0.65 * n)
            bump_height = 0.60
            for i in range(center_start, center_end):
                dist = abs(i - int(0.5*n))
                f = f.at[i].set(jnp.maximum(0, base_height + bump_height * (1 - 2*dist/(center_end-center_start))))
        
        return f

    def _create_gaussian_mixture(self, n, seed_idx):
        """Create Gaussian mixture function."""
        f = jnp.zeros(n)
        key = jax.random.PRNGKey(42 + seed_idx * 100)
        
        num_gaussians = 3 + (seed_idx % 3)
        mus = jax.random.uniform(key, (num_gaussians,), minval=-2.0, maxval=2.0)
        sigmas = jax.random.uniform(key, (num_gaussians,), minval=0.3, maxval=0.8)
        weights = jax.random.uniform(key, (num_gaussians,), minval=0.1, maxval=0.5)
        weights = weights / jnp.sum(weights)
        
        x = jnp.arange(n)
        for i in range(num_gaussians):
            gaussian = weights[i] * jnp.exp(-((x - mus[i])**2) / (2 * sigmas[i]**2))
            f = f + gaussian
        
        return jnp.maximum(f, 0.001)

    def _create_multi_level_improved(self, n, seed_idx):
        """Create improved multi-level step function."""
        f = jnp.zeros(n)
        
        levels = [
            0.45 + 0.05 * (seed_idx % 5),
            1.15 + 0.10 * ((seed_idx + 1) % 5),
            1.95 + 0.15 * ((seed_idx + 2) % 5),
            1.15 + 0.10 * ((seed_idx + 3) % 5),
            0.45 + 0.05 * ((seed_idx + 4) % 5),
        ]
        
        positions = jnp.array([0.08, 0.25, 0.45, 0.65, 0.85])
        
        for i in range(len(positions) - 1):
            start = int(positions[i] * n)
            end = int(positions[i+1] * n)
            f = f.at[start:end].set(levels[i])
        
        return jnp.maximum(f, 0.001)

    def _create_oscillatory_decay(self, n, seed_idx):
        """Create oscillatory decay function."""
        f = jnp.zeros(n)
        key = jax.random.PRNGKey(42 + seed_idx * 100)
        
        alpha = 0.25 + 0.1 * ((seed_idx % 5) / 5.0)
        beta = 3.0 + 1.0 * ((seed_idx % 5) / 5.0)
        gamma = 0.7 + 0.2 * ((seed_idx % 5) / 5.0)
        
        x = jnp.arange(n)
        f = (1 + alpha * jnp.cos(beta * x)) * jnp.exp(-gamma * jnp.abs(x))
        f = jnp.maximum(f, 0.001)
        
        return f

    def _create_multi_start(self, num_starts=60):
        """Create diverse initializations across different families."""
        initializations = []
        
        for i in range(20):
            mutation = ['bump_height_increase', 'bump_height_decrease', 'base'][i % 3]
            init = self._create_refined_step_initializer(0, i, mutation)
            initializations.append((init, jax.random.PRNGKey(42 + i * 100)))
        
        for i in range(20):
            init = self._create_gaussian_mixture(0, i)
            initializations.append((init, jax.random.PRNGKey(42 + 20 + i * 100)))
        
        for i in range(10):
            init = self._create_multi_level_improved(0, i)
            initializations.append((init, jax.random.PRNGKey(42 + 40 + i * 100)))
        
        for i in range(10):
            init = self._create_oscillatory_decay(0, i)
            initializations.append((init, jax.random.PRNGKey(42 + 50 + i * 100)))
        
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
        initializations = self._create_multi_start(num_starts=60)
        n = self.hypers.num_intervals
        
        best_f = jnp.zeros(n)
        best_c2 = 0.0
        
        for idx, (init_f, seed_key) in enumerate(initializations):
            family_name = ['step', 'step', 'step', 'gaussian', 'gaussian', 'gaussian', 
                          'multi-level', 'multi-level', 'multi-level', 'oscillatory', 'oscillatory', 'oscillatory'][idx % 12]
            
            print(f"\n=== Starting optimization from {family_name} variant {idx + 1}/60 ===")
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

        return jax.nn.relu(best_f), best_c2 if best_f is not None else 0.0


def run():
    hypers = OptimizerHyperparameters(best_c2=0.913137)
    optimizer = C2Optimizer(hypers)
    optimized_f, final_c2_val = optimizer.run_optimization()
    f_values_np = np.array(optimized_f)
    return f_values_np, float(final_c2_val), float(-final_c2_val), hypers.num_intervals
# EVOLVE-BLOCK-END
