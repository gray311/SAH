# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    """Hyperparameters for the optimization process."""

    num_intervals: int = 200
    learning_rate: float = 0.001
    num_steps: int = 10000
    warmup_steps: int = 1000


class C2Optimizer:
    """
    Optimizes a discretized function to find a lower bound for the C2 constant.
    Uses improved initialization and proper convolution normalization.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        """
        Computes the objective function with proper normalization.
        """
        f_non_negative = jax.nn.relu(f_values)
        
        # Ensure positive sum for numerical stability
        f_sum = jnp.sum(f_non_negative)
        # Use jnp.where for JIT compatibility
        f_normalized = f_non_negative / jnp.maximum(f_sum, 1e-10)
        
        # Discrete autoconvolution via FFT with proper normalization
        N = self.hypers.num_intervals
        # Pad with zeros for circular convolution to approximate linear convolution
        padded_f = jnp.concatenate([f_normalized, jnp.zeros(N, dtype=f_normalized.dtype)])
        
        # Compute convolution: (f * f)[k] = sum_j f[j] * f[k-j]
        # Using FFT: conv = IFFT(FFT(f)^2)
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real
        
        # Take only the first N points (linear convolution result)
        convolution = convolution[:N]
        
        # Scale convolution by N (discretization factor)
        convolution = convolution * N
        
        # Calculate L2-norm squared of the convolution (trapezoidal rule)
        h = 1.0 / N
        # Use trapezoidal rule for better accuracy
        y_edges = jnp.concatenate([jnp.array([0.0]), convolution, jnp.array([0.0])])
        y_left = y_edges[:-1]
        y_right = y_edges[1:]
        l2_norm_squared = h * (0.5 * jnp.sum(y_left**2) + jnp.sum(convolution**2) + 0.5 * jnp.sum(y_right**2))
        
        # Calculate L1-norm of the convolution (trapezoidal rule)
        norm_1 = h * (jnp.sum(convolution) + jnp.sum(convolution))
        
        # Calculate infinity-norm of the convolution
        norm_inf = jnp.max(jnp.abs(convolution))
        
        # Calculate C2 ratio
        denominator = norm_1 * norm_inf
        # Use jnp.where for JIT compatibility
        c2_ratio = jnp.where(denominator > 1e-10, l2_norm_squared / denominator, jnp.inf)
        
        # We want to MAXIMIZE C2, so the optimizer must MINIMIZE its negative.
        return -c2_ratio

    def _create_step_function_init(self):
        """Create an initial function based on the known step function structure."""
        # Based on the current best: a step function with specific ratios
        # The record 0.8962799441554086 comes from a specific step function
        # Let's try a 2-step function: high plateau, low plateau
        
        N = self.hypers.num_intervals
        
        # Create a step-like function with a transition region
        # Start with a simple asymmetric step
        step_pos = N // 3
        
        # Left part: higher value, Right part: lower value
        # This creates a "ramp-down" structure
        f_init = jnp.ones(N)
        f_init = f_init * 0.5 + 0.5  # Values between 0.5 and 1.0
        f_init = f_init * (1.0 - jnp.arange(N) / N)  # Linear decay
        
        # Apply a step transition
        f_init = jnp.where(jnp.arange(N) < step_pos, 1.0, 0.1)
        
        return f_init

    def train_step(self, f_values: jnp.ndarray, opt_state: optax.OptState) -> tuple:
        """Performs a single training step."""
        loss, grads = jax.value_and_grad(self._objective_fn)(f_values)
        updates, opt_state = self.optimizer.update(grads, opt_state, f_values)
        f_values = optax.apply_updates(f_values, updates)
        return f_values, opt_state, loss

    def run_optimization(self):
        """Sets up and runs the full optimization process."""
        schedule = optax.warmup_cosine_decay_schedule(
            init_value=0.0,
            peak_value=self.hypers.learning_rate,
            warmup_steps=self.hypers.warmup_steps,
            decay_steps=self.hypers.num_steps - self.hypers.warmup_steps,
            end_value=self.hypers.learning_rate * 1e-4,
        )
        self.optimizer = optax.adam(learning_rate=schedule)

        # Use step-function-inspired initialization
        key = jax.random.PRNGKey(42)
        f_values = self._create_step_function_init()
        
        # Add small random perturbation to escape local minima
        f_values = f_values + jax.random.normal(key, f_values.shape) * 0.01
        f_values = jax.nn.relu(f_values)

        opt_state = self.optimizer.init(f_values)
        print(
            f"Number of intervals (N): {self.hypers.num_intervals}, Steps: {self.hypers.num_steps}"
        )
        train_step_jit = jax.jit(self.train_step)

        loss = jnp.inf
        for step in range(self.hypers.num_steps):
            f_values, opt_state, loss = train_step_jit(f_values, opt_state)
            if step % 1000 == 0 or step == self.hypers.num_steps - 1:
                print(f"Step {step:5d} | C2 ≈ {-loss:.8f}")

        final_c2 = -self._objective_fn(f_values)
        print(f"Final C2 lower bound found: {final_c2:.8f}")
        return jax.nn.relu(f_values), final_c2


def run():
    """Entry point for running the optimization."""
    hypers = Hyperparameters()
    optimizer = C2Optimizer(hypers)
    optimized_f, final_c2_val = optimizer.run_optimization()

    loss_val = -final_c2_val
    f_values_np = np.array(optimized_f)

    return f_values_np, float(final_c2_val), float(loss_val), hypers.num_intervals


# EVOLVE-BLOCK-END
