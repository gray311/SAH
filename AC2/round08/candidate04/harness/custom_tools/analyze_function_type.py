def run(ctx, args):
    code = ctx.get_program()
    program = ctx.get_best_program()
    
    # Detect function type from code patterns
    has_spline = 'scipy.interpolate' in code or 'BSpline' in code or 'CubicSpline' in code
    has_mixture = 'Gaussian' in code or 'exp' in code.lower() and 'mixture' in code.lower() or 'weighted' in code.lower()
    has_polynomial = 'poly' in code.lower() and ('fit' in code or 'coeff' in code)
    has_step = 'piecewise' in code.lower() or 'jnp.where' in code or 'step' in code.lower()
    
    # Check for optimization patterns
    uses_fft = 'fft' in code.lower() or 'ifft' in code.lower()
    uses_ad = 'autograd' in code or 'jax.grad' in code or 'vmap' in code
    
    # Estimate performance tier based on patterns
    if has_spline:
        func_type = 'spline'
        tier = 'advanced'
        recommendation = 'Consider B-spline knot placement or tensor-product splines'
    elif has_mixture:
        func_type = 'mixture'
        tier = 'advanced'
        recommendation = 'Try different mixture weights or number of components'
    elif has_polynomial:
        func_type = 'polynomial'
        tier = 'intermediate'
        recommendation = 'Try higher degree or truncated polynomial forms'
    elif has_step:
        func_type = 'step'
        tier = 'baseline'
        recommendation = 'Seed already uses multi-level steps - explore smoother alternatives'
    else:
        func_type = 'unknown'
        tier = 'unknown'
        recommendation = 'Try spline or mixture models for better performance'
    
    return {
        'function_class': func_type,
        'tier': tier,
        'uses_fft': uses_fft,
        'uses_ad': uses_ad,
        'has_spline': has_spline,
        'has_mixture': has_mixture,
        'has_polynomial': has_polynomial,
        'has_step': has_step,
        'recommendation': recommendation
    }
