def run(ctx, args):
    import random
    family_type = args.get("family_type", "spline")
    num_components = args.get("num_components", 5)
    
    # Generate diverse function parameters based on family
    if family_type == "spline":
        knots = sorted([round(random.uniform(0.1, 0.9), 3) for _ in range(num_components)])
        weights = [round(abs(random.gauss(1.0, 0.3)), 4) for _ in range(num_components)]
        return {
            "family_type": family_type,
            "note": f"Generated B-spline with {num_components} knots. Use scipy.interpolate.BSpline(knots, weights, k=3) for implementation.",
            "knots": knots,
            "weights": weights
        }
    elif family_type == "mixture":
        mus = [round(random.uniform(0.1, 0.9), 3) for _ in range(num_components)]
        sigmas = [round(random.uniform(0.05, 0.25), 4) for _ in range(num_components)]
        weights = [round(abs(random.gauss(1.0, 0.2)), 4) for _ in range(num_components)]
        return {
            "family_type": family_type,
            "note": f"Generated Gaussian mixture with {num_components} components. Each term: weight * exp(-0.5*((x-mu)/sigma)^2)",
            "mus": mus,
            "sigmas": sigmas,
            "weights": weights
        }
    elif family_type == "learned":
        # Neural network prior parameters
        return {
            "family_type": family_type,
            "note": "Use small MLP: f(x) = softplus(W2 @ tanh(W1 @ x + b1) + b2). Initialize weights with small random values, ensure output >= 0.",
            "hidden_size": num_components * 2,
            "init_scale": 0.1
        }
    else:  # hybrid
        knots = sorted([round(random.uniform(0.1, 0.8), 3) for _ in range(num_components)])
        weights = [round(abs(random.gauss(1.0, 0.3)), 4) for _ in range(num_components)]
        base_height = round(random.uniform(0.8, 1.3), 3)
        return {
            "family_type": family_type,
            "note": f"Hybrid: step base (height={base_height}) with B-spline peaks on knots {knots} with weights {weights}",
            "base_height": base_height,
            "knots": knots,
            "weights": weights
        }
