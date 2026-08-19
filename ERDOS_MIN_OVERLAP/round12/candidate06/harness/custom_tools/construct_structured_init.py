def run(ctx, args):
    import math
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(42)
    constructions = {}
    x = np.linspace(0, domain, N)
    a1, a2 = 0.25, 0.75
    bw1, bw2 = 0.15, 0.15
    latent = np.exp(-((x-a1)/bw1)**2 * 20) + np.exp(-((x-a2)/bw2)**2 * 20)
    latent = (latent - np.min(latent)) / (np.max(latent) - np.min(latent) + 1e-10)
    constructions['bimodal_tight'] = latent
    phases = np.array([0.0, 0.333, 0.666])
    levels = np.array([-5, -2, 5])
    latent = np.zeros(N)
    for p, l in zip(phases, levels):
        in_range = (x >= p) & (x < p + 0.333)
        latent = latent + l * in_range
    latent = latent + rng.normal(size=N) * 0.2
    constructions['triangular_3step'] = latent
    periodic = 2.0 * (x < 0.5) - 1.0
    latent = periodic * 4.0
    latent = latent + rng.normal(size=N) * 0.3
    constructions['periodic_2'] = latent
    marks = np.array([0.0, 2*0.25, 2*0.625, 2*0.9375, 2*1.0])
    kernel_widths = np.array([0.08, 0.1, 0.09, 0.09, 0.1])
    latent = np.zeros(N)
    for mark, kw in zip(marks, kernel_widths):
        latent = latent + 6.0 * np.exp(-((x-mark)/kw)**2 * 15)
    latent = latent + rng.normal(size=N) * 0.2
    constructions['golomb_5'] = latent
    return {"constructions": constructions}