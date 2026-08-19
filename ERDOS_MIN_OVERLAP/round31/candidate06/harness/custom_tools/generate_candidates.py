def run(ctx, args):
    import numpy as np
    import math
    
    N = 800
    domain = 2.0
    dx = domain / N
    domain_vals = np.linspace(0, domain, N)
    
    candidates = []
    
    # Pattern 1: Bipartite (single threshold)
    thresh = 0.7
    latent = np.where(domain_vals < thresh, 3.0, -3.0)
    latent = latent + 0.5 * np.random.randn(N)
    h1 = 1.0 / (1.0 + np.exp(-latent / 5.0))
    h1 = h1 * 4.0 * dx  # scale to integral ~ 1
    h1 = h1 / (np.sum(h1) * dx)  # normalize
    candidates.append(h1)
    
    # Pattern 2: Trimodal (three peaks)
    centers = [0.5, 1.0, 1.5]
    latent2 = np.zeros(N)
    for c in centers:
        mask = np.abs(domain_vals - c) < 0.12
        latent2[mask] = 4.0
    latent2 -= 2.0
    h2 = 1.0 / (1.0 + np.exp(-latent2 / 5.0))
    h2 = h2 * 4.0 * dx
    h2 = h2 / (np.sum(h2) * dx)
    candidates.append(h2)
    
    # Pattern 3: Piecewise-3
    latent3 = np.zeros(N)
    seg1 = np.where(domain_vals < 0.66, 3.5, 0.0)
    seg2 = np.where((domain_vals >= 0.66) & (domain_vals < 1.33), 3.5, 0.0)
    seg3 = np.where(domain_vals >= 1.33, 3.5, 0.0)
    latent3 = seg1 + seg2 + seg3
    latent3 -= 1.5
    h3 = 1.0 / (1.0 + np.exp(-latent3 / 5.0))
    h3 = h3 * 4.0 * dx
    h3 = h3 / (np.sum(h3) * dx)
    candidates.append(h3)
    
    # Pattern 4: Golomb-like (sparse peaks)
    marks = [0.0, 0.4, 0.8, 1.2, 1.6]
    latent4 = np.zeros(N)
    for m in marks:
        mask = np.abs(domain_vals - m) < 0.1
        latent4[mask] = 4.0
    latent4 -= 2.5
    h4 = 1.0 / (1.0 + np.exp(-latent4 / 5.0))
    h4 = h4 * 4.0 * dx
    h4 = h4 / (np.sum(h4) * dx)
    candidates.append(h4)
    
    # Pattern 5: Random with constraint
    np.random.seed(42)
    latent5 = np.random.randn(N) * 2.0
    h5 = 1.0 / (1.0 + np.exp(-latent5 / 5.0))
    h5 = h5 * 4.0 * dx
    h5 = h5 / (np.sum(h5) * dx)
    candidates.append(h5)
    
    return {"candidates": [c.tolist() for c in candidates]}
