# EVOLVE-BLOCK-START
from dataclasses import dataclass
import jax
import jax.numpy as jnp
import optax


@dataclass
class Hyperparameters:
    num_intervals: int = 200
    learning_rate: float = 0.005
    num_steps_per_restart: int = 16000
    num_restarts: int = 2
    penalty_strength: float = 100000.0


class ErdosOptimizer:
    def __init__(self, hypers):
        self.hypers = hypers
        self.domain_width = 2.0
        self.dx = self.domain_width / self.hypers.num_intervals

    def _compute_c5(self, h):
        j = 1.0 - h
        N = self.hypers.num_intervals
        h_padded = jnp.pad(h, (0, N))
        j_padded = jnp.pad(j, (0, N))
        corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))
        correlation = jnp.fft.ifft(corr_fft).real
        return jnp.max(correlation * self.dx)

    def _objective_fn(self, h):
        c5 = self._compute_c5(h)
        integral_h = jnp.sum(h) * self.dx
        constraint_loss = (integral_h - 1.0) ** 2
        return c5 + self.hypers.penalty_strength * constraint_loss

    def _optimize(self, init_h):
        optimizer = optax.adam(self.hypers.learning_rate)
        init_h = jnp.asarray(init_h)
        opt_state = optimizer.init(init_h)
        
        @jax.jit
        def step(h, opt_state):
            loss, grads = jax.value_and_grad(self._objective_fn)(h)
            updates, opt_state = optimizer.update(grads, opt_state)
            h = optax.apply_updates(h, updates)
            return h, opt_state, loss
        
        for step_idx in range(self.hypers.num_steps_per_restart):
            init_h, opt_state, loss = step(init_h, opt_state)
            if (step_idx + 1) % 500 == 0:
                init_h = jnp.clip(init_h, 0.0, 1.0)
                integral_h = jnp.sum(init_h) * self.dx
                if integral_h > 0:
                    init_h = init_h * (1.0 / integral_h)
                    init_h = jnp.clip(init_h, 0.0, 1.0)
        
        return init_h, float(self._compute_c5(init_h))

    def run(self):
        best_h, best_c5 = None, float('inf')
        
        seeds = [42, 123, 456, 789, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        
        for seed in seeds:
            key = jax.random.PRNGKey(seed)
            init_h = jax.random.uniform(key, (self.hypers.num_intervals,), minval=0.12, maxval=0.88)
            h, c5 = self._optimize(init_h)
            if c5 < best_c5:
                best_c5 = c5
                best_h = h
                print(f"  Seed {seed}: {c5:.6f}")
        
        final_h = jnp.clip(jax.nn.sigmoid(best_h * 8), 0.0, 1.0)
        intv = jnp.sum(final_h) * self.dx
        if abs(intv - 1.0) > 1e-6:
            final_h = jnp.clip(final_h / intv, 0.0, 1.0)
        final_c5 = float(self._compute_c5(final_h))
        print(f"Final Best C5 = {final_c5:.8f}")
        return final_h, final_c5, self.hypers.num_intervals


def run():
    hypers = Hyperparameters()
    opt = ErdosOptimizer(hypers)
    h, c5, n = opt.run()
    return h, c5, n


# EVOLVE-BLOCK-END
# EVOLVE-BLOCK-END
