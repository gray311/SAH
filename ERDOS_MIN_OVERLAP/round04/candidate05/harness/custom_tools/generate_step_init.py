def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    
    constructions = {}
    
    # Type 1: Bimodal rectangles (h=1 on two bands)
    x = np.linspace(0, domain, N)
    w1, w2 = 0.22, 0.22
    # High regions at [0, w1] and [2-w2, 2]
    in_high1 = (x < w1)
    in_high2 = (x > 2 - w2)
    h_vals = np.zeros(N)
    h_vals[in_high1 | in_high2] = 1.0
    h_vals[in_high1 & in_high2] = 0.8  # small overlap region
    # Latent for sigmoid to produce these values
    latent = np.log(h_vals / (1.0 - h_vals + 1e-10))
    constructions['bimodal_rect'] = latent
    
    # Type 2: Trimmed bimodal (three-level)
    # h=1 on [0, a], h=0.5 on [a, b], h=0 on [b, 2]
    # Solve: a*1 + (b-a)*0.5 = 1 with a=0.2, b=0.6
    a, b = 0.2, 0.6
    h_vals = np.zeros(N)
    h_vals[(x < a)] = 1.0
    h_vals[(x >= a) & (x < b)] = 0.5
    h_vals[(x >= b)] = 0.0
    latent = np.log(h_vals / (1.0 - h_vals + 1e-10))
    constructions['trimmed_bimodal'] = latent
    
    # Type 3: Three equal pulses
    # Three pulses of width 1/3, h=1 each, separated by zeros
    w = 1.0 / 3.0
    h_vals = np.zeros(N)
    h_vals[(x < w)] = 1.0
    h_vals[(x >= w) & (x < 2*w)] = 0.0
    h_vals[(x >= 2*w)] = 1.0
    latent = np.log(h_vals / (1.0 - h_vals + 1e-10))
    constructions['three_pulse'] = latent
    
    # Type 4: Golomb ruler spacing (optimal marks: [0, 0.25, 0.625, 1.125, 2.0])
    marks = [0.0, 0.25, 0.625, 1.125, 2.0]
    widths = [0.08, 0.08, 0.08, 0.08, 0.08]
    h_vals = np.zeros(N)
    for m, wd in zip(marks, widths):
        region = (x >= m) & (x < m + wd)
        h_vals[region] = 1.0
    latent = np.log(h_vals / (1.0 - h_vals + 1e-10))
    constructions['golomb_pulse'] = latent
    
    return {"constructions": constructions, "keys": list(constructions.keys())}
