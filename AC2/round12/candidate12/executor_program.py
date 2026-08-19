# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Hyperparameters for hybrid step-function optimization."""
    num_intervals: int = 600
    learning_rate: float = 0.15
    num_steps: int = 25000
    warmup_steps: int = 2500
    best_c2: float = 0.927976
    stagnation_window: int = 100
    reinit_fraction: float = 0.12
    reinit_std: float = 0.025
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

    def _create_hybrid_step_initializer(self, n, pattern_idx):
        """Create hybrid step functions with additional localized features."""
        f = jnp.zeros(n)
        
        if pattern_idx == 0:
            # Base step + central bump
            left_width = int(0.22 * n)
            right_width = int(0.28 * n)
            base_height = 1.50
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Add central bump
            center_start = int(0.35 * n)
            center_end = int(0.65 * n)
            bump_height = 0.65
            for i in range(center_start, center_end):
                dist = abs(i - int(0.5*n))
                f = f.at[i].set(jnp.maximum(0, base_height + bump_height * (1 - 2*dist/(center_end-center_start))))
        elif pattern_idx == 1:
            # Base step + two side bumps
            left_width = int(0.20 * n)
            right_width = int(0.25 * n)
            base_height = 1.45
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Left bump
            bump1_start = int(0.08 * n)
            bump1_end = int(0.18 * n)
            bump1_height = 0.55
            for i in range(bump1_start, bump1_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump1_height))
            # Right bump
            bump2_start = int(0.72 * n)
            bump2_end = int(0.82 * n)
            bump2_height = 0.55
            for i in range(bump2_start, bump2_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump2_height))
        elif pattern_idx == 2:
            # Base step with asymmetric bumps
            left_width = int(0.24 * n)
            right_width = int(0.26 * n)
            base_height = 1.55
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Larger left bump
            bump1_start = int(0.05 * n)
            bump1_end = int(0.15 * n)
            bump1_height = 0.70
            for i in range(bump1_start, bump1_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump1_height))
            # Smaller right bump
            bump2_start = int(0.75 * n)
            bump2_end = int(0.85 * n)
            bump2_height = 0.45
            for i in range(bump2_start, bump2_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump2_height))
        elif pattern_idx == 3:
            # Multi-step with bumps
            f = jnp.zeros(n)
            f = f.at[int(0.08*n):int(0.20*n)].set(0.85)
            f = f.at[int(0.20*n):int(0.55*n)].set(2.15)
            f = f.at[int(0.55*n):int(0.80*n)].set(0.95)
            # Add central enhancement
            for i in range(int(0.35*n), int(0.65*n)):
                dist = abs(i - int(0.5*n))
                f = f.at[i].set(jnp.maximum(0, f[i] + 0.35 * (1 - 2*dist/(int(0.30*n)))))
        elif pattern_idx == 4:
            # Base step with three bumps
            left_width = int(0.18 * n)
            right_width = int(0.22 * n)
            base_height = 1.40
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Three bumps
            for center, height in [(int(0.12*n), 0.45), (int(0.48*n), 0.60), (int(0.78*n), 0.50)]:
                start = max(0, int(center - int(0.03*n)))
                end = min(n, int(center + int(0.03*n)))
                for i in range(start, end):
                    dist = abs(i - center)
                    f = f.at[i].set(jnp.maximum(0, base_height + height * (1 - dist/0.03/n)))
        elif pattern_idx == 5:
            # High step with narrow central feature
            left_width = int(0.15 * n)
            right_width = int(0.20 * n)
            base_height = 1.70
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Narrow central spike
            spike_center = int(0.5 * n)
            spike_width = int(0.08 * n)
            spike_height = 0.55
            for i in range(spike_center - spike_width//2, spike_center + spike_width//2 + 1):
                if 0 <= i < n:
                    dist = abs(i - spike_center)
                    f = f.at[i].set(jnp.maximum(0, base_height + spike_height * (1 - 2*dist/spike_width)))
        elif pattern_idx == 6:
            # Asymmetric base with offset bump
            left_width = int(0.26 * n)
            right_width = int(0.24 * n)
            base_height = 1.52
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Offset bump to the left
            bump_start = int(0.06 * n)
            bump_end = int(0.16 * n)
            bump_height = 0.62
            for i in range(bump_start, bump_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump_height))
        elif pattern_idx == 7:
            # Base step with plateau enhancement
            left_width = int(0.20 * n)
            right_width = int(0.25 * n)
            base_height = 1.48
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Plateau in middle
            plateau_start = int(0.28 * n)
            plateau_end = int(0.72 * n)
            plateau_height = 0.48
            for i in range(plateau_start, plateau_end):
                f = f.at[i].set(jnp.maximum(0, base_height + plateau_height))
        elif pattern_idx == 8:
            # Multi-step with side enhancements
            f = jnp.zeros(n)
            f = f.at[int(0.06*n):int(0.18*n)].set(0.78)
            f = f.at[int(0.18*n):int(0.48*n)].set(2.38)
            f = f.at[int(0.48*n):int(0.82*n)].set(1.08)
            # Side enhancements
            for center, height, width in [(int(0.12*n), 0.38, int(0.04*n)), (int(0.78*n), 0.38, int(0.04*n))]:
                start = max(0, int(center - width//2))
                end = min(n, int(center + width//2))
                for i in range(start, end):
                    dist = abs(i - center)
                    f = f.at[i].set(jnp.maximum(0, f[i] + height * (1 - dist/(width/2))))
        elif pattern_idx == 9:
            # High step with dual bumps
            left_width = int(0.16 * n)
            right_width = int(0.21 * n)
            base_height = 1.68
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Two bumps
            for center, height, width in [(int(0.18*n), 0.52, int(0.06*n)), (int(0.72*n), 0.52, int(0.06*n))]:
                start = max(0, int(center - width//2))
                end = min(n, int(center + width//2))
                for i in range(start, end):
                    dist = abs(i - center)
                    f = f.at[i].set(jnp.maximum(0, base_height + height * (1 - dist/(width/2))))
        elif pattern_idx == 10:
            # Base with central ridge
            left_width = int(0.22 * n)
            right_width = int(0.28 * n)
            base_height = 1.53
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Central ridge
            center_start = int(0.32 * n)
            center_end = int(0.68 * n)
            ridge_height = 0.58
            for i in range(center_start, center_end):
                dist = abs(i - int(0.5*n))
                f = f.at[i].set(jnp.maximum(0, base_height + ridge_height * (1 - 2*dist/(center_end-center_start))))
        elif pattern_idx == 11:
            # Asymmetric multi-step with bump
            f = jnp.zeros(n)
            f = f.at[int(0.08*n):int(0.20*n)].set(0.82)
            f = f.at[int(0.20*n):int(0.52*n)].set(2.42)
            f = f.at[int(0.52*n):int(0.82*n)].set(1.02)
            # Bump on left side
            bump_start = int(0.10*n)
            bump_end = int(0.20*n)
            bump_height = 0.42
            for i in range(bump_start, bump_end):
                f = f.at[i].set(jnp.maximum(0, f[i] + bump_height))
        elif pattern_idx == 12:
            # High step with asymmetric bumps
            left_width = int(0.17 * n)
            right_width = int(0.23 * n)
            base_height = 1.65
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Larger left bump
            bump1_start = int(0.06*n)
            bump1_end = int(0.16*n)
            bump1_height = 0.68
            for i in range(bump1_start, bump1_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump1_height))
            # Smaller right bump
            bump2_start = int(0.74*n)
            bump2_end = int(0.84*n)
            bump2_height = 0.42
            for i in range(bump2_start, bump2_end):
                f = f.at[i].set(jnp.maximum(0, base_height + bump2_height))
        elif pattern_idx == 13:
            # Base step with three small bumps
            left_width = int(0.21 * n)
            right_width = int(0.27 * n)
            base_height = 1.50
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Three small bumps
            for center, height, width in [(int(0.10*n), 0.35, int(0.03*n)), (int(0.45*n), 0.45, int(0.04*n)), (int(0.80*n), 0.35, int(0.03*n))]:
                start = max(0, int(center - width//2))
                end = min(n, int(center + width//2))
                for i in range(start, end):
                    dist = abs(i - center)
                    f = f.at[i].set(jnp.maximum(0, base_height + height * (1 - dist/(width/2))))
        elif pattern_idx == 14:
            # High step with central plateau bump
            left_width = int(0.18 * n)
            right_width = int(0.22 * n)
            base_height = 1.62
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Central plateau
            plateau_start = int(0.30*n)
            plateau_end = int(0.70*n)
            plateau_height = 0.52
            for i in range(plateau_start, plateau_end):
                f = f.at[i].set(jnp.maximum(0, base_height + plateau_height))
        elif pattern_idx == 15:
            # Multi-step with asymmetric enhancement
            f = jnp.zeros(n)
            f = f.at[int(0.07*n):int(0.19*n)].set(0.80)
            f = f.at[int(0.19*n):int(0.49*n)].set(2.40)
            f = f.at[int(0.49*n):int(0.81*n)].set(1.05)
            # Asymmetric enhancement
            for i in range(int(0.12*n), int(0.22*n)):
                f = f.at[i].set(jnp.maximum(0, f[i] + 0.40))
        elif pattern_idx == 16:
            # Base with dual plateaus
            left_width = int(0.20 * n)
            right_width = int(0.25 * n)
            base_height = 1.46
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Two plateaus
            for center, height, width in [(int(0.14*n), 0.46, int(0.05*n)), (int(0.76*n), 0.46, int(0.05*n))]:
                start = max(0, int(center - width//2))
                end = min(n, int(center + width//2))
                for i in range(start, end):
                    f = f.at[i].set(jnp.maximum(0, base_height + height))
        elif pattern_idx == 17:
            # High step with central spike and wings
            left_width = int(0.16 * n)
            right_width = int(0.21 * n)
            base_height = 1.72
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Central spike
            spike_center = int(0.5 * n)
            spike_width = int(0.06 * n)
            spike_height = 0.62
            for i in range(spike_center - spike_width//2, spike_center + spike_width//2 + 1):
                if 0 <= i < n:
                    dist = abs(i - spike_center)
                    f = f.at[i].set(jnp.maximum(0, base_height + spike_height * (1 - 2*dist/spike_width)))
        elif pattern_idx == 18:
            # Asymmetric base with offset plateau
            left_width = int(0.25 * n)
            right_width = int(0.23 * n)
            base_height = 1.54
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Offset plateau
            plateau_start = int(0.08 * n)
            plateau_end = int(0.18 * n)
            plateau_height = 0.54
            for i in range(plateau_start, plateau_end):
                f = f.at[i].set(jnp.maximum(0, base_height + plateau_height))
        elif pattern_idx == 19:
            # Base step with four small bumps
            left_width = int(0.19 * n)
            right_width = int(0.24 * n)
            base_height = 1.48
            for i in range(left_width):
                f = f.at[i].set(base_height)
            for i in range(n - left_width, n - right_width):
                f = f.at[i].set(base_height)
            # Four small bumps
            for center, height, width in [(int(0.08*n), 0.32, int(0.025*n)), (int(0.25*n), 0.40, int(0.03*n)), (int(0.65*n), 0.40, int(0.03*n)), (int(0.82*n), 0.32, int(0.025*n))]:
                start = max(0, int(center - width//2))
                end = min(n, int(center + width//2))
                for i in range(start, end):
                    dist = abs(i - center)
                    f = f.at[i].set(jnp.maximum(0, base_height + height * (1 - dist/(width/2))))
        else:
            # Default: base step with central bump
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

    def _create_multi_start(self, num_starts=20):
        """Create diverse hybrid step initializations."""
        initializations = []
        for i in range(num_starts):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_hybrid_step_initializer(0, i)
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
        initializations = []
        n = self.hypers.num_intervals
        
        for i in range(30):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_hybrid_step_initializer(n, i)
            initializations.append((init, key))
        
        best_f = None
        best_c2 = 0.0
        
        for idx, (init_f, seed_key) in enumerate(initializations):
            print(f"\n=== Starting optimization from hybrid step pattern {idx + 1}/30 ===")
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
            
            print(f"\n=== Phase 2 fine-tuning for hybrid step pattern {idx + 1} ===")
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
