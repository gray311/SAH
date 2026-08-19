def run(ctx, args):
    import random
    best_f = ctx.get_best_program()
    lines = best_f.split('\n')
    
    architectures = [
        '# Triangular peak\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nps = int(0.35*600)\npe = int(0.50*600)\nh = 1.85\nf = f.at[ps:ps+10].set(h * jnp.linspace(0, 1, 10))\nf = f.at[ps+10:pe-10].set(h)\nf = f.at[pe-10:pe].set(h * jnp.linspace(1, 0, 10))',
        '# Bimodal steps\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nf = f.at[int(0.15*600):int(0.28*600)].set(1.40)\nf = f.at[int(0.42*600):int(0.55*600)].set(1.70)',
        '# Asymmetric - mass on left\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nf = f.at[int(0.05*600):int(0.18*600)].set(1.20)\nf = f.at[int(0.18*600):int(0.35*600)].set(2.00)\nf = f.at[int(0.35*600):int(0.60*600)].set(0.80)',
        '# Adaptive - coarse tails, fine peaks\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nf = f.at[int(0.00*600):int(0.05*600)].set(0.40)\nf = f.at[int(0.95*600):int(1.00*600)].set(0.40)\npr = int(0.20*600)\nf = f.at[pr:pr+120].set(1.90)',
        '# Plateau with steep edges\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nf = f.at[int(0.20*600):int(0.30*600)].set(1.30)\nf = f.at[int(0.30*600):int(0.70*600)].set(2.50)\nf = f.at[int(0.70*600):int(0.80*600)].set(1.30)\nf = f.at[int(0.80*600):int(0.95*600)].set(0.50)'
    ]
    
    random.seed(42)
    
    return {'architectures': architectures, 'note': 'Diverse architectures generated. Select by probe scores.'}
