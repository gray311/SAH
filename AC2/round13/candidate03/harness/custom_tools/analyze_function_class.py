def run(ctx, args):
    best_program = ctx.get_best_program()
    analysis = {}
    
    import re
    content = best_program
    
    has_steps = bool(re.search(r'\.set\([0-9.]+,\s*[0-9.]+,\s*\)', content))
    has_relu = bool(re.search(r'jax\.nn\.relu|jnp\.maximum', content))
    has_gaussian = bool(re.search(r'exp\(-\(', content) and bool(re.search(r'mu|mean', content, re.IGNORECASE)))
    has_spline = bool(re.search(r'splev|splrep|BSpline', content, re.IGNORECASE))
    has_oscillatory = bool(re.search(r'cos\(beta|cos\(.*\*.*\)', content))
    
    if has_steps or has_relu:
        analysis['family'] = 'step_like'
        analysis['reasoning'] = 'Program uses piecewise constant assignments or ReLU transformations, characteristic of step functions'
    elif has_gaussian:
        analysis['family'] = 'Gaussian_mixture'
        analysis['reasoning'] = 'Program contains Gaussian kernel structures with mean/standard deviation parameters'
    elif has_spline:
        analysis['family'] = 'B_spline'
        analysis['reasoning'] = 'Program uses spline interpolation functions (splev/splrep)'
    elif has_oscillatory:
        analysis['family'] = 'oscillatory_decay'
        analysis['reasoning'] = 'Program contains oscillatory components (cosine) with decay terms'
    else:
        analysis['family'] = 'unknown_or_piecewise_linear'
        analysis['reasoning'] = 'Function appears to be piecewise or hybrid construction'
    
    orthogonal_suggestions = {
        'step_like': ['gaussian_mixture', 'bspline', 'oscillatory_decay', 'exponential_decay'],
        'gaussian_mixture': ['step_like', 'bspline', 'piecewise_linear', 'oscillatory_decay'],
        'bspline': ['step_like', 'gaussian_mixture', 'piecewise_linear', 'fractal_construction'],
        'oscillatory_decay': ['step_like', 'gaussian_mixture', 'exponential_decay', 'piecewise_linear'],
        'piecewise_linear': ['gaussian_mixture', 'bspline', 'oscillatory_decay', 'multi_level_asymmetric'],
        'unknown_or_piecewise_linear': ['gaussian_mixture', 'bspline', 'oscillatory_decay', 'exponential_decay']
    }
    
    analysis['suggested_families'] = orthogonal_suggestions.get(analysis['family'], ['gaussian_mixture', 'bspline', 'oscillatory_decay'])
    analysis['failure_hypothesis'] = 'Step-function-like approaches have sharp transitions that create constructive interference in the convolution, leading to local optima. Smooth functions (Gaussian mixtures, splines) or structured functions (oscillatory with decay) may achieve better ||f★f||_2^2 / ||f★f||_∞ ratios by distributing mass more evenly.'
    
    return {
        'current_family': analysis['family'],
        'reasoning': analysis['reasoning'],
        'suggested_families': analysis['suggested_families'],
        'failure_hypothesis': analysis['failure_hypothesis'],
        'note': 'Use this analysis to diversify your exploration. Call generate_candidates with these suggested families.'
    }
