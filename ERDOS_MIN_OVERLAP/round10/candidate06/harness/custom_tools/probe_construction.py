def run(ctx, args):
    import numpy as np
    N = 800
    domain = 2.0
    dx = domain / N
    rng = np.random.default_rng(42)
    constructions = {}
    
    # bimodal_tight: Two sharp peaks at 0.25 and 0.75 with equal area
    x = np.linspace(0, domain, N)
    peak1, peak2 = 0.25, 0.75
    width1, width2 = 0.12, 0.12
    heights = 4.0
    bimodal = heights * np.exp(-((x-peak1)/width1)**2) + heights * np.exp(-((x-peak2)/width2)**2)
    bimodal = np.clip(bimodal, 0, 1)
    constructions['bimodal_tight'] = bimodal
    
    # periodic_step: Alternating between 0 and 1 with adjusted widths
    x = np.linspace(0, domain, N)
    widths = [0.3, 0.3, 0.3, 0.1]
    periodic = np.zeros(N)
    for i, (start, width) in enumerate([(0.0, widths[0]), (0.3, widths[1]), (0.6, widths[2]), (0.9, widths[3])]):
        if start + width <= domain:
            periodic = periodic + np.where((x >= start) & (x < min(start+width, domain)), 1.0, 0.0)
    periodic = periodic + rng.normal(size=N) * 0.02
    periodic = np.clip(periodic, 0, 1)
    constructions['periodic_step'] = periodic
    
    # golomb_ruler: 5 peaks at optimal spacing
    x = np.linspace(0, domain, N)
    marks = np.array([0.0, 0.5, 1.5, 1.8, 2.0])
    widths = np.array([0.12, 0.1, 0.08, 0.08, 0.1])
    heights = 6.0
    golomb = np.zeros(N)
    for mark, width in zip(marks, widths):
        golomb = golomb + heights * np.exp(-((x-mark)/width)**2)
    golomb = np.clip(golomb, 0, 1)
    constructions['golomb_ruler'] = golomb
    
    # triangular_wave: 3-level piecewise function
    x = np.linspace(0, domain, N)
    boundaries = [0.0, 0.333, 0.666, 1.0]
    levels = [0.0, 0.5, 1.0, 0.0]
    triangular = np.zeros(N)
    for i in range(1, len(boundaries)):
        start, end = boundaries[i-1], boundaries[i]
        if start < end:
            triangular = triangular + levels[i-1] * np.where((x >= start) & (x < end), 1.0, 0.0)
    triangular = np.clip(triangular, 0, 1)
    constructions['triangular_wave'] = triangular
    
    return {"constructions": constructions,
            "integral_info": {k: np.trapz(np.clip(constructions[k], 0, 1), x)
                              for k in constructions}}
