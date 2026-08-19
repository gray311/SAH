def run(ctx, args):
    import random
    random.seed(42 + ctx.iteration if hasattr(ctx, 'iteration') else 42)
    n = ctx.get_best_program()  # dummy, we'll generate patterns directly
    patterns = []
    
    # Pattern 1: Pyramid (low-high-low)
    patterns.append({
        'name': 'pyramid',
        'levels': 7,
        'heights': [0.4, 0.7, 1.5, 3.0, 1.5, 0.7, 0.4],
        'positions': [0.0, 0.14, 0.29, 0.43, 0.57, 0.71, 0.86, 1.0],
        'rationale': 'Symmetric pyramid concentrates energy at center'
    })
    
    # Pattern 2: Mountain (flat base, high peak)
    patterns.append({
        'name': 'mountain',
        'levels': 5,
        'heights': [0.5, 0.5, 2.8, 2.8, 0.5],
        'positions': [0.0, 0.20, 0.40, 0.60, 0.80, 1.0],
        'rationale': 'Wide base with high peak creates strong convolution peak'
    })
    
    # Pattern 3: Asymmetric (shifted high)
    patterns.append({
        'name': 'asymmetric_shifted',
        'levels': 6,
        'heights': [0.3, 0.8, 2.2, 1.8, 0.9, 0.3],
        'positions': [0.0, 0.10, 0.25, 0.40, 0.60, 0.80, 1.0],
        'rationale': 'Asymmetric placement tests non-symmetric optima'
    })
    
    # Pattern 4: Multi-peak (two high regions)
    patterns.append({
        'name': 'dual_peak',
        'levels': 8,
        'heights': [0.4, 0.4, 2.5, 2.5, 2.5, 2.5, 0.4, 0.4],
        'positions': [0.0, 0.12, 0.25, 0.38, 0.50, 0.62, 0.75, 0.88, 1.0],
        'rationale': 'Two high regions create two convolution peaks, may improve L2'
    })
    
    # Pattern 5: Staircase (ascending)
    patterns.append({
        'name': 'staircase',
        'levels': 7,
        'heights': [0.3, 0.6, 0.9, 1.5, 2.5, 3.0, 2.5],
        'positions': [0.0, 0.14, 0.29, 0.43, 0.57, 0.71, 0.86, 1.0],
        'rationale': 'Ascending then descending tests monotonicity benefits'
    })
    
    # Pattern 6: Flat-top (plateau)
    patterns.append({
        'name': 'flat_top',
        'levels': 5,
        'heights': [0.5, 0.5, 2.0, 2.0, 0.5],
        'positions': [0.0, 0.20, 0.40, 0.60, 0.80, 1.0],
        'rationale': 'Flat top creates uniform convolution in central region'
    })
    
    # Pattern 7: High-narrow spike
    patterns.append({
        'name': 'spike',
        'levels': 4,
        'heights': [0.4, 2.8, 2.8, 0.4],
        'positions': [0.0, 0.30, 0.50, 0.70, 1.0],
        'rationale': 'Very narrow high peak maximizes sup norm contribution'
    })
    
    return {
        'patterns': patterns,
        'note': 'Each pattern has levels, heights, and positions arrays. Edit the EVOLVE-BLOCK to implement one pattern. Use jnp.at for efficient updates.'
    }
