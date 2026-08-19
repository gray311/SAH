# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    """Hyperparameters for the optimization process."""

    num_intervals: int = 50
    learning_rate: float = 0.01
    num_steps: int = 15000
    warmup_steps: int = 1000


def construct_step_function(num_intervals: int, num_steps: int = 12, seed: int = 42) -> jnp.ndarray:
    """
    Construct a piecewise step function with specified number of steps.
    Uses random breakpoints and heights for diversity.
    Based on the record-holder approach.
    """
    np.random.seed(seed)
    # Create breakpoints symmetrically around 0
    half_steps = num_steps // 2
    left_breaks = np.sort(np.random.uniform(-6, 0, half_steps))
    right_breaks = -np.sort(-np.random.uniform(0, 6, half_steps))
    all_breaks = np.concatenate([left_breaks, right_breaks])
    all_breaks = np.unique(all_breaks)
    
    # Ensure 0 is included
    if 0 not in all_breaks:
        all_breaks = np.concatenate([[0], all_breaks])
    all_breaks = np.sort(all_breaks)
    
    # Generate heights (positive values) - try a specific pattern
    # Record-holder likely uses a specific height pattern
    heights = np.ones(len(all_breaks))
    # Make center higher
    center_idx = len(all_breaks) // 2
    heights[center_idx] = 1.5
    heights[center_idx-1] = 1.2 if center_idx > 0 else 1.2
    heights[center_idx+1] = 1.2 if center_idx < len(heights)-1 else 1.2
    
    # Create step function: constant between breakpoints
    x = np.linspace(-10, 10, num_intervals)
    f_values = np.zeros(num_intervals)
    
    for i in range(num_intervals):
        # Find which interval this x falls into
        for j in range(len(all_breaks) - 1):
            if all_breaks[j] <= x[i] < all_breaks[j+1]:
                f_values[i] = heights[j]
                break
        else:
            # Last interval
            f_values[i] = heights[-1]
    
    return jnp.array(f_values)


class C2Optimizer:
    """
    Optimizes a discretized function to find a lower bound for the C2 constant
    using the rigorous, unitless, piecewise-linear integral method.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        """
        Computes the objective function using the unitless norm calculation.
        """
        f_non_negative = jax.nn.relu(f_values)

        # Unscaled discrete autoconvolution
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real

        # Calculate L2-norm squared of the convolution (rigorous method)
        num_conv_points = len(convolution)
        h = 1.0 / (num_conv_points + 1)
        y_points = jnp.concatenate([jnp.array([0.0]), convolution, jnp.array([0.0])])
        y1, y2 = y_points[:-1], y_points[1:]
        l2_norm_squared = jnp.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))

        # Calculate L1-norm of the convolution
        norm_1 = jnp.sum(jnp.abs(convolution)) / (len(convolution) + 1)

        # Calculate infinity-norm of the convolution
        norm_inf = jnp.max(jnp.abs(convolution))

        # Calculate C2 ratio
        denominator = norm_1 * norm_inf
        c2_ratio = l2_norm_squared / denominator

        # We want to MAXIMIZE C2, so the optimizer must MINIMIZE its negative.
        return -c2_ratio

    def train_step(self, f_values: jnp.ndarray, opt_state: optax.OptState) -> tuple:
        """Performs a single training step."""
        loss, grads = jax.value_and_grad(self._objective_fn)(f_values)
        updates, opt_state = self.optimizer.update(grads, opt_state, f_values)
        f_values = optax.apply_updates(f_values, updates)
        return f_values, opt_state, loss

    def run_optimization(self, initial_f: jnp.ndarray = None):
        """Sets up and runs the full optimization process."""
        schedule = optax.warmup_cosine_decay_schedule(
            init_value=0.0,
            peak_value=self.hypers.learning_rate,
            warmup_steps=self.hypers.warmup_steps,
            decay_steps=self.hypers.num_steps - self.hypers.warmup_steps,
            end_value=self.hypers.learning_rate * 1e-4,
        )
        self.optimizer = optax.adam(learning_rate=schedule)

        if initial_f is not None:
            f_values = initial_f
        else:
            key = jax.random.PRNGKey(42)
            f_values = jax.random.uniform(key, (self.hypers.num_intervals,))

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
    
    # Try with pure step function initialization - best seed found
    initial_f = construct_step_function(num_intervals=hypers.num_intervals, num_steps=12, seed=42)
    optimized_f, final_c2_val = optimizer.run_optimization(initial_f=initial_f)

    loss_val = -final_c2_val
    f_values_np = np.array(optimized_f)

    return f_values_np, float(final_c2_val), float(loss_val), hypers.num_intervals
# EVOLVE-BLOCK-END
