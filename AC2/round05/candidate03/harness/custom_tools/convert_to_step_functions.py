def run(ctx, args):
    import json
    code = """# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
from dataclasses import dataclass

@dataclass
class StepFunctionHyperparameters:
    num_pulses: int = 3
    pulse_width: float = 0.15
    pulse_height: float = 1.3
    learning_rate: float = 0.2
    num_steps: int = 20000
    warmup_steps: int = 2000

class StepFunctionOptimizer:
    def __init__(self, hypers: StepFunctionHyperparameters):
        self.hypers = hypers
        self.best_f = None
        self.best_c2 = 0.0
        
    def _create_step_function(self, key):
        n = 800
        f = jnp.zeros(n)
        center = n // 2
        width = int(n * self.hypers.pulse_width / 2)
        
        if self.hypers.num_pulses == 1:
            left = center - width
            right = center + width
            f = f.at[left:right].set(self.hypers.pulse_height)
        elif self.hypers.num_pulses == 2:
            gap = 20
            left1 = center - width - gap
            right1 = center - gap
            left2 = center + gap
            right2 = center + width + gap
            f = f.at[left1:right1].set(self.hypers.pulse_height)
            f = f.at[left2:right2].set(self.hypers.pulse_height)
        else:
            spacing = int(n * self.hypers.pulse_width / 3)
            positions = [center - spacing - 30, center, center + spacing + 30]
            for pos in positions:
                f = f.at[pos - int(width/2):pos + int(width/2)].set(self.hypers.pulse_height)
        return f
    
    def _objective_fn(self, f_values: jnp.ndarray):
        f_non_negative = jax.nn.relu(f_values)
        N = len(f_non_negative)
        padded_f = jnp.pad(f_non_negative, (0, N))
        fft_f = jnp.fft.fft(padded_f)
        convolution = jnp.fft.ifft(fft_f * fft_f).real
        h = 1.0 / len(convolution)
        l2_norm_squared = h * jnp.sum(convolution**2)
        norm_1 = h * jnp.sum(jnp.abs(convolution))
        norm_inf = jnp.max(jnp.abs(convolution))
        c2_ratio = l2_norm_squared / (norm_1 * norm_inf)
        return -c2_ratio
    
    def _train_step(self, f_values, opt_state, optimizer):
        loss, grads = jax.value_and_grad(self._objective_fn)(f_values)
        updates, opt_state = optimizer.update(grads, opt_state, f_values)
        f_values = optax.apply_updates(f_values, updates)
        return f_values, opt_state, loss
    
    def run_optimization(self):
        key = jax.random.PRNGKey(42)
        optimizer = optax.Adam(learning_rate=self.hypers.learning_rate)
        opt_state = optimizer.init(jnp.zeros(800))
        best_f = None
        best_c2 = 0.0
        for pulse_config in range(self.hypers.num_pulses):
            key, subkey = jax.random.split(key)
            init_f = self._create_step_function(subkey)
            print(f"Optimizing {pulse_config+1}-pulse step function")
            f_values = init_f.copy()
            opt_state_curr = opt_state.copy()
            for step in range(self.hypers.num_steps):
                if step < self.hypers.warmup_steps:
                    lr = self.hypers.learning_rate * (step + 1) / self.hypers.warmup_steps
                else:
                    progress = (step - self.hypers.warmup_steps) / (self.hypers.num_steps - self.hypers.warmup_steps)
                    lr = self.hypers.learning_rate * (0.5 + 0.5 * jnp.cos(jnp.pi * progress))
                f_values, opt_state_curr, loss = self._train_step(f_values, opt_state_curr, optimizer)
                c2 = -loss
                if c2 > best_c2:
                    best_c2 = c2
                    best_f = f_values.copy()
        return best_f, best_c2
# EVOLVE-BLOCK-END
"""
    return {"code": code}