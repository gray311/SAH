def run(ctx, args):
    import numpy as np
    num_intervals = args.get('num_intervals', 200)
    num_candidates = args.get('num_candidates', 5)
    domain = np.linspace(0, 2, num_intervals)
    
    candidates = []
    
    # Pattern 1: Single block h=1 on [0,1]
    h1 = np.zeros(num_intervals)
    mask = domain < 1.0
    h1[mask] = 1.0
    integral = np.sum(h1) * (2.0/num_intervals)
    scale = 1.0 / (integral + 1e-9)
    h1 = h1 * scale
    candidates.append(h1)
    
    # Pattern 2: Two blocks [0,0.5] and [1.5,2] with h=0.5
    h2 = np.zeros(num_intervals)
    mask1 = (domain >= 0.0) & (domain < 0.5)
    mask2 = (domain >= 1.5) & (domain <= 2.0)
    h2[mask1] = 0.5
    h2[mask2] = 0.5
    integral = np.sum(h2) * (2.0/num_intervals)
    scale = 1.0 / (integral + 1e-9)
    h2 = h2 * scale
    candidates.append(h2)
    
    # Pattern 3: Uniform h=0.5 with small perturbation
    h3 = np.full(num_intervals, 0.5)
    integral = np.sum(h3) * (2.0/num_intervals)
    scale = 1.0 / (integral + 1e-9)
    h3 = h3 * scale
    candidates.append(h3)
    
    # Pattern 4: Sinusoidal
    h4 = 0.5 + 0.5 * np.sin(np.pi * domain)
    h4 = np.clip(h4, 0, 1)
    integral = np.sum(h4) * (2.0/num_intervals)
    scale = 1.0 / (integral + 1e-9)
    h4 = h4 * scale
    candidates.append(h4)
    
    # Pattern 5: Three blocks
    h5 = np.zeros(num_intervals)
    h5[domain < 1/3] = 0.75
    h5[(domain >= 1/3) & (domain < 2/3)] = 0.25
    h5[domain >= 2/3] = 0.75
    integral = np.sum(h5) * (2.0/num_intervals)
    scale = 1.0 / (integral + 1e-9)
    h5 = np.clip(h5 * scale, 0, 1)
    candidates.append(h5)
    
    return {"candidates": [c.tolist() for c in candidates],
            "num_intervals": num_intervals}
