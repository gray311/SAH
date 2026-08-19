# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
from dataclasses import dataclass


@dataclass
class Hyperparameters:
    """Hyperparameters."""

    num_intervals: int = 80
    learning_rate: float = 0.03
    num_steps: int = 20000
    init_decay: float = 1.5


class C2Optimizer:
    """
    Optimizes using asymmetric exponential-family initialization
    inspired by successful step-function solutions.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers

    def _c2_score(self, x):
        """C2 ratio computation."""
        f = jnp.exp(x)
        N = self.hypers.num_intervals
        padded = jnp.pad(f, (0, N))
        fft_f = jnp.fft.fft(padded)
        conv = jnp.fft.ifft(fft_f * fft_f).real
        
        h = 1.0 / (len(conv) + 1)
        y = jnp.concatenate([jnp.array([0.0]), conv, jnp.array([0.0])])
        y1, y2 = y[:-1], y[1:]
        l2_sq = jnp.sum((h / 3) * (y1**2 + y1 * y2 + y2**2))
        
        norm1 = jnp.sum(jnp.abs(conv)) / (len(conv) + 1)
        norminf = jnp.max(jnp.abs(conv))
        
        return l2_sq / (norm1 * norminf + 1e-15)

    def _init_func(self):
        """Create asymmetric exponential-like initialization."""
        N = self.hypers.num_intervals
        x_pos = jnp.arange(N) / N
        
        # Create exponential decay (right-skewed)
        exponential = -self.hypers.init_decay * x_pos
        f_shape = jnp.exp(exponential)
        
        # Normalize
        f_shape = f_shape / jnp.sum(f_shape)
        
        # Take logarithm to work in log-space
        x_init = jnp.log(f_shape + 1e-8)
        
        # Add Gaussian noise
        key = jax.random.PRNGKey(42)
        noise = jax.random.normal(key, (N,)) * 0.05
        x_init = x_init + noise
        
        return x_init

    def _init_func2(self):
        """Create bimodal initialization."""
        N = self.hypers.num_intervals
        key = jax.random.PRNGKey(42)
        
        # Two clusters with different amplitudes
        center1, center2 = N // 4, 3 * N // 4
        gauss1 = jnp.exp(-10 * (jnp.arange(N) - center1) ** 2)
        gauss2 = 0.8 * jnp.exp(-10 * (jnp.arange(N) - center2) ** 2)
        bimodal = gauss1 + gauss2
        bimodal = bimodal / jnp.sum(bimodal) * 2.0
        
        x_init = jnp.log(bimodal + 1e-8)
        
        return x_init

    def train_step(self, x, opt_state, step_num):
        """Single training step."""
        c2 = self._c2_score(x)
        loss = -c2
        grad = jax.grad(self._c2_score)(x)
        grad = -grad
        
        progress = step_num / self.hypers.num_steps
        lr_schedule = jnp.where(progress < 0.2, 
                               jax.nn.sigmoid(step_num / 500),
                               (1 + jnp.cos(jnp.pi * progress)) / 2 * 0.05)
        current_lr = 0.03 * lr_schedule
        
        grad = jnp.clip(grad, -3.0, 3.0)
        updates, opt_state = optax.adam(learning_rate=current_lr).update(grad, opt_state, x)
        x = optax.apply_updates(x, updates)
        
        return x, opt_state, loss

    def run(self):
        """Main optimization with multiple initialization attempts."""
        # Try multiple initializations, keep the best
        best_x = None
        best_c2 = -jnp.inf
        
        for seed in [42, 123, 456, 789]:
            key = jax.random.PRNGKey(seed)
            
            # Choose between asymmetric and bimodal init based on seed parity
            if seed % 2 == 0:
                x = self._init_func()
            else:
                x = self._init_func2()
            
            x = x.at[jnp.arange(len(x))[:5]].set(x[:5] + 0.5)  # Boost left side
            
            optimizer = optax.adam(learning_rate=0.05)
            opt_state = optimizer.init(x)
            
            train_fn = jax.jit(lambda h, s: self.train_step(h, s, jnp.zeros(())))
            
            for step in range(self.hypers.num_steps):
                x, opt_state, loss = train_fn(x, opt_state)
                
                if step % 5000 == 0 or step == self.hypers.num_steps - 1:
                    c2 = -loss
                    if c2 > best_c2:
                        best_c2 = c2
                        best_x = x.copy()
                        print(f"Seed {seed}, Step {step:5d} | C2 = {c2:.8f}")
            
            # Evaluate final
            c2_final = self._c2_score(x)
            if c2_final > best_c2:
                best_c2 = c2_final
                best_x = x.copy()
        
        return jnp.exp(best_x), best_c2


def run():
    hypers = Hyperparameters()
    optimizer = C2Optimizer(hypers)
    f_out, c2 = optimizer.run()
    return np.array(f_out), float(c2), 0.0, hypers.num_intervals
# EVOLVE-BLOCK-END
