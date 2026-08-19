# EVOLVE-BLOCK-START
import jax
import jax.numpy as jnp
import optax
import numpy as np
import tqdm


def compute_c5(h, N):
    j_val = 1.0 - h
    dx = 2.0 / N
    h_pad = jnp.pad(h, (0, N))
    j_pad = jnp.pad(j_val, (0, N))
    corr = jnp.fft.ifft(jnp.fft.fft(h_pad) * jnp.conj(jnp.fft.fft(j_pad))).real
    return float(jnp.max(corr * dx))

def objective_impl(latents, penalty, N):
    """Direct implementation without JAX transformations."""
    h = jax.nn.sigmoid(latents)
    dx = 2.0 / N
    j_val = 1.0 - h
    h_pad = jnp.pad(h, (0, N))
    j_pad = jnp.pad(j_val, (0, N))
    corr = jnp.fft.ifft(jnp.fft.fft(h_pad) * jnp.conj(jnp.fft.fft(j_pad))).real
    obj = jnp.max(corr * dx)
    integral = jnp.sum(h) * dx
    return obj + penalty * (integral - 1.0) ** 2

def create_optimizer_state(penalty, N, lr):
    """Create loss and grad functions that work with JAX transformations."""
    loss_fn_with_penalty = lambda x: objective_impl(x, penalty, N)
    return jax.grad(loss_fn_with_penalty)

def run_optimization():
    best_c5 = float('inf')
    best_h = None
    
    strategies = [
        {"num_intervals": 200, "learning_rate": 0.01, "num_steps": 4000, "penalty": 100000.0, "seeds": [1, 42]},
        {"num_intervals": 300, "learning_rate": 0.005, "num_steps": 5000, "penalty": 50000.0, "seeds": [1, 42, 100]},
    ]
    
    for strat in strategies:
        N = strat["num_intervals"]
        pen = strat["penalty"]
        lr = strat["learning_rate"]
        steps = strat["num_steps"]
        seeds = strat["seeds"]
        
        # Get gradient function directly
        loss_with_penalty = lambda x: objective_impl(x, pen, N)
        grad_fn = jax.grad(loss_with_penalty)
        jit_loss = jax.jit(loss_with_penalty)
        jit_grad = jax.grad(jit_loss)
        
        optimizer = optax.adam(lr)
        
        for seed in seeds:
            print(f"Intervals={N}, Seed={seed}")
            
            key = jax.random.PRNGKey(seed)
            latents = jax.random.normal(key, (N,))
            opt_state = optimizer.init(latents)
            
            # Simple loop
            for i in tqdm.tqdm(range(steps), desc=f"N={N}, seed={seed}"):
                total_loss = jit_loss(latents)
                grads = jit_grad(latents)
                updates, opt_state = optimizer.update(grads, opt_state)
                latents = optax.apply_updates(latents, updates)
            
            final_h = jax.nn.sigmoid(latents)
            c5 = compute_c5(final_h, N)
            
            if c5 < best_c5:
                best_c5 = c5
                best_h = final_h
            
            print(f"  Result C5 = {c5:.8f}")
    
    return best_h, best_c5, max(s["num_intervals"] for s in strategies)

def run():
    final_h, c5_bound, n_points = run_optimization()
    return final_h, c5_bound, n_points
# EVOLVE-BLOCK-END
