def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    x = np.linspace(0, domain, N)
    pattern = args.get("pattern", "bimodal")
    sigma = args.get("sigma", 0.1)
    amplitude = args.get("amplitude", 4.0)
    latent = np.zeros(N)
    
    if pattern == "bimodal":
        a1, a2 = 0.25, 0.75
        latent = amplitude * np.exp(-(x-a1)**2 / (2*sigma**2)) + amplitude * np.exp(-(x-a2)**2 / (2*sigma**2))
    
    elif pattern == "periodic":
        duty = args.get("duty", 0.5)
        high = args.get("high", 5.0)
        low = args.get("low", -5.0)
        latent = high * ((x < domain*duty) & (x >= 0)).astype(float) + low * ((x >= domain*duty) & (x < domain)).astype(float)
    
    elif pattern == "golomb":
        marks = np.array([0.0, 0.5, 1.25, 1.875, 2.0])
        sigmas = 0.08 * np.array([1, 1.25, 1.1, 1.1, 1.2])
        amps = args.get("golomb_amp", 8.0)
        for m, s, a in zip(marks, sigmas, [amps]*5):
            latent += a * np.exp(-(x-m)**2 / (2*s**2))
    
    elif pattern == "triangular":
        levels = np.array([-10, -2, 10])
        widths = np.array([0.33, 0.34, 0.33])
        for lvl, w in zip(levels, widths):
            latent += lvl * ((x >= 0.33) & (x < 0.66)).astype(float)
    
    latent += np.random.default_rng(999).normal(0, 0.1, N)
    return {pattern: latent}
