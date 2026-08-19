def run(ctx, args):
    return {
        'architectures': [
            '# Piecewise-linear\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nf = f.at[int(0.05*600):int(0.35*600)].set(jnp.linspace(0.5, 2.2, 300))\nf = f.at[int(0.35*600):int(0.65*600)].set(jnp.linspace(2.2, 0.5, 300))',
            '# Multi-level asymmetric\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nf = f.at[int(0.02*600):int(0.10*600)].set(1.10)\nf = f.at[int(0.10*600):int(0.25*600)].set(2.10)\nf = f.at[int(0.25*600):int(0.45*600)].set(1.80)\nf = f.at[int(0.45*600):int(0.65*600)].set(1.20)\nf = f.at[int(0.65*600):int(0.92*600)].set(0.70)',
            '# Double triangular with gap\nimport jax.numpy as jnp\nf = jnp.zeros(600)\nf = f.at[int(0.10*600):int(0.20*600)].set(jnp.linspace(0.3, 1.9, 100))\nf = f.at[int(0.20*600):int(0.30*600)].set(jnp.linspace(1.9, 0.3, 100))\nf = f.at[int(0.55*600):int(0.65*600)].set(jnp.linspace(0.3, 1.9, 100))\nf = f.at[int(0.65*600):int(0.75*600)].set(jnp.linspace(1.9, 0.3, 100))'
        ],
        'note': 'Completely new architectures. Use probes to select best.'
    }
