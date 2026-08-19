import random
import math

def run(ctx, args):
    candidates = []
    
    # 1. Multi-modal piecewise linear
    candidates.append({
        "family": "piecewise_linear_multi_modal",
        "code_snippet": "N=100; x = jnp.linspace(-1.5, 1.5, N+1); f = jnp.where(x < -1.0, 0.0, jnp.where(x < 0.5, x + 1.0, jnp.where(x < 1.0, 2.0 - x, 0.0)))"
    })
    
    # 2. Gaussian mixture
    candidates.append({
        "family": "gaussian_mixture",
        "code_snippet": "N=100; x = jnp.linspace(-3, 3, N+1); f = jnp.exp(-0.5*((x-0.0)**2)) + 0.3*jnp.exp(-0.2*((x-1.0)**2)) + 0.3*jnp.exp(-0.2*((x+1.0)**2))"
    })
    
    # 3. Spline-like (cubic segments)
    candidates.append({
        "family": "piecewise_cubic",
        "code_snippet": "N=150; x = jnp.linspace(-2, 2, N+1); k = jnp.minimum(jnp.maximum(jnp.floor((x+2)*N/4 + 0.5), 0), 3); f = 0.5*jnp.sin(N*x/4 + k*jnp.pi/N)**2"
    })
    
    # 4. Exponential decay combination
    candidates.append({
        "family": "exponential_mixture",
        "code_snippet": "N=80; x = jnp.linspace(-2, 2, N+1); f = 1.0/(1.0 + 0.5*abs(x)) + 0.3*0.8**abs(x)"
    })
    
    # 5. Symmetric double-peaked
    candidates.append({
        "family": "symmetric_peaks",
        "code_snippet": "N=120; x = jnp.linspace(-2.0, 2.0, N+1); f = 0.0 + 0.5*jnp.exp(-4*(abs(x)-0.6)**2) + 0.5*jnp.exp(-4*(abs(x)-1.2)**2)"
    })
    
    # 6. Multi-level step function
    candidates.append({
        "family": "multi_level_steps",
        "code_snippet": "N=60; x = jnp.linspace(-1.5, 1.5, N+1); f = jnp.where(x < -0.3, 0.0, jnp.where(x < 0.0, 0.8, jnp.where(x < 0.3, 1.2, jnp.where(x < 0.6, 0.0, jnp.where(x < 0.9, 0.4, 0.0))))"
    })
    
    # 7. Smoothed step function
    candidates.append({
        "family": "smoothed_steps",
        "code_snippet": "N=100; x = jnp.linspace(-2, 2, N+1); f = 0.0 + 0.3*jnp.tanh(10*(x + 0.5)) + 0.3*jnp.tanh(10*(x - 0.5)) + 1.4"
    })
    
    # 8. Multi-scale sum
    candidates.append({
        "family": "multi_scale_sum",
        "code_snippet": "N=140; x = jnp.linspace(-3, 3, N+1); f = jnp.exp(-x**2/12) + 0.5*jnp.exp(-4*(x-0.5)**2) + 0.5*jnp.exp(-4*(x+0.5)**2)"
    })
    
    return {"candidates": candidates, "note": "8 diverse function families for C2 optimization"}
