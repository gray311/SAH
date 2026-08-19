def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    x = np.linspace(0, domain, N, endpoint=False)
    h1 = np.zeros(N)
    width = 0.2
    h1[(x >= 0.2) & (x < 0.4)] = 1.0 / (2.0 * width)
    h1[(x >= 0.6) & (x < 0.8)] = 1.0 / (2.0 * width)
    integral1 = np.sum(h1) * dx
    scale1 = 1.0 / integral1 if integral1 > 0 else 1.0
    h1 = np.clip(h1 * scale1, 0, 1)
    
    h2 = np.zeros(N)
    peaks = [(0.25, 0.2), (0.5, 0.25), (0.75, 0.2)]
    for cx, cw in peaks:
        mask = (x >= cx - cw/2) & (x < cx + cw/2)
        h2[mask] = (x[mask] - (cx - cw/2)) / cw
    integral2 = np.sum(h2) * dx
    scale2 = 1.0 / integral2 if integral2 > 0 else 1.0
    h2 = np.clip(h2 * scale2, 0, 1)
    
    h3 = np.zeros(N)
    h3[(x >= 0.0) & (x < 0.4)] = 0.625
    h3[(x >= 0.6) & (x < 1.0)] = 0.625
    h3[(x >= 1.0) & (x < 2.0)] = 0.25
    integral3 = np.sum(h3) * dx
    scale3 = 1.0 / integral3 if integral3 > 0 else 1.0
    h3 = np.clip(h3 * scale3, 0, 1)
    
    selected = h1
    
    return {
        "h": selected.tolist(),
        "type": "bimodal_symmetric",
        "integral_check": float(np.sum(selected) * dx)
    }
