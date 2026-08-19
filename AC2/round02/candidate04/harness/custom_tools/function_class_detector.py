def run(ctx, args):
    program = ctx.get_program()
    text = str(program)
    result = {"detected_class": "unknown", "exploration_status": "unknown", "recommended_classes": []}
    
    # Detect piecewise-linear (current seed)
    if "piecewise-linear" in text.lower() or ("node" in text.lower() and "interval" in text.lower()):
        result["detected_class"] = "piecewise-linear"
        result["exploration_status"] = "ALREADY_CONVERGED_LOCAL_OPTIMUM"
        result["recommended_classes"] = ["piecewise-constant (step functions)", "Gaussian mixtures", "exponential combinations", "B-splines", "Fourier-based"]
    # Detect step/constant
    elif "step" in text.lower() or "piecewise-constant" in text.lower() or "bin height" in text.lower():
        result["detected_class"] = "piecewise-constant"
        result["exploration_status"] = "HISTORICAL_RECORD_HOLDER"
        result["recommended_classes"] = ["Gaussian mixtures", "exponential combinations", "piecewise-linear (for comparison)", "B-splines"]
    # Detect Gaussian
    elif "Gaussian" in text or "gaussian" in text.lower() or "normal" in text.lower():
        result["detected_class"] = "Gaussian mixture"
        result["exploration_status"] = "PROMISING_CLASS"
        result["recommended_classes"] = ["exponential combinations", "piecewise-constant", "B-splines"]
    # Detect exponential
    elif "exponential" in text.lower() or "decay" in text.lower():
        result["detected_class"] = "exponential"
        result["exploration_status"] = "PROMISING_CLASS"
        result["recommended_classes"] = ["Gaussian mixtures", "piecewise-constant", "B-splines"]
    # Detect spline
    elif "spline" in text.lower() or "B-spline" in text:
        result["detected_class"] = "B-spline"
        result["exploration_status"] = "PROMISING_CLASS"
        result["recommended_classes"] = ["Gaussian mixtures", "exponential combinations", "piecewise-constant"]
    else:
        result["detected_class"] = "custom/other"
        result["exploration_status"] = "UNKNOWN"
        result["recommended_classes"] = ["piecewise-constant", "Gaussian mixtures", "exponential combinations", "B-splines", "piecewise-linear"]
    
    return result
