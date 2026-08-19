def run(ctx, args):
    import numpy as np
    current_bound = args.get("current_best_score", 0.38092303510845016)
    N = 800
    domain = 2.0
    dx = domain / N
    
    # Greedy piecewise-constant construction with 3 steps
    best_overlap = float("inf")
    a_found, b_found, c_found = None, None, None
    
    for a in np.linspace(0.2, 0.9, 20):
        for b in np.linspace(a, 1.0, 15):
            c = 2.0 - b
            h_vals = np.zeros(N)
            h_vals[:int(N*a)] = 2.0
            h_vals[int(N*a):int(N*c)] = 1.0
            h_vals[int(N*c):] = 0.0
            h = h_vals * (N * dx)
            h = h / (np.sum(h) * dx + 1e-10) * 1.0
            h = np.clip(h, 0, 1)
            h_padded = np.pad(h, (0, N))
            j_padded = np.pad(1.0 - h, (0, N))
            corr = np.fft.fft(h_padded) * np.conj(np.fft.fft(j_padded))
            overlap = np.fft.ifft(corr).real
            max_overlap = np.max(overlap * dx)
            if max_overlap < best_overlap:
                best_overlap = max_overlap
                a_found, b_found, c_found = a, b, c
    
    a, b, c = a_found, b_found, c_found
    code = "def _get_best_initialization(seed: int) -> jnp.ndarray:\n"
    code += "    N = self.hypers.num_intervals\n"
    code += "    x = jnp.linspace(0, 2, N)\n"
    code += f"    h = jnp.where(x < a, 1.5, jnp.where(x >= 2-a, 1.5, 0.5))\n"
    code += f"    h = h / (jnp.sum(h) * {dx})\n"
    code += "    return h\n"
    
    return {
        "new_method_code": code,
        "breakpoints": {"a": float(a), "b": float(b), "c": float(c)},
        "estimated_bound": float(best_overlap),
        "instruction": "Replace _get_best_initialization with this code and set num_restarts=1"
    }
