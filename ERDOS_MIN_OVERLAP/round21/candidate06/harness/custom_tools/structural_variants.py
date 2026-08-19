def run(ctx, args):
    import numpy as np
    edits = []
    
    # Edit 1: Higher frequency waves
    edit1 = """Pattern 2: Higher frequency waves
    latent = latent + jnp.sin(3 * jnp.pi * x) * 2.5 + jnp.cos(5 * jnp.pi * x) * 1.5"""
    edits.append(edit1)
    
    # Edit 2: Different Golomb ruler
    edit2 = """Pattern 12: Different Golomb ruler
    marks = jnp.array([0.0, 0.33, 0.66, 1.33, 2.0])
    latent = jnp.zeros(N)
    for m in marks:
        mask = jnp.abs(x - m) < 0.12
        latent = latent.at[mask].set(4.5)
    latent = latent - 2.0"""
    edits.append(edit2)
    
    # Edit 3: Multi-scale Gaussian mixture
    edit3 = """Pattern 15: Multi-scale Gaussian
    latent = jnp.zeros(N)
    centers = jnp.array([0.3, 0.7, 1.3, 1.7])
    widths = jnp.array([0.1, 0.2, 0.15, 0.25])
    amplitudes = jnp.array([3.0, 2.5, 3.5, 2.0])
    for c, w, a in zip(centers, widths, amplitudes):
        latent = latent + a * jnp.exp(-((x - c) / w)**2)
    latent = latent - 1.5"""
    edits.append(edit3)
    
    # Edit 4: Adaptive threshold
    edit4 = """Pattern 16: Adaptive threshold
    x = jnp.linspace(0, 2, N)
    threshold = 0.75
    latent = jnp.where(x < 0.5, 3.5, jnp.where(x > 1.0, 3.5, -2.5))
    latent = latent - jnp.sin(2 * jnp.pi * x) * 1.0"""
    edits.append(edit4)
    
    # Edit 5: Symmetric peaks
    edit5 = """Pattern 17: Symmetric peaks
    latent = jnp.zeros(N)
    x = jnp.linspace(0, 2, N)
    for center in [0.5, 1.0, 1.5]:
        mask = jnp.abs(x - center) < 0.1
        latent = latent.at[mask].set(4.0)
    latent = latent + jnp.sin(4 * jnp.pi * x) * 0.5
    latent = latent - 1.5"""
    edits.append(edit5)
    
    # Wrap each edit as a program modification
    return {"edits": edits, "num_edits": len(edits)}
