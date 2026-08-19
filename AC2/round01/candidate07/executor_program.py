# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    num_intervals: int = 100
    learning_rate: float = 0.005
    num_steps: int = 60000
    warmup_steps: int = 3000


class C2Optimizer:
    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers

    def _objective_fn(self, f_values: jnp.ndarray) -> jnp.ndarray:
        f_non_neg = jax.nn.relu(f_values)
        N = self.hypers.num_intervals
        padded_f = jnp.pad(f_non_neg, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real
        num_conv = len(convolution)
        h = 1.0 / (num_conv + 1)
        y_points = jnp.concatenate([jnp.array([0.0]), convolution, jnp.array([0.0])])
        y1, y2 = y_points[:-1], y_points[1:]
        l2_norm_sq = jnp.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))
        norm_1 = jnp.sum(jnp.abs(convolution)) / (len(convolution) + 1)
        norm_inf = jnp.max(jnp.abs(convolution))
        denom = norm_1 * norm_inf
        c2_ratio = l2_norm_sq / (denom + 1e-20)
        return -c2_ratio

    def train_step(self, f_values: jnp.ndarray, opt_state: optax.OptState) -> tuple:
        loss, grads = jax.value_and_grad(self._objective_fn)(f_values)
        updates, opt_state = self.optimizer.update(grads, opt_state, f_values)
        f_values = optax.apply_updates(f_values, updates)
        return f_values, opt_state, loss

    def run_optimization(self, seed: int) -> tuple:
        schedule = optax.warmup_cosine_decay_schedule(
            init_value=0.0, peak_value=0.008,
            warmup_steps=3000, decay_steps=57000, end_value=1e-12,
        )
        self.optimizer = optax.adam(learning_rate=schedule)

        key = jax.random.PRNGKey(seed)
        f_values = jax.random.exponential(key, (self.hypers.num_intervals,)) * 0.3 + 0.35

        opt_state = self.optimizer.init(f_values)
        train_step_jit = jax.jit(self.train_step)

        loss = jnp.inf
        for step in range(self.hypers.num_steps):
            f_values, opt_state, loss = train_step_jit(f_values, opt_state)
            f_values = jax.nn.relu(f_values)
            if step % 15000 == 0 or step == self.hypers.num_steps - 1:
                c2_temp = -self._objective_fn(f_values)
                if step == self.hypers.num_steps - 1 or jnp.isinf(c2_temp):
                    print(f"Seed {seed}: Step {step:6d} | C2 ≈ {-loss:.8f}")

        f_values = jax.nn.relu(f_values)
        final_c2 = -self._objective_fn(f_values)
        print(f"Seed {seed}: Final C2: {final_c2:.10f}")
        return f_values, final_c2


def run():
    hypers = Hyperparameters()
    best_c2 = -jnp.inf
    best_f = None
    
    for seed in [42, 123, 456, 789, 1012, 2024, 3036, 4048, 5060, 6072, 7084, 8096, 9108, 10214, 11320, 12426, 13532]:
        optimizer = C2Optimizer(hypers)
        f_vals, c2_val = optimizer.run_optimization(seed)
        if c2_val > best_c2:
            best_c2 = c2_val
            best_f = f_vals
            print(f"\n*** New best: seed={seed}, C2={best_c2:.10f} ***")

    f_np = np.array(best_f)
    print(f"\n=== Final: C2={best_c2:.10f}, Record=0.8962799441554086 ***")
    return f_np, float(best_c2), float(-best_c2), hypers.num_intervals
# EVOLVE-BLOCK-END
