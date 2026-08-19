def run(ctx, args):
    program = ctx.get_program()
    text = str(program)
    block_start = text.find('# EVOLVE-BLOCK-START')
    block_end = text.find('# EVOLVE-BLOCK-END')
    evolve_block = text[block_start:block_end] if block_start != -1 and block_end != -1 else text
    
    analysis = {
        "detected_class": "unknown",
        "params_count": "N/A",
        "stability": "unknown",
        "recommendation": "Analyze your current representation first"
    }
    
    # Check for piecewise-linear indicators
    if 'piecewise-linear' in text.lower() or 'piecewise linear' in text.lower() or 'trapezoidal' in text.lower():
        analysis['detected_class'] = 'Piecewise-linear'
        analysis['params_count'] = 'N+1 node values'
        analysis['stability'] = 'good'
        analysis['recommendation'] = 'CRITICAL: Record-breakers use piecewise-constant (step functions) at 0.8963! Switch to step functions immediately. Edit your EVOLVE-BLOCK to use step-function initialization with jnp.zeros and jnp.pad or step_height patterns. Test 10+ step variants with probe_solution before evaluating.'
    # Check for piecewise-constant / step functions
    elif 'step' in text.lower() and 'function' in text.lower() or 'piecewise-constant' in text.lower() or 'step' in text.lower() and 'height' in text.lower():
        analysis['detected_class'] = 'Piecewise-constant (step functions)'
        analysis['params_count'] = 'N bin heights'
        analysis['stability'] = 'excellent'
        analysis['recommendation'] = 'Good! You are using step functions. This is the current record-breaker class. Try: different step widths, asymmetric steps, multi-level steps with 2-3 heights, varying support widths.'
    elif 'gaussian' in text.lower() or 'normal' in text.lower() or 'bell' in text.lower():
        analysis['detected_class'] = 'Gaussian mixture'
        analysis['params_count'] = 'K means + variances + weights'
        analysis['stability'] = 'excellent'
        analysis['recommendation'] = 'You are using Gaussian mixtures. Good for smooth functions. Try: K=2,3,5,10 variants, clustered means, small vs large variances. Compare with step functions as baseline.'
    elif 'spline' in text.lower() or 'bspline' in text.lower():
        analysis['detected_class'] = 'B-spline'
        analysis['params_count'] = 'knot positions + coefficients'
        analysis['stability'] = 'good'
        analysis['recommendation'] = 'You are using B-splines. Good for smooth, localized functions. Try: uniform vs adaptive knots, different polynomial degrees.'
    elif 'exponential' in text.lower() or 'decay' in text.lower():
        analysis['detected_class'] = 'Exponential combination'
        analysis['params_count'] = 'decay rates + shapes + weights'
        analysis['stability'] = 'excellent'
        analysis['recommendation'] = 'You are using exponential combinations. Natural decay behavior. Try: single vs double exponential, varying decay rates.'
    else:
        # Default: assume piecewise-linear if no step patterns detected (common seed behavior)
        if 'init' in text.lower() and 'zeros' in text.lower() and 'set' in text.lower():
            analysis['detected_class'] = 'Piecewise-linear'
            analysis['params_count'] = 'N+1 node values'
            analysis['stability'] = 'good'
            analysis['recommendation'] = 'CRITICAL: Detected piecewise-linear! Record-breakers use piecewise-constant (step functions) at 0.8963. SWITCH to step functions. Edit to use: f = jnp.zeros(n); f = f.at[start:end].set(step_height). This is a SIMPLE one-line change from your current approach.'
        else:
            analysis['detected_class'] = 'Custom/Other'
            analysis['params_count'] = 'varies'
            analysis['stability'] = 'to be determined'
            analysis['recommendation'] = 'Could not auto-detect representation class. Try calling probe_solution to test different function representations. Step functions (piecewise-constant) are current record-breakers at 0.8963.'
    
    return analysis
