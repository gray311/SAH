def run(ctx, args):
    program = ctx.get_program()
    import re
    text = str(program)
    analysis = {"class": "unknown", "params": "N/A", "stability": "unknown", "suggestions": []}
    
    if "B-spline" in text or "bspline" in text:
        analysis["class"] = "B-spline"
        analysis["params"] = "knot positions + coefficients"
        analysis["stability"] = "good"
        analysis["suggestions"] = ["Try piecewise-constant (step-like)", "Try Gaussian mixtures"]
    elif "Gaussian" in text or "gaussian" in text:
        analysis["class"] = "Gaussian mixture"
        analysis["params"] = "means + variances + weights"
        analysis["stability"] = "excellent"
        analysis["suggestions"] = ["Try exponential combinations", "Try piecewise-linear with more intervals"]
    elif "step" in text.lower() or "piecewise-constant" in text.lower():
        analysis["class"] = "Piecewise-constant"
        analysis["params"] = "bin heights"
        analysis["stability"] = "good"
        analysis["suggestions"] = ["Try piecewise-linear for smoother transitions", "Try B-splines for flexibility"]
    elif "piecewise-linear" in text.lower():
        analysis["class"] = "Piecewise-linear"
        analysis["params"] = "node values"
        analysis["stability"] = "good"
        analysis["suggestions"] = ["Try piecewise-constant (step functions)", "Try Gaussian mixtures", "Try Fourier-based"]
    elif "exponential" in text.lower() or "decay" in text.lower():
        analysis["class"] = "Exponential decay"
        analysis["params"] = "rates + shapes"
        analysis["stability"] = "excellent"
        analysis["suggestions"] = ["Try Gaussian mixtures", "Try piecewise-constant"]
    elif "Fourier" in text or "fft" in text.lower():
        analysis["class"] = "Fourier-based"
        analysis["params"] = "coefficients"
        analysis["stability"] = "depends on discretization"
        analysis["suggestions"] = ["Try piecewise-constant", "Try B-splines"]
    else:
        analysis["class"] = "Custom/Other"
        analysis["params"] = "varies"
        analysis["stability"] = "to be determined"
        analysis["suggestions"] = ["Try step functions (piecewise-constant)", "Try Gaussian mixtures", "Try B-splines", "Try exponential combinations"]
    
    return analysis
