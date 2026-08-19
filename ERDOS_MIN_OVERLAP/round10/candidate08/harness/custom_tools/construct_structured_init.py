def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    rng = np.random.default_rng(42)
    constructions = {}
    
    # bimodal_tight: Two narrow peaks at 0.25 and 0.75
    x = np.linspace(0, domain, N)
    a1, a2 = 0.25, 0.75
    bw1, bw2 = 0.12, 0.12
    latent = np.exp(-((x-a1)/bw1)**2 * 25) + np.exp(-((x-a2)/bw2)**2 * 25)
    constructions['bimodal_tight'] = latent
    
    # triangular_3step: Three-level triangular pattern
    x = np.linspace(0, domain, N)
    phases = np.array([0.0, 0.333, 0.666])
    levels = np.array([-5, -1, 5])
    latent = np.zeros(N)
    for p, l in zip(phases, levels):
        in_range = (x >= p) & (x < p + 0.333)
        latent = latent + l * in_range
    latent = latent + rng.normal(size=N) * 0.15
    constructions['triangular_3step'] = latent
    
    # periodic_2: Simple alternating pattern with asymmetry
    x = np.linspace(0, domain, N)
    periodic = 3.5 * (x < 0.4) - 2.5 * (x < 0.6)
    latent = periodic + rng.normal(size=N) * 0.1
    constructions['periodic_2'] = latent
    
    # golomb_5: Optimal spacing pattern from Golomb ruler
    x = np.linspace(0, domain, N)
    marks = np.array([0.0, 0.45, 0.75, 1.2, 1.65])
    kernel_widths = np.array([0.1, 0.12, 0.08, 0.11, 0.1])
    latent = np.zeros(N)
    for mark, kw in zip(marks, kernel_widths):
        latent = latent + 7.0 * np.exp(-((x-mark)/kw)**2 * 20)
    latent = latent + rng.normal(size=N) * 0.1
    constructions['golomb_5'] = latent
    
    return {"constructions": constructions, "keys_used": list(constructions.keys())}
