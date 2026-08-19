def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    x = np.linspace(0, domain, N)
    constructions = {}
    
    # Construction 1: Bimodal sharp - two narrow peaks at 0.25, 0.75
    h1 = np.zeros(N)
    a1, a2 = 0.25, 0.75
    w1, w2 = 0.15, 0.15
    h1[(x >= a1) & (x < a1 + w1)] = 0.95
    h1[(x >= a2) & (x < a2 + w2)] = 0.95
    integral = h1.sum() * dx
    if integral > 0:
        h1 = h1 / integral
    constructions['bimodal_sharp'] = h1
    
    # Construction 2: Trichotomous - three-level pattern
    h2 = np.zeros(N)
    phases = [0.0, 1/3, 2/3]
    heights = [0.0, 1.0, 0.5]
    h2[(x >= phases[0]) & (x < phases[1])] = heights[0]
    h2[(x >= phases[1]) & (x < phases[2])] = heights[1]
    h2[(x >= phases[2])] = heights[2]
    integral = h2.sum() * dx
    if integral > 0:
        h2 = h2 / integral
    constructions['trichotomous'] = h2
    
    # Construction 3: Tri-peaked - three narrow peaks
    h3 = np.zeros(N)
    peaks = [0.2, 0.5, 0.8]
    widths = [0.12, 0.12, 0.12]
    for p, w in zip(peaks, widths):
        h3[(x >= p) & (x < p + w)] = 0.95
    integral = h3.sum() * dx
    if integral > 0:
        h3 = h3 / integral
    constructions['tri_peaked'] = h3
    
    # Construction 4: Asymmetric - wide left, narrow right
    h4 = np.zeros(N)
    h4[(x >= 0.0) & (x < 0.4)] = 0.85
    h4[(x >= 0.6) & (x < 1.0)] = 0.90
    integral = h4.sum() * dx
    if integral > 0:
        h4 = h4 / integral
    constructions['asymmetric'] = h4
    
    # Clip to [0,1]
    for k in constructions:
        constructions[k] = np.clip(constructions[k], 0, 1)
    
    return {"constructions": {k: v.tolist() for k, v in constructions.items()}}