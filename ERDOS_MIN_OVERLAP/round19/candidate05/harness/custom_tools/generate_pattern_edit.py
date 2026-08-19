def run(ctx, args):
    import math
    pattern_type = args.get("pattern_type", "concentrated_peak")
    center = args.get("center", 0.5)
    return {
        "pattern_code": "# Pattern 15: {type} at {c}\n"
                       "key, subkey = jax.random.split(key)\n"
                       "x = jnp.linspace(0, 2, N)\n"
                       "c = {c}\n"
                       "latent = jnp.zeros(N)\n"
                       "mask = jnp.abs(x - c) < 0.12\n"
                       "latent = latent.at[mask].set(6.0)\n"
                       "latent = latent.at[~mask].set(-6.0)\n"
                       "latent = latent + jax.random.normal(subkey, (N,)) * 0.3\n"
                       "latent = jax.lax.stop_gradient(latent)\n"
                       "h = jax.nn.sigmoid(latent)\n"
                       "j_val = 1.0 - h\n"
                       "h_padded = jnp.pad(h, (0, N))\n"
                       "j_padded = jnp.pad(j_val, (0, N))\n"
                       "corr_fft = jnp.fft.fft(h_padded) * jnp.conj(jnp.fft.fft(j_padded))\n"
                       "correlation = jnp.fft.ifft(corr_fft).real\n"
                       "obj = jnp.max(correlation * self.dx)\n"
                       "if obj < best_obj:\n"
                       "    best_obj = obj\n"
                       "    best_latent = latent".replace("{type}", pattern_type).replace("{c}", str(center))
    }
