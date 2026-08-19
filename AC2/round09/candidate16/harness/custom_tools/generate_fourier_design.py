def run(ctx, args):
    from dataclasses import dataclass
    N = args.get("num_terms", 20)
    
    def construct_fourier(coeffs, f_vals):
        f = jnp.zeros(400)
        for k in range(N):
            freq = k * 10.0
            amp = abs(coeffs[k]) + 0.01
            phase = coeffs[k + N] if k + N < 2 * N else 0.0
            f = f.at[f_vals].add(amp * jnp.cos(freq * f_vals + phase))
        f = jax.nn.relu(f)
        return f
    
    def compute_c2(f_vals):
        padded = jnp.pad(f_vals, (0, 400))
        fft_f = jnp.fft.fft(padded)
        conv = jnp.fft.ifft(fft_f * fft_f).real
        
        h = 1.0 / len(conv)
        l2_sq = jnp.sum((h / 3) * (conv[:-1] ** 2 + conv[:-1] * conv[1:] + conv[1:] ** 2))
        norm1 = jnp.sum(jnp.abs(conv)) / len(conv)
        norm_inf = jnp.max(jnp.abs(conv))
        denom = norm1 * norm_inf
        return l2_sq / denom
    
    return {"num_terms": N, "compute_c2": compute_c2, "construct": construct_fourier}