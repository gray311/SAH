def run(ctx, args):
    import random
    family = args.get("family", "gaussian_mixture")
    seed = args.get("seed_variation", 0)
    random.seed(seed)
    
    families = {
        "spline": {
            "type": "cubic_spline",
            "params": {
                "num_control_points": random.choice([8, 10, 12]),
                "num_intervals": ctx.hypers.num_intervals if hasattr(ctx, 'hypers') else 400,
                "continuity": "c2"
            },
            "hint": "Use scipy.interpolate.CubicSpline with these control points. Ensure f(x) >= 0 everywhere."
        },
        "fourier": {
            "type": "fourier_optimized",
            "params": {
                "num_modes": random.choice([10, 15, 20]),
                "optimization_method": "coordinate_descent",
                "positivity_constraint": "via_phase"
            },
            "hint": "Optimize Fourier coefficients. Enforce positivity in spatial domain using phase constraints."
        },
        "gaussian_mixture": {
            "type": "gaussian_mixture",
            "params": {
                "num_components": random.choice([5, 7, 9, 12]),
                "activation": "softplus"
            },
            "hint": "f(x) = Σ w_i * exp(-((x-μ_i)/σ_i)²). Optimize w, μ, σ with softplus for positivity."
        },
        "piecewise_poly": {
            "type": "piecewise_polynomial",
            "params": {
                "degree": random.choice([2, 3]),
                "num_pieces": random.choice([6, 8, 10]),
                "continuity": "c2"
            },
            "hint": "Use piecewise quadratic/cubic polynomials. Ensure C² continuity at breakpoints."
        }
    }
    
    config = families[family]
    return {
        "family": config["type"],
        "params": config["params"],
        "hint": config["hint"],
        "note": "This is a complete function family specification. Use this to replace the entire EVOLVE-BLOCK."
    }
