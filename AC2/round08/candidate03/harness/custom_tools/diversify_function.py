def run(ctx, args):
    import random
    current_f = ctx.get_best_program()
    current_family = "step"
    if "spline" in current_f.lower():
        current_family = "spline"
    elif "fourier" in current_f.lower() or "cos" in current_f.lower():
        current_family = "fourier"
    elif "polynomial" in current_f.lower() or "decay" in current_f.lower():
        current_family = "polynomial"
    elif "gaussian" in current_f.lower() or "exp" in current_f.lower():
        current_family = "gaussian"
    
    all_families = ["step", "spline", "fourier", "polynomial", "gaussian", "hybrid", "adaptive"]
    candidates = [f for f in all_families if f != current_family]
    family = random.choice(candidates)
    
    hints = {
        "spline": "Use scipy.interpolate.splrep/splev with knots in [-3, 3]",
        "fourier": "Use sum of cos(k*pi*x/L) with softplus coefficients",
        "polynomial": "Use (1 - |x|/R)^alpha for |x|<R, 0 otherwise",
        "gaussian": "Sum of exp(-a*(x-x0)^2) with softplus for amplitude",
        "hybrid": "Step function in center, Gaussian tails",
        "adaptive": "Start coarse, refine near peaks",
        "step": "Seed's style step function"
    }
    return {"family": family, "hint": hints.get(family, "Implement {family} function")}
