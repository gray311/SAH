def run(ctx, args):
    code = ctx.get_program()
    import re
    penalty_match = re.search(r'penalty_strength:\s*float\s*=\s*([\d.]+)', code)
    intervals_match = re.search(r'num_intervals:\s*int\s*=\s*(\d+)', code)
    lr_match = re.search(r'base_learning_rate:\s*float\s*=\s*([\d.eE+-]+)', code)
    steps_match = re.search(r'num_steps:\s*int\s*=\s*(\d+)', code)
    restarts_match = re.search(r'num_restarts:\s*int\s*=\s*(\d+)', code)
    seed_match = re.search(r'seed_start:\s*int\s*=\s*(\d+)', code)
    
    penalty_str = float(penalty_match.group(1)) if penalty_match else 1370.0
    intervals = int(intervals_match.group(1)) if intervals_match else 800
    lr = float(lr_match.group(1)) if lr_match else 0.0053
    steps = int(steps_match.group(1)) if steps_match else 59000
    restarts = int(restarts_match.group(1)) if restarts_match else 3
    seed = int(seed_match.group(1)) if seed_match else 0
    
    sigmoid_ok = 'jax.nn.sigmoid' in code or 'sigmoid' in code
    
    c5_estimate = 0.395 - 0.015 * min(restarts, 5) / 5
    
    return {
        "penalty_strength": penalty_str,
        "num_intervals": intervals,
        "base_learning_rate": lr,
        "num_steps": steps,
        "num_restarts": restarts,
        "seed_start": seed,
        "sigmoid_present": sigmoid_ok,
        "c5_estimate": c5_estimate,
        "note": "Hyperparameter analysis complete"
    }
