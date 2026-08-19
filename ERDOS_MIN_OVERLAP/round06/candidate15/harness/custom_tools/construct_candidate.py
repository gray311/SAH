def run(ctx, args):
    import math
    import numpy as np
    N = args.get("intervals", 100)
    dx = 2.0 / N
    x = np.linspace(0, 2, N+1)[1:]  # exclude right endpoint
    
    pattern = args.get("pattern", "uniform")
    
    candidates = []
    
    if pattern == "uniform":
        # h = c on [0,a], 0 elsewhere, ∫h = c*a*dx = 1 => c = 1/(a*dx)
        for a in [0.3, 0.4, 0.5, 0.6]:
            c = 1.0 / (a * dx)
            if c > 1.0:
                continue
            h = np.zeros(N)
            h[:int(a/dx)] = c
            if np.any(h > 1.0):
                continue
            h = h / np.sum(h) * N * dx  # normalize
            candidates.append(h)
    
    elif pattern == "two_plateau":
        # h = a on [0,b], h = c on [1,2]
        for b in [0.2, 0.3, 0.4, 0.5]:
            for a in [0.5, 0.6, 0.7, 0.8]:
                c = 0.5 * a
                h = np.zeros(N)
                h[:int(b/dx)] = a
                h[int(1.0/dx):] = c
                if np.any(h > 1.0) or np.any(h < 0.0):
                    continue
                total = np.sum(h) * dx
                if abs(total - 1.0) < 0.01:
                    h = h / total * 1.0
                    candidates.append(h)
    
    elif pattern == "concentrated":
        # h = 1 on [0.5, 1.5]
        h = np.zeros(N)
        start = int(0.5/dx)
        end = int(1.5/dx)
        h[start:end] = 1.0
        integral = np.sum(h) * dx
        if abs(integral - 1.0) > 0.05:
            scale = 1.0 / integral
            h = h * scale
            if np.any(h > 1.0):
                return {"note": "concentrated failed normalization"}
        candidates.append(h)
    
    elif pattern == "alternating":
        # Alternating blocks of different heights
        num_blocks = 4
        for block_ratio in [0.25, 0.3, 0.33]:
            h = np.zeros(N)
            for i in range(num_blocks):
                start_pos = i * (2.0 / num_blocks)
                end_pos = (i + 1) * (2.0 / num_blocks)
                start_idx = int(start_pos / dx)
                end_idx = int(end_pos / dx)
                h[start_idx:end_idx] = 0.5 + i * 0.2
            h = h / np.sum(h) * N * dx
            if np.any(h > 1.0) or np.any(h < 0.0):
                continue
            candidates.append(h)
    
    else:
        # Uniform-like with slight variation
        base = 0.4
        h = np.ones(N) * base
        # Add small perturbations
        for i in range(0, N, 20):
            pert = np.random.uniform(-0.1, 0.1)
            h[i] += pert
        h = h / np.sum(h) * N * dx
        if np.any(h > 1.0):
            h = np.clip(h, 0.0, 1.0)
        h = h / np.sum(h) * N * dx
        candidates.append(h)
    
    # Return the best candidate
    if not candidates:
        # Fallback: uniform h=0.5 everywhere
        h = np.ones(N) * 0.5
        h = h / np.sum(h) * N * dx
        if np.any(h > 1.0):
            h = np.ones(N) * 1.0 / 2.0
        return {"h": h.tolist(), "note": "fallback uniform"}
    
    # Return all candidates as list
    return {"candidates": [c.tolist() for c in candidates[:5]], "pattern": pattern, "N": N}