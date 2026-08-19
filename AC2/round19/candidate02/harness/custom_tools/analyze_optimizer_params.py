def run(ctx, args):
    import re
    code = ctx.get_program()
    params = {}
    
    # Extract hyperparameters from the dataclass
    param_patterns = {
        'num_intervals': r'num_intervals:\s*(\d+)',
        'learning_rate': r'learning_rate:\s*([\d.]+)',
        'num_steps': r'num_steps:\s*(\d+)',
        'warmup_steps': r'warmup_steps:\s*(\d+)',
        'best_c2': r'best_c2:\s*([\d.]+)',
        'stagnation_window': r'stagnation_window:\s*(\d+)',
        'reinit_fraction': r'reinit_fraction:\s*([\d.]+)',
        'reinit_std': r'reinit_std:\s*([\d.]+)',
        'reinit_interval': r'reinit_interval:\s*(\d+)'
    }
    
    for name, pattern in param_patterns.items():
        match = re.search(pattern, code)
        if match:
            val = match.group(1)
            try:
                params[name] = float(val) if '.' in val else int(val)
            except:
                params[name] = val
    
    return {
        'current_params': params,
        'note': 'Use these values as baseline for generating variants'
    }
