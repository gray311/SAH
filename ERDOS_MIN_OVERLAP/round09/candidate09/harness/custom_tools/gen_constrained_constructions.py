def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    constructions = {}
    x = np.linspace(0, domain, N)
    
    # Bimodal: two narrow peaks at 0.25 and 0.75, equal mass
    latent = np.exp(-((x-0.25)/0.12)**2 * 30) + np.exp(-((x-0.75)/0.12)**2 * 30)
    h = 1.0 / (1.0 + np.exp(-latent))
    integral = np.sum(h) * dx
    scale = 1.0 / np.sum(h)  # normalize integral to 1
    h = h * scale
    h = np.clip(h, 0.01, 0.99)  # ensure strictly in (0,1)
    constructions["bimodal_tight"] = h
    
    # Triangular 3-step: low, medium, high levels
    h = np.zeros(N)
    phases = np.array([0.0, 0.333, 0.666])
    levels = np.array([0.1, 0.4, 0.8])
    for p, lev in zip(phases, levels):
        h += lev * ((x >= p) & (x < p + 0.333))
    integral = np.sum(h) * dx
    scale = 1.0 / np.sum(h)
    h = h * scale
    h = np.clip(h, 0.01, 0.99)
    constructions["triangular_3step"] = h
    
    # Periodic alternating: high on [0,0.5], low on [0.5,1]
    h = np.zeros(N)
    h[x < 1.0] = 0.6
    h[x >= 1.0] = 0.4
    integral = np.sum(h) * dx
    scale = 1.0 / np.sum(h)
    h = h * scale
    h = np.clip(h, 0.01, 0.99)
    constructions["periodic_alternating"] = h
    
    # Golomb-inspired 5 peaks
    marks = np.array([0.0, 0.375, 0.625, 0.875, 1.0])
    widths = np.array([0.08, 0.1, 0.09, 0.09, 0.08])
    h = np.zeros(N)
    for m, w in zip(marks, widths):
        h += 3.0 * np.exp(-((x-m)/w)**2 * 20)
    integral = np.sum(h) * dx
    scale = 1.0 / np.sum(h)
    h = h * scale
    h = np.clip(h, 0.01, 0.99)
    constructions["golomb_5"] = h
    
    # Sawtooth 4-level
    h = np.zeros(N)
    levels = [0.15, 0.35, 0.55, 0.75]
    for i, lev in enumerate(levels):
        start = i * 0.5
        end = (i+1) * 0.5 if i < 3 else 2.0
        h[(x >= start) & (x < end)] = lev
    integral = np.sum(h) * dx
    scale = 1.0 / np.sum(h)
    h = h * scale
    h = np.clip(h, 0.01, 0.99)
    constructions["sawtooth_4level"] = h
    
    # Plateau 3-level with flat top
    h = np.zeros(N)
    h[x < 0.333] = 0.2
    h[(x >= 0.333) & (x < 0.666)] = 0.8
    h[x >= 0.666] = 0.25
    integral = np.sum(h) * dx
    scale = 1.0 / np.sum(h)
    h = h * scale
    h = np.clip(h, 0.01, 0.99)
    constructions["plateau_3level"] = h
    
    return {"constructions": constructions, "count": len(constructions)}