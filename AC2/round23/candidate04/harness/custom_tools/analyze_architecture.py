def run(ctx, args):
    best_f = ctx.get_best_program()
    lines = best_f.split('\n')
    
    # Detect step-function pattern
    has_step = any('pattern_idx' in l or '_create_step' in l for l in lines)
    has_poly = any('polyval' in l or 'jnp.polyval' in l for l in lines)
    has_exp = any('exp(-' in l or 'jax.nn.exp' in l for l in lines)
    has_spline = any('BSpline' in l or 'spline' in l for l in lines)
    
    # Detect polynomial
    if has_poly or has_exp:
        arch = 'polynomial' if has_poly else 'exponential'
    elif has_spline:
        arch = 'spline'
    elif has_step:
        arch = 'step-function'
    else:
        arch = 'unknown'
    
    # Check if stuck (all step-functions)
    stuck_warning = ''
    if arch == 'step-function':
        stuck_warning = 'WARNING: Current architecture is step-function. Consider exploring polynomials or splines!'
    
    return {'architecture_type': arch, 'stuck_warning': stuck_warning}
