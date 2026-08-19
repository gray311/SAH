# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class OptimizerHyperparameters:
    """Hyperparameters for the optimization process with hybrid optimization settings."""

    num_intervals: int = 300  # Finer discretization for better function representation
    learning_rate: float = 0.13  # Optimal learning rate for this configuration
    num_steps: int = 40000
    warmup_steps: int = 4000
    best_c2: float = 0.0
    # Hybrid optimization parameters - optimized for C₂ landscape exploration
    stagnation_window: int = 100  # Fast detection of local optima
    reinit_fraction: float = 0.12  # 12% of intervals reinitialized per reinit
    reinit_std: float = 0.02  # Conservative perturbation for stability
    reinit_interval: int = 200  # More frequent reinit checks for better escape


class C2Optimizer:
    """
    Optimizes a discretized function to find a lower bound for the C2 constant.
    Uses Adam optimizer with adaptive learning rate schedule and hybrid exploration.
    """

    def __init__(self, hypers: OptimizerHyperparameters):
        self.hypers = hypers
        self.best_f = None
        self.best_c2 = hypers.best_c2
        self.stagnation_history = {}  # Track gradient norms per start

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        """Computes the objective function using the unitless norm calculation."""
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

    def _create_initializer(self, key, pattern_idx):
        """Create step-function-like initialization with different patterns."""
        n = self.hypers.num_intervals
        f = jnp.zeros(n)
        
        if pattern_idx == 0:
            start = int(0.25 * n)
            end = int(0.75 * n)
            h = 1.0
        elif pattern_idx == 1:
            start = int(0.35 * n)
            end = int(0.65 * n)
            h = 1.2
        elif pattern_idx == 2:
            f = f.at[int(0.2*n):int(0.3*n)].set(1.0)
            f = f.at[int(0.4*n):int(0.6*n)].set(2.0)
            f = f.at[int(0.7*n):int(0.8*n)].set(1.5)
            h = 1.0
        elif pattern_idx == 3:
            start = int(0.25 * n)
            end = int(0.75 * n)
            h = 1.1
        elif pattern_idx == 4:
            # Narrower step function in the middle
            start = int(0.3*n)
            end = int(0.7*n)
            h = 1.3
        elif pattern_idx == 5:
            # Asymmetric step function - wider on left
            start = int(0.15 * n)
            end = int(0.55 * n)
            h = 1.15
        elif pattern_idx == 6:
            # Wider step function
            start = int(0.2*n)
            end = int(0.8*n)
            h = 0.9
        elif pattern_idx == 7:
            # Multi-level: three segments with varying heights
            f = f.at[int(0.1*n):int(0.25*n)].set(1.2)
            f = f.at[int(0.25*n):int(0.6*n)].set(1.8)
            f = f.at[int(0.6*n):int(0.85*n)].set(1.1)
            h = 1.0
        elif pattern_idx == 8:
            # Two-step function with gap
            f = f.at[int(0.1*n):int(0.35*n)].set(1.4)
            f = f.at[int(0.55*n):int(0.9*n)].set(0.85)
            h = 1.0
        else:
            start = int(0.25 * n)
            end = int(0.75 * n)
            h = 1.0
        
        if pattern_idx == 2:
            f = f.at[int(0.2*n):int(0.3*n)].set(1.0)
            f = f.at[int(0.4*n):int(0.6*n)].set(2.0)
            f = f.at[int(0.7*n):int(0.8*n)].set(1.5)
        elif pattern_idx == 7:
            f = f.at[int(0.1*n):int(0.25*n)].set(1.2)
            f = f.at[int(0.25*n):int(0.6*n)].set(1.8)
            f = f.at[int(0.6*n):int(0.85*n)].set(1.1)
        elif pattern_idx == 8:
            f = f.at[int(0.1*n):int(0.35*n)].set(1.4)
            f = f.at[int(0.55*n):int(0.9*n)].set(0.85)
        else:
            f = f.at[start:end].set(h)
        
        return f

    def _create_multi_start(self, num_starts=6):
        """Create multiple different initializations."""
        initializations = []
        for i in range(num_starts):
            key = jax.random.PRNGKey(42 + i * 100)
            init = self._create_initializer(key, i)
            initializations.append((init, key))
        return initializations

    def _local_reinitialization(self, f_values: jnp.ndarray, key) -> jnp.ndarray:
        """Perform local reinitialization on 10-20% of intervals."""
        n = len(f_values)
        num_reinit = int(self.hypers.reinit_fraction * n)
        
        # Select random indices for reinitialization
        key, subkey = jax.random.split(key)
        reinit_indices = jax.random.permutation(subkey, n)[:num_reinit]
        
        # Create perturbation
        perturbation = jax.random.normal(subkey, f_values.shape) * self.hypers.reinit_std
        
        # Apply reinitialization while preserving non-negativity
        f_new = f_values.at[reinit_indices].set(f_values[reinit_indices] + perturbation[reinit_indices])
        f_new = jax.nn.relu(f_new)
        
        return f_new

    def _check_stagnation(self, c2_history: list, step_count: int) -> bool:
        """Check if C2 improvement stagnation is detected."""
        if step_count < self.hypers.stagnation_window:
            return False
        
        # Check recent C2 improvements
        recent_c2s = c2_history[-self.hypers.stagnation_window:]
        improvement = recent_c2s[-1] - recent_c2s[0]
        
        # Reset history if there's significant improvement
        if improvement > 1e-6:
            return False
        
        return True

    def _train_step(self, f_values: jnp.ndarray, opt_state, optimizer) -> Tuple:
        """Performs a single training step."""
        loss, grads = jax.value_and_grad(self._objective_fn)(f_values)
        updates, opt_state = optimizer.update(grads, opt_state, f_values)
        f_values = optax.apply_updates(f_values, updates)
        return f_values, opt_state, loss, grads

    def run_optimization(self) -> Tuple:
        """Sets up and runs two-phase multi-start optimization with hybrid exploration."""
        import optax
        
        # Create multiple initializations
        initializations = self._create_multi_start(num_starts=9)
        
        best_f = None
        best_c2 = 0.0
        
        for idx, (init_f, seed_key) in enumerate(initializations):
            print(f"\n=== Starting optimization from profile {idx + 1}/9 ===")
            
            # Phase 1: Coarse search with higher learning rate
            schedule1 = optax.warmup_cosine_decay_schedule(
                init_value=0.0,
                peak_value=self.hypers.learning_rate * 1.5,
                warmup_steps=self.hypers.warmup_steps,
                decay_steps=self.hypers.num_steps // 2 - self.hypers.warmup_steps,
                end_value=self.hypers.learning_rate * 0.1,
            )
            optimizer1 = optax.adam(learning_rate=schedule1, eps=1e-8)
            
            # Initialize with perturbation
            key = jax.random.PRNGKey(42 + idx * 100)
            f_values = init_f + 0.08 * jax.random.normal(key, init_f.shape)
            opt_state = optimizer1.init(f_values)
            
            # Hybrid optimization state
            step_count = 0
            stagnation_detected = False
            reinit_key = jax.random.PRNGKey(42 + idx * 1000)
            c2_history = []
            
            train_step_jit1 = jax.jit(lambda fv, os: self._train_step(fv, os, optimizer1))

            for step in range(self.hypers.num_steps // 2):
                f_values, opt_state, loss, grads = train_step_jit1(f_values, opt_state)
                step_count += 1
                
                current_c2 = -loss
                c2_history.append(float(current_c2))
                
                # Check for stagnation
                if self._check_stagnation(c2_history, step_count):
                    stagnation_detected = True
                
                # Perform reinitialization if stagnation detected
                if stagnation_detected and step_count % self.hypers.reinit_interval == 0:
                    f_values = self._local_reinitialization(f_values, reinit_key)
                    stagnation_detected = False
                    reinit_key, _ = jax.random.split(reinit_key)
                
                if float(current_c2) > float(best_c2):
                    best_c2 = current_c2
                    best_f = f_values.copy()
                
                if step % 5000 == 0 or step == self.hypers.num_steps // 2 - 1:
                    print(f"  Step {step:5d} | C2 ≈ {-loss:.8f} | Best: {best_c2:.8f} | Stagnation: {stagnation_detected}")
            
            # Phase 2: Fine-tuning with lower learning rate
            schedule2 = optax.warmup_cosine_decay_schedule(
                init_value=0.0,
                peak_value=self.hypers.learning_rate * 0.5,
                warmup_steps=1000,
                decay_steps=self.hypers.num_steps // 2 - 1000,
                end_value=self.hypers.learning_rate * 1e-4,
            )
            optimizer2 = optax.adam(learning_rate=schedule2, eps=1e-8)
            
            key = jax.random.PRNGKey(43 + idx * 100)
            f_values = best_f + 0.02 * jax.random.normal(key, best_f.shape)
            opt_state = optimizer2.init(f_values)
            
            print(f"\n=== Phase 2 fine-tuning for profile {idx + 1} ===")
            train_step_jit2 = jax.jit(lambda fv, os: self._train_step(fv, os, optimizer2))
            
            step_count = 0
            stagnation_detected = False
            reinit_key = jax.random.PRNGKey(43 + idx * 1000)
            c2_history = []
            
            for step in range(self.hypers.num_steps // 2):
                f_values, opt_state, loss, grads = train_step_jit2(f_values, opt_state)
                step_count += 1
                
                current_c2 = -loss
                c2_history.append(float(current_c2))
                
                # Check for stagnation
                if self._check_stagnation(c2_history, step_count):
                    stagnation_detected = True
                
                # Perform reinitialization if stagnation detected
                if stagnation_detected and step_count % self.hypers.reinit_interval == 0:
                    f_values = self._local_reinitialization(f_values, reinit_key)
                    stagnation_detected = False
                    reinit_key, _ = jax.random.split(reinit_key)
                
                if float(current_c2) > float(best_c2):
                    best_c2 = current_c2
                    best_f = f_values.copy()
                
                if step % 5000 == 0 or step == self.hypers.num_steps // 2 - 1:
                    print(f"  Step {step:5d} | C2 ≈ {-loss:.8f} | Best: {best_c2:.8f} | Stagnation: {stagnation_detected}")

        return jax.nn.relu(best_f), best_c2 if best_f is not None else 0.0


def run():
    """Entry point for running the optimization."""
    hypers = OptimizerHyperparameters(best_c2=0.8962799441554086)
    optimizer = C2Optimizer(hypers)
    optimized_f, final_c2_val = optimizer.run_optimization()

    loss_val = -final_c2_val
    f_values_np = np.array(optimized_f)

    return f_values_np, float(final_c2_val), float(loss_val), hypers.num_intervals
# EVOLVE-BLOCK-END
