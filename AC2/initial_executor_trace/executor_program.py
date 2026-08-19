# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    """Hyperparameters for the optimization process."""

    num_intervals: int = 400
    learning_rate: float = 0.005
    num_steps: int = 50000
    warmup_steps: int = 5000


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

        # Unscaled discrete autoconvolution using FFT
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real

        # Calculate L2-norm squared of the convolution: ||g||_2^2 = sum(g^2) * h
        # Using trapezoidal rule for numerical integration
        num_conv_points = len(convolution)
        h = 1.0 / num_conv_points
        g_squared = convolution ** 2
        # Trapezoidal rule: h * (0.5*g[0]^2 + sum(g[1:-1]^2) + 0.5*g[-1]^2)
        l2_norm_squared = h * (0.5 * g_squared[0] + jnp.sum(g_squared[1:-1]) + 0.5 * g_squared[-1])

        # Calculate L1-norm of the convolution: ||g||_1 = sum(|g|) * h
        norm_1 = jnp.sum(jnp.abs(convolution)) * h

        # Calculate infinity-norm of the convolution: ||g||_inf = max(|g|)
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

        key = jax.random.PRNGKey(42)
        # Initialize with a refined step function pattern
        # Fine-tuning the plateau widths and heights
        N = self.hypers.num_intervals
        center = N // 2
        
        # Create a refined step function
        f_values = jnp.ones(N) * 0.25
        # High plateau in the very center
        center_width = N // 20
        f_values = f_values.at[center - center_width: center + center_width].set(2.0)
        # Medium plateau around the center
        width2 = N // 10
        f_values = f_values.at[center - width2: center + width2].set(1.2)
        # Slight taper at edges
        width3 = N // 5
        f_values = f_values.at[center - width3: center + width3].set(0.6)

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
