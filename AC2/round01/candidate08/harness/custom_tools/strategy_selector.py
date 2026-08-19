def run(ctx, args):
    best_score = ctx.best_score()
    evals_left = ctx.budget_left()
    notes = ctx.scratch_read("strategy_notes") or ""
    
    if best_score < 0.95:
        candidates = [
            {"rep": "piecewise_linear", "opt": "adam", "reason": "Start with simple piecewise linear, Adam optimizer"},
            {"rep": "gaussian_mixture", "opt": "adam", "reason": "Try smooth Gaussian-based functions"},
            {"rep": "step_function", "opt": "gradient_ascent", "reason": "Step functions achieve ~0.896 historically"}
        ]
    elif best_score < 0.98:
        candidates = [
            {"rep": "adaptive_resolution", "opt": "adam", "reason": "Refine discretization coarser-to-finer"},
            {"rep": "fourier_truncation", "opt": "lbfgs", "reason": "Optimize Fourier coefficients with positivity constraint"},
            {"rep": "spline_bezier", "opt": "coordinate_descent", "reason": "Try B-spline or Bezier representation"}
        ]
    elif best_score < 0.998:
        candidates = [
            {"rep": "piecewise_robust", "opt": "l_bfgs", "reason": "Refine piecewise linear with more intervals and L-BFGS"},
            {"rep": "ensemble_mix", "opt": "evolutionary", "reason": "Combine multiple promising functions"},
            {"rep": "adaptive_parameterization", "opt": "simulated_annealing", "reason": "Adaptively tune parameters per region"}
        ]
    else:
        candidates = [
            {"rep": "hyperrefinement", "opt": "lbfgs", "reason": "High-resolution L-BFGS refinement"},
            {"rep": "fourier_fine", "opt": "coordinate_descent", "reason": "Fine-tune Fourier-based representation"},
            {"rep": "multi_obj_pareto", "opt": "evolutionary", "reason": "Multi-objective exploration near optimum"}
        ]
    
    ctx.scratch_write("strategy_notes", str(candidates))
    return {"best": candidates[0], "alternatives": candidates[1:3],
            "note": f"Current: {best_score:.6f}, Evals left: {evals_left}"}
