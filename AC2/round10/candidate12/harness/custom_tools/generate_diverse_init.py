def run(ctx, args):
    import random
    random.seed(hash(ctx.get_program()) % 2**31)
    
    prog = ctx.get_program()
    current_best = ctx.best_score()
    
    # Determine function class based on exploration state
    if random.random() < 0.25:
        # Spline-based: piecewise polynomial
        n_intervals = random.choice([100, 150, 200])
        num_knots = random.choice([10, 15, 20])
        func_type = "B-spline"
        init_str = f"Piecewise cubic B-spline with {num_knots} knots on {n_intervals} intervals"
        params = {
            "knot_positions": [i / (num_knots + 1) for i in range(num_knots + 1)],
            "coefficients": [random.uniform(-1, 1) for _ in range(num_knots + 1)],
            "n_intervals": n_intervals
        }
    elif random.random() < 0.35:
        # Mixture of Gaussians
        num_components = random.choice([3, 4, 5])
        func_type = "Gaussian mixture"
        init_str = f"Sum of {num_components} weighted Gaussians"
        params = {
            "means": [random.uniform(0.3, 0.7) for _ in range(num_components)],
            "stds": [random.uniform(0.1, 0.3) for _ in range(num_components)],
            "weights": [1.0 / num_components for _ in range(num_components)],
            "n_intervals": random.choice([150, 200, 250])
        }
    elif random.random() < 0.35:
        # Asymmetric step function
        num_steps = random.choice([5, 7, 9])
        func_type = "Asymmetric steps"
        init_str = f"Piecewise constant with {num_steps} non-uniform segments"
        params = {
            "n_intervals": random.choice([100, 150, 200]),
            "step_positions": [random.uniform(0.15, 0.85) for _ in range(num_steps - 1)],
            "step_heights": [random.uniform(0.8, 2.5) for _ in range(num_steps)]
        }
    else:
        # Exponential decay variant
        func_type = "Asymmetric exponential"
        init_str = "Exp decay on one side, constant on other"
        params = {
            "decay_rate": random.uniform(0.5, 2.0),
            "start_point": random.uniform(0.3, 0.6),
            "n_intervals": random.choice([150, 200, 250]),
            "height_left": random.uniform(1.0, 2.0),
            "height_right": random.uniform(0.5, 1.5)
        }
    
    result = {
        "function_class": func_type,
        "description": init_str,
        "parameters": params,
        "expected_n_intervals": params["n_intervals"]
    }
    
    return result
