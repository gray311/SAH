def run(ctx, args):
    candidates = []
    
    # Candidate 1: Uniform middle interval (exact integral=1)
    candidates.append({
        "name": "uniform_middle",
        "description": "h=1 on [0.5, 1.5], h=0 elsewhere. Integral=1.0 exactly.",
        "num_intervals": 200,
        "construction": "h = jnp.where((x >= 0.5) & (x < 1.5), 1.0, 0.0)"
    })
    
    # Candidate 2: Double interval [0,0.5] U [1.5,2]
    candidates.append({
        "name": "double_interval",
        "description": "h=1 on [0, 0.5] U [1.5, 2], h=0 elsewhere. Integral=1.0.",
        "num_intervals": 200,
        "construction": "h = jnp.where((x >= 0.0) & (x < 0.5) | (x >= 1.5) & (x <= 2.0), 1.0, 0.0)"
    })
    
    # Candidate 3: Left half only
    candidates.append({
        "name": "left_half",
        "description": "h=1 on [0, 1], h=0 on [1, 2]. Integral=1.0.",
        "num_intervals": 200,
        "construction": "h = jnp.where((x >= 0.0) & (x < 1.0), 1.0, 0.0)"
    })
    
    # Candidate 4: Cosine-modulated (Fourier-friendly, integral approx 1)
    candidates.append({
        "name": "cosine_shape",
        "description": "h(x) = 0.5 + 0.5*cos(pi*x) for x in [0,2], clamped to [0,1]. Integral approx 1.",
        "num_intervals": 200,
        "construction": "h = jnp.clip(0.5 + 0.5 * jnp.cos(jnp.pi * x), 0.0, 1.0)"
    })
    
    # Candidate 5: Three equal intervals
    candidates.append({
        "name": "three_intervals",
        "description": "h=1 on [0, 0.333] U [0.666, 1.0] U [1.333, 1.666], h=0 elsewhere. Integral=1.0.",
        "num_intervals": 200,
        "construction": "h = jnp.where((x >= 0.0) & (x < 0.333333) | (x >= 0.666667) & (x < 1.0) | (x >= 1.333333) & (x < 1.666667), 1.0, 0.0)"
    })
    
    return {"candidates": candidates, "note": "These are STRUCTURED candidates. Implement the construction field directly in the EVOLVE-BLOCK."}
