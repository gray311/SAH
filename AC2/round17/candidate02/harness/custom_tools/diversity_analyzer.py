def run(ctx, args):
    import math
    best_f = ctx.get_best_program()
    if not best_f or "jnp.zeros" in best_f:
        return {"note": "no best function yet", "directions": ["try Gaussian mixture", "try B-spline", "try oscillatory decay"]}
    
    # Extract key characteristics from the code
    has_gaussian = "exp(-((x" in best_f or "exp(" in best_f
    has_step = "jnp.zeros" in best_f and "base_height" in best_f
    has_spline = "splev" in best_f or "splrep" in best_f
    has_oscillatory = "cos(" in best_f or "sin(" in best_f
    has_piecewise = "piecewise" in best_f
    
    diversity_score = 0.0
    suggested_directions = []
    
    # Score diversity (0 = all same family, 1 = diverse)
    family_types = [has_gaussian, has_step, has_spline, has_oscillatory, has_piecewise]
    diversity_score = sum(family_types) / 5.0
    
    if diversity_score < 0.4:
        suggested_directions.append("Try completely different family from current one")
    
    # Suggest mutations based on what's missing
    if not has_gaussian:
        suggested_directions.append("Add Gaussian mixture component")
    if not has_spline:
        suggested_directions.append("Try B-spline basis with softplus constraints")
    if not has_oscillatory:
        suggested_directions.append("Add oscillatory term: (1 + α cos(βx)) * exp(-γ|x|)")
    if not has_piecewise:
        suggested_directions.append("Use piecewise-linear with optimized vertices")
    
    # Get current best score
    best_c2 = ctx.best_score()
    
    return {
        "best_function_characteristics": {
            "has_gaussian": has_gaussian,
            "has_step": has_step,
            "has_spline": has_spline,
            "has_oscillatory": has_oscillatory,
            "has_piecewise": has_piecewise,
        },
        "diversity_score": float(diversity_score),
        "suggested_directions": suggested_directions,
        "current_best_c2": best_c2,
        "note": "Use these directions to generate diverse candidates with generate_candidates"
    }
