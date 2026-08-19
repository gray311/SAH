def run(ctx, args):
    import math
    import re
    seed_code = args.get("seed_pattern", "")
    
    variants = []
    
    # Variant 1: Scale input x by factor α
    variants.append({
        "name": "scaled_x",
        "code": f"""
        x_scaled = jnp.linspace(0, 2, N) * {0.5}
        latent = jnp.sin(2 * jnp.pi * x_scaled) * 2.0 + jnp.cos(4 * jnp.pi * x_scaled) * 1.0
        """
    })
    
    # Variant 2: Shift x by offset
    variants.append({
        "name": "shifted_x",
        "code": f"""
        x_shifted = jnp.linspace(0, 2, N) + {0.5}
        latent = jnp.sin(2 * jnp.pi * x_shifted) * 2.0 + jnp.cos(4 * jnp.pi * x_shifted) * 1.0
        """
    })
    
    # Variant 3: Piecewise with 3 levels
    variants.append({
        "name": "piecewise_3level",
        "code": f"""
        x = jnp.linspace(0, 2, N)
        levels = jnp.array([{0.6}, {0.2}, {0.2}])
        thresholds = jnp.array([{0.0}, {0.666}, {1.0}])
        latent = jnp.zeros(N)
        for thresh, level in zip(thresholds, levels):
            latent = latent + level * ((x >= thresh) & (x < thresh + 0.333)).astype(float)
        """
    })
    
    # Variant 4: Bimodal with adjustable width
    variants.append({
        "name": "bimodal_varwidth",
        "code": f"""
        x = jnp.linspace(0, 2, N)
        centers = jnp.array([{0.25}, {0.75}])
        width = {0.15}
        latent = jnp.zeros(N)
        for c in centers:
            latent = latent + 10.0 * jnp.exp(-((x-c)/width)**2 * 8)
        latent = latent + jax.random.normal(key, (N,)) * {0.2}
        """
    })
    
    # Variant 5: Piecewise with asymmetric ratios
    variants.append({
        "name": "asymmetric_piecewise",
        "code": f"""
        x = jnp.linspace(0, 2, N)
        a = {0.3}
        latent = jnp.where(x < a, {0.5}, jnp.where(x < 1-a, {0.3}, {0.2}))
        latent = latent + jax.random.normal(key, (N,)) * {0.2}
        """
    })
    
    return {"variants": variants, "count": len(variants)}
