def run(ctx, args):
    code = ctx.get_program()
    # Look for jnp.piecewise, jnp.where patterns that indicate step functions
    has_piecewise = 'jnp.piecewise' in code or 'piecewise' in code.lower()
    has_where_steps = 'jnp.where' in code
    
    # Check for linear patterns (slope terms like x, or linear expressions)
    linear_indicators = [
        'jnp.where' in code and ('x <' in code or 'x >' in code or 'x <= ' in code),
        'x *' in code or '+ x' in code or '- x' in code,
    ]
    
    # Extract function type based on patterns
    if has_piecewise and not ('jnp.linspace' in code or 'np.linspace' in code):
        func_type = 'step'
        is_step = True
    elif 'jnp.linspace' in code or 'np.linspace' in code:
        func_type = 'linear'
        is_step = False
    elif any('jnp.where' in line and 'jnp.where' in ctx.get_program() for line in code.split('\n')[:10]):
        # Check if where statements create constants or linear functions
        func_type = 'step' if 'constant' in ctx.get_program().lower() else 'unknown'
        is_step = True
    elif 'lambda x' in code or 'x**' in code:
        func_type = 'nonlinear'
        is_step = False
    else:
        func_type = 'unknown'
        is_step = None
    
    # Estimate number of steps/regions
    import re
    regions = re.findall(r'x\s*[><=]\s*[0-9.-]+', code)
    num_regions = len(set(regions)) if regions else 0
    num_steps = num_regions // 2 if num_regions > 0 else 0
    
    return {
        'function_type': func_type,
        'is_piecewise_constant': is_step if is_step is not None else False,
        'num_regions': num_regions,
        'estimated_num_steps': num_steps,
        'has_piecewise': has_piecewise,
        'has_linear': any('x*' in line or '+x' in line or '-x' in line 
                        for line in code.split('\n') if 'where' in line.lower())
    }
