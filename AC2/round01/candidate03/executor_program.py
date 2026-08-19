# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    """Hyperparameters for symmetric step optimization."""

    num_intervals: int = 50
    learning_rate: float = 0.01
    num_steps: int = 20000
    warmup_steps: int = 1000


class C2Optimizer:
    """
    Optimizes using symmetric step-function approximation.
    The record-holder might benefit from symmetric (even) functions.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers

    def _construct_symmetric_step(self, N: int, key) -> jnp.ndarray:
        """
        Constructive initialization: symmetric step around center.
        High in two central regions, low at edges.
        """
        center = N // 2
        
        # High plateau in center region
        plateau_start = N // 4
        plateau_end = 3 * N // 4
        
        # Create symmetric pattern
        pattern = jnp.zeros(N)
        pattern = pattern.at[plateau_start:plateau_end].set(1.0)
        
        # Very small noise
        perturbation = 0.01 * jax.random.normal(key, (N,))
        pattern = pattern + perturbation
        
        # Ensure positivity
        pattern = jax.nn.softplus(pattern - 0.3)
        
        return pattern

    def _construct_centered_bump(self, N: int, key) -> jnp.ndarray:
        """
        Constructive initialization: centered bump with flat top.
        Similar to a plateau function.
        """
        center = N // 2
        plateau_width = N // 2
        
        # Flat top in center, sloped edges
        left_width = plateau_width // 2
        plateau_start = center - left_width
        plateau_end = center + left_width
        
        left_slope = jnp.linspace(0, 1, plateau_start)
        plateau = jnp.ones(plateau_end - plateau_start)
        right_slope = jnp.linspace(1, 0, N - plateau_end)
        
        f_values = jnp.concatenate([left_slope, plateau, right_slope])
        
        # Small noise
        perturbation = 0.02 * jax.random.normal(key, (N,))
        f_values = f_values + perturbation
        
        return f_values

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        """
        Computes the objective function using the unitless norm calculation.
        """
        f_non_negative = jax.nn.relu(f_values)

        # Unscaled discrete autoconvolution using FFT
        N = len(f_values)
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real

        # Calculate L2-norm squared of the convolution (trapezoidal rule)
        conv_real = convolution.real
        h = 1.0 / len(conv_real)
        l2_norm_squared = jnp.sum(h * (conv_real ** 2))

        # Calculate L1-norm of the convolution
        norm_1 = jnp.sum(jnp.abs(conv_real)) * h

        # Calculate infinity-norm of the convolution
        norm_inf = jnp.max(jnp.abs(conv_real))

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
            init_value=0.001,
            peak_value=self.hypers.learning_rate,
            warmup_steps=self.hypers.warmup_steps,
            decay_steps=self.hypers.num_steps - self.hypers.warmup_steps,
            end_value=self.hypers.learning_rate * 1e-4,
        )
        self.optimizer = optax.adam(learning_rate=schedule)

        key = jax.random.PRNGKey(42)
        
        # Try symmetric step initialization
        N = self.hypers.num_intervals
        f_values = self._construct_symmetric_step(N, key)

        opt_state = self.optimizer.init(f_values)
        print(
            f"Number of intervals (N): {self.hypers.num_intervals}, Steps: {self.hypers.num_steps}"
        )
        train_step_jit = jax.jit(self.train_step)

        loss = jnp.inf
        for step in range(self.hypers.num_steps):
            f_values, opt_state, loss = train_step_jit(f_values, opt_state)
            if step % 2000 == 0 or step == self.hypers.num_steps - 1:
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
# EVOLVE-BLOCK-END
