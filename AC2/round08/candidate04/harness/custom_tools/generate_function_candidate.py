def run(ctx, args):
    import math
    family = args.get('family', 'spline')
    params = args.get('parameters', {})
    num_intervals = params.get('num_intervals', 200)
    
    if family == 'step':
        return {
            'function_def': 'def create_step_function(x, intervals=200):',
            'instructions': 'Create piecewise-constant step with specified heights',
            'type_hints': 'Use jnp.piecewise or direct assignment for constants'
        }
    elif family == 'spline':
        return {
            'function_def': 'def create_spline_function(x, num_knots=20):',
            'instructions': 'Use cubic B-spline with knot optimization',
            'type_hints': 'Knot positions control shape, optimize them'
        }
    elif family == 'mixture':
        return {
            'function_def': 'def create_mixture_function(x, num_components=5):',
            'instructions': 'Gaussian mixture with custom means and variances',
            'type_hints': 'Optimize weights, means, and stds'
        }
    elif family == 'polynomial':
        return {
            'function_def': 'def create_polynomial_function(x, degree=4):',
            'instructions': 'Exponential of polynomial for positivity',
            'type_hints': 'Optimize polynomial coefficients'
        }
    else:
        return {
            'function_def': 'def create_hybrid_function(x):',
            'instructions': 'Hybrid of step base with smooth refinements',
            'type_hints': 'Combine discontinuous and smooth components'
        }
    return {'function': family, 'output': {'function_def': ..., 'instructions': ..., 'type_hints': ...}}
