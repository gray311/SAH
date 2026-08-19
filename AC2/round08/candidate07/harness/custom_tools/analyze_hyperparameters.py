def run(ctx, args):
    code = ctx.get_program()
    import re

    # Extract OptimizerHyperparameters values
    patterns = {
        'num_intervals': r'num_intervals:\s*([\d.]+)',
        'learning_rate': r'learning_rate:\s*([\d.]+)',
        'num_steps': r'num_steps:\s*([\d.]+)',
        'warmup_steps': r'warmup_steps:\s*([\d.]+)',
        'best_c2': r'best_c2:\s*([\d.]+)',
        'stagnation_window': r'stagnation_window:\s*([\d.]+)',
        'reinit_fraction': r'reinit_fraction:\s*([\d.]+)',
        'reinit_std': r'reinit_std:\s*([\d.]+)',
        'reinit_interval': r'reinit_interval:\s*([\d.]+)',
    }

    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, code)
        if match:
            result[key] = float(match.group(1))
        else:
            result[key] = None

    return result
