def run(ctx, args):
    import random
    random.seed(42)
    candidates = []
    n_intervals = ctx.hypers.num_intervals if hasattr(ctx, 'hypers') else 450
    
    # Step variants
    patterns = [
        {"type": "step", "heights": [1.40, 1.60], "positions": [0.25, 0.75]},
        {"type": "step", "heights": [1.1, 1.9, 1.1], "positions": [0.15, 0.40, 0.70]},
        {"type": "symmetric", "heights": [1.3, 1.8, 1.3], "positions": [0.15, 0.4, 0.65, 0.85]},
    ]
    for i, p in enumerate(patterns):
        candidates.append({
            "class": "step_variant",
            "pattern_idx": i,
            "params": p
        })
    
    # Gaussian mixture
    candidates.append({
        "class": "gaussian_mixture",
        "num_components": 3,
        "means": [0.1, 0.5, 0.9],
        "sigmas": [0.15, 0.25, 0.15],
        "weights": [0.3, 0.4, 0.3]
    })
    
    # Spline variant
    candidates.append({
        "class": "cubic_spline",
        "num_knots": 30,
        "knot_quantiles": [i/30 for i in range(1, 30)],
        "initial_coeffs": [0.5 + random.random() * 0.5] * 30
    })
    
    return {
        "diversity_samples": candidates,
        "note": "These diverse classes should be tested with evaluate_solution"
    }
