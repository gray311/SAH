def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    x = np.linspace(0, domain, N)
    dx = domain / N
    
    # bimodal_step
    h1 = np.zeros(N)
    h1[(x >= 0.25) & (x <= 0.375)] = 1.0
    h1[(x >= 1.25) & (x <= 1.625)] = 1.0
    integral_h1 = np.sum(h1) * dx
    h1 = h1 / integral_h1
    blueprints = {}
    blueprints['bimodal_step'] = np.log(h1 + 1e-10) / 0.01
    
    # periodic_alternating
    h2 = np.zeros(N)
    h2[(x >= 0) & (x <= 0.5)] = 1.0
    h2[(x >= 1) & (x <= 1.5)] = 1.0
    integral_h2 = np.sum(h2) * dx
    h2 = h2 / integral_h2
    blueprints['periodic_alternating'] = np.log(h2 + 1e-10) / 0.005
    
    # golomb_construction
    golomb = np.array([0, 1, 4, 9, 11])
    scaled = golomb / 12.0 * 2.0
    widths = np.array([0.1, 0.12, 0.15, 0.13, 0.1])
    h_golomb = np.zeros(N)
    for mark, w in zip(scaled, widths):
        h_golomb += ((x >= mark - w/2) & (x <= mark + w/2)).astype(float)
    integral_golomb = np.sum(h_golomb) * dx
    h_golomb = h_golomb / integral_golomb
    blueprints['golomb_construction'] = np.log(h_golomb + 1e-10) / 1.0
    
    return {'blueprints': blueprints, 'normalized': True}