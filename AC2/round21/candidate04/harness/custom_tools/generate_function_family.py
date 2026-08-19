def run(ctx, args):
    import random
    random.seed(42)
    family_choices = [
        ("gaussian_mixture", "Define f(x) as sum of 3-5 Gaussians with varied sigma, optimize mu and weight"),
        ("b_spline", "Use B-spline basis with 10-15 knots. Optimize knot positions first, then coefficients."),
        ("hybrid_step_smooth", "Step base (like seed) but add smooth Gaussian tails on both sides"),
        ("step_with_wings", "Keep step base but add asymmetric exponential decay wings on edges"),
        ("multi_gaussian", "Weighted sum of Gaussians. Optimize center separation"),
        ("piecewise_linear", "Linear pieces with optimized slopes and continuity"),
    ]
    chosen = random.choice(family_choices)
    return {"family_type": chosen[0], "prompt": chosen[1],
            "strategy": f"Implement {chosen[0]} with 3-5 key parameters",
            "parameters_to_optimize": 3}
