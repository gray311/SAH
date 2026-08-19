def run(ctx, args):
    program = ctx.get_program()
    text = str(program)
    analysis = {"class": "unknown", "params": "N/A", "stability": "unknown", "suggestions": []}
    
    if "B-spline" in text or "bspline" in text.lower():
        analysis["class"] = "B-spline"
        analysis["params"] = "knot positions + coefficients"
        analysis["stability"] = "good"
        analysis["suggestions"] = ["Try piecewise-constant (step functions)", "Try Gaussian mixtures", "Try Fourier-space optimization"]
    elif "Gaussian" in text or "gaussian" in text.lower():
        analysis["class"] = "Gaussian mixture"
        analysis["params"] = "means + variances + weights (K components)"
        analysis["stability"] = "excellent"
        analysis["suggestions"] = ["Try piecewise-constant (step functions)", "Try exponential combinations", "Try B-splines"]
    elif "step" in text.lower() or "piecewise-constant" in text.lower():
        analysis["class"] = "Piecewise-constant"
        analysis["params"] = "bin heights"
        analysis["stability"] = "good"
        analysis["suggestions"] = ["Try piecewise-linear for smoother transitions", "Try Gaussian mixtures", "Try asymmetric step functions"]
    elif "piecewise-linear" in text.lower() or "interpolation" in text.lower():
        analysis["class"] = "Piecewise-linear"
        analysis["params"] = "node values"
        analysis["stability"] = "good"
        analysis["suggestions"] = ["Try piecewise-constant (step functions)", "Try Gaussian mixtures", "Try Fourier-based constructions"]
    elif "exponential" in text.lower() or "decay" in text.lower():
        analysis["class"] = "Exponential decay"
        analysis["params"] = "rates + shapes"
        analysis["stability"] = "excellent"
        analysis["suggestions"] = ["Try Gaussian mixtures", "Try piecewise-constant", "Try B-splines"]
    elif "Fourier" in text or "fft" in text.lower():
        analysis["class"] = "Fourier-based"
        analysis["params"] = "coefficients"
        analysis["stability"] = "depends on discretization"
        analysis["suggestions"] = ["Try piecewise-constant", "Try B-splines", "Try exponential combinations"]
    elif "GaussianMixture" in text or "GMM" in text:
        analysis["class"] = "Gaussian mixture"
        analysis["params"] = "means + variances + weights"
        analysis["stability"] = "excellent"
        analysis["suggestions"] = ["Try piecewise-constant (step functions)", "Try exponential combinations", "Try B-splines"]
    else:
        analysis["class"] = "Custom/Other"
        analysis["params"] = "varies"
        analysis["stability"] = "to be determined"
        analysis["suggestions"] = ["Try step functions (piecewise-constant)", "Try Gaussian mixtures", "Try B-splines", "Try exponential combinations", "Try Fourier-based optimization"]
    
    return analysis
