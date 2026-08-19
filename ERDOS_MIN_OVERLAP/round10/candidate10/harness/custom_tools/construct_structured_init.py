def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(123)
    x = np.linspace(0, domain, N)
    constructions = {}
    
    # Binary (0/1) single block: h=1 on [0.5, 1.5], 0 elsewhere (integral=1)
    binary = np.zeros(N)
    binary[(x >= 0.5) & (x < 1.5)] = 1.0
    constructions['binary_1block'] = binary
    
    # Binary two blocks: [0,0.5] and [1,1.5]
    binary2 = np.zeros(N)
    binary2[(x >= 0.0) & (x < 0.5)] = 1.0
    binary2[(x >= 1.0) & (x < 1.5)] = 1.0
    constructions['binary_2blocks'] = binary2
    
    # Three-equal blocks
    three = np.zeros(N)
    widths = N // 3
    three[(x >= 0) & (x < widths*dx)] = 1.0
    three[(x >= 1) & (x < 1+widths*dx)] = 1.0
    constructions['binary_3equal'] = three
    
    # Gaussian-bimodal (sharp peaks, not smooth)
    g1 = np.exp(-((x - 0.25) ** 2) / (2 * 0.08**2))
    g2 = np.exp(-((x - 0.75) ** 2) / (2 * 0.08**2))
    bimodal = g1 + g2
    norm = np.max(bimodal) * 0.5
    bimodal = (bimodal / norm).clip(0, 1)
    constructions['bimodal_sharp'] = bimodal
    
    # Five peaks (Golomb-inspired positions)
    marks = np.array([0.0, 0.4, 0.65, 0.9, 1.4])
    gauss5 = np.zeros(N)
    for m in marks:
        gauss5 += np.exp(-((x - m) ** 2) / (2 * 0.05**2))
    norm5 = np.max(gauss5) * 0.6
    gauss5 = (gauss5 / norm5).clip(0, 1)
    constructions['pentapeak'] = gauss5
    
    # Periodic square wave
    periodic = np.where((x >= 0.25) & (x < 0.75), 0.5, 0.0)
    constructions['periodic_square'] = periodic
    
    return {"constructions": constructions, "num_constructions": len(constructions)}
