def run(ctx, args):
    import random
    import numpy as np
    best_f = ctx.get_best_program()
    # Choose random family type
    family = random.choice(['gaussian_hybrid', 'spline', 'poly_cutoff', 'hybrid_step', 'fractal'])
    
    n = ctx.hypers.num_intervals if hasattr(ctx, 'hypers') else 600
    
    if family == 'gaussian_hybrid':
        # Step function modulated by Gaussian
        f = np.exp(-((np.arange(n) - n/2)**2) / (2 * (0.15*n)**2))
        f = f + 0.3 * np.exp(-((np.arange(n) - n/2)**2) / (2 * (0.1*n)**2))
    
    elif family == 'spline':
        # Piecewise quadratic spline
        f = np.zeros(n)
        knots = np.array([0.2, 0.35, 0.5, 0.65, 0.8, 1.0])
        for i, k in enumerate(knots[:-1]):
            start = int(k * n)
            end = int((k + 0.1) * n)
            f[start:end] = 0.8 + 0.3 * np.linspace(0, 1, end-start)
    
    elif family == 'poly_cutoff':
        # Step with polynomial smooth edges
        f = np.ones(n) * 1.2
        # Smooth edges using quadratic polynomial
        edge_width = int(0.05 * n)
        f[:edge_width] = f[:edge_width] * (np.linspace(0, 1, edge_width)**2 + 0.3)
        f[-edge_width:] = f[-edge_width:] * (np.linspace(1, 0, edge_width)**2 + 0.3)
    
    elif family == 'hybrid_step':
        # Core step + smooth boundary
        f = np.zeros(n)
        core_start = int(0.2 * n)
        core_end = int(0.8 * n)
        f[core_start:core_end] = 1.5
        # Add Gaussian tails
        f = f + 0.2 * np.exp(-((np.arange(n) - n/2)**2) / (2 * (0.2*n)**2))
    
    elif family == 'fractal':
        # Self-similar multi-scale structure
        f = np.zeros(n)
        scale = 0.2
        f[int(scale*n):int(scale*2*n)] = 0.5
        f[int(scale*3*n):int(scale*4*n)] = 0.5
        f[int(scale*5*n):int(scale*6*n)] = 1.8
        f[int(1-scale*n):int(1-scale*2*n)] = 0.5
        f[int(1-scale*3*n):int(1-scale*4*n)] = 0.5
    
    # Ensure non-negativity
    f = np.maximum(f, 0)
    
    return {"family": family, "new_code": f.astype(np.float32).tolist(), "note": f"Generated {family} variant"}