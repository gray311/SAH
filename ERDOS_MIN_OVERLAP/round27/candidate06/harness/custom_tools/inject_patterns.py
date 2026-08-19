def run(ctx, args):
    p15 = '''
        elif pattern == 15:
            x = jnp.linspace(0, 2, N)
            latent = jnp.where(x < 0.4, 3.0, -3.0)
        elif pattern == 17:
            x = jnp.linspace(0, 2, N)
            frac = x - jnp.floor(x)
            T = 0.7
            latent = 0.5 + 0.5 * jnp.sin(2 * jnp.pi * frac / T)
    '''
    return {"edit": "After pattern == 14, add: " + p15, "patterns": ["15: asymmetric_bipartite", "17: frac_wave"]}