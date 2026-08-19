def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    
    rng = np.random.default_rng(123)
    constructions = {}
    
    # bimodal_tight: Two narrow peaks at 0.25 and 0.75 (theoretical optimal)
    x = np.linspace(0, domain, N)
    a1, a2 = 0.25, 0.75
    bw1, bw2 = 0.12, 0.12
    latent = np.exp(-((x-a1)/bw1)**2 * 30) + np.exp(-((x-a2)/bw2)**2 * 30)
    latent = (latent - np.min(latent)) / (np.max(latent) - np.min(latent) + 1e-10)
    constructions["bimodal_tight"] = latent
    
    # triangular_3step: Three-level triangular pattern
    x = np.linspace(0, domain, N)
    phases = np.array([0.0, 0.333, 0.666])
    levels = np.array([-10, -3, 10])
    latent = np.zeros(N)
    for p, l in zip(phases, levels):
        in_range = (x >= p) & (x < p + 0.333)
        latent = latent + l * in_range
    latent = latent + rng.normal(size=N) * 0.3
    constructions["triangular_3step"] = latent
    
    # periodic_2: Simple alternating pattern
    x = np.linspace(0, domain, N)
    periodic = 2.0 * (x < 0.5) - 1.0
    latent = periodic * 5.0
    latent = latent + rng.normal(size=N) * 0.4
    constructions["periodic_2"] = latent
    
    # golomb_5: 5 marks at optimal spacing
    x = np.linspace(0, domain, N)
    marks = np.array([0.0, 0.5, 1.0, 1.25, 1.75])
    kernel_widths = np.array([0.06, 0.07, 0.065, 0.065, 0.07])
    latent = np.zeros(N)
    for mark, kw in zip(marks, kernel_widths):
        latent = latent + 7.0 * np.exp(-((x-mark)/kw)**2 * 20)
    latent = latent + rng.normal(size=N) * 0.2
    constructions["golomb_5"] = latent
    
    return {
        "constructions": constructions,
        "usage_hint": "Use as initial_latent for the optimizer. Edit to set initial_latent = ..."
    }
