def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    constructions = {}
    x = np.linspace(0, domain, N)
    # bimodal_tight: Two narrow peaks at 0.25 and 0.75
    latent = np.exp(-((x-0.25)/0.12)**2 * 25) + np.exp(-((x-0.75)/0.12)**2 * 25)
    constructions['bimodal_tight'] = latent
    # bimodal_wide: Broader peaks
    latent = np.exp(-((x-0.25)/0.25)**2 * 12) + np.exp(-((x-0.75)/0.25)**2 * 12)
    constructions['bimodal_wide'] = latent
    # triangular_3step: Three-level pattern
    phases = np.array([0.0, 0.333, 0.666])
    levels = np.array([-5, 5, -5])
    latent = np.zeros(N)
    for p, l in zip(phases, levels):
        in_range = (x >= p) & (x < p + 0.333)
        latent += l * in_range
    constructions['triangular_3step'] = latent
    # periodic_1: Period-1 alternating
    periodic = 2.0 * (x < 0.5) - 1.0
    latent = periodic * 5.0
    constructions['periodic_1'] = latent
    # periodic_1_5: Period-1.5 alternating
    periodic = 2.0 * (x < 0.667) - 1.0
    latent = periodic * 5.0
    constructions['periodic_1_5'] = latent
    # four_bimodal: Four narrow peaks
    peaks = np.array([0.1, 0.4, 1.0, 1.7])
    latent = np.zeros(N)
    for p in peaks:
        latent += np.exp(-((x-p)/0.1)**2 * 20)
    constructions['four_bimodal'] = latent
    # symmetric_bimodal: Symmetric about x=1
    latent = np.exp(-((x-1)/0.15)**2 * 18) * 2.0
    constructions['symmetric_bimodal'] = latent
    return {"constructions": constructions}
