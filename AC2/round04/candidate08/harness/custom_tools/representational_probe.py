def run(ctx, args):
    program = ctx.get_program()
    text = str(program)
    
    analysis = {
        "detected_class": "unknown",
        "params_count": "N/A",
        "stability": "unknown",
        "alternatives": []
    }
    
    if "piecewise-linear" in text.lower() or "trapezoidal" in text.lower():
        analysis["detected_class"] = "Piecewise-linear"
        analysis["params_count"] = "N+1 node values"
        analysis["stability"] = "good"
        analysis["alternatives"] = [
            "Try piecewise-constant (step functions) - current record holders at 0.8963",
            "Try Gaussian mixtures - smooth localized peaks may concentrate better",
            "Try B-spline basis - local support with C^k continuity"
        ]
    elif "step" in text.lower() or "piecewise-constant" in text.lower():
        analysis["detected_class"] = "Piecewise-constant (step functions)"
        analysis["params_count"] = "N bin heights"
        analysis["stability"] = "excellent"
        analysis["alternatives"] = [
            "Try piecewise-linear - smooth transitions may improve convolution behavior",
            "Try Gaussian mixtures - test if smoothness helps",
            "Try multi-level steps - varying heights in different regions"
        ]
    elif "gaussian" in text.lower() or "normal" in text.lower():
        analysis["detected_class"] = "Gaussian mixture"
        analysis["params_count"] = "K means + variances + weights"
        analysis["stability"] = "excellent"
        analysis["alternatives"] = [
            "Try piecewise-constant - discrete steps may work better",
            "Try piecewise-linear - test smoothness vs sharpness",
            "Try exponential combinations - natural decay alternative"
        ]
    elif "spline" in text.lower() or "bspline" in text.lower():
        analysis["detected_class"] = "B-spline"
        analysis["params_count"] = "knot positions + coefficients"
        analysis["stability"] = "good"
        analysis["alternatives"] = [
            "Try piecewise-constant - simpler, fewer parameters",
            "Try Gaussian mixtures - smoother behavior",
            "Try exponential combinations"
        ]
    elif "exponential" in text.lower() or "decay" in text.lower():
        analysis["detected_class"] = "Exponential combination"
        analysis["params_count"] = "decay rates + shapes + weights"
        analysis["stability"] = "excellent"
        analysis["alternatives"] = [
            "Try piecewise-constant - test if sharp transitions help",
            "Try Gaussian mixtures - test smooth vs sharp",
            "Try piecewise-linear - intermediate smoothness"
        ]
    elif "fourier" in text.lower() or "fft" in text.lower():
        analysis["detected_class"] = "Fourier-based"
        analysis["params_count"] = "coefficients"
        analysis["stability"] = "depends on discretization"
        analysis["alternatives"] = [
            "Try piecewise-constant - simpler representation",
            "Try Gaussian mixtures",
            "Try B-splines"
        ]
    else:
        analysis["detected_class"] = "Custom/Other"
        analysis["params_count"] = "varies"
        analysis["stability"] = "to be determined"
        analysis["alternatives"] = [
            "Try step functions (piecewise-constant) - current record holders",
            "Try Gaussian mixtures - smooth localized peaks",
            "Try B-splines - local support flexibility",
            "Try exponential combinations - natural positive decay"
        ]
    
    return analysis
