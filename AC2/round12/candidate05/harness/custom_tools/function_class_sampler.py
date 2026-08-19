def run(ctx, args):
    import random
    random.seed(42)
    
    classes = [
        {
            "class_name": "gaussian_mixture_2",
            "description": "Two Gaussian peaks with different means and standard deviations",
            "structure": "f(x) = w1*exp(-(x-μ1)²/(2σ1²)) + w2*exp(-(x-μ2)²/(2σ2²))",
            "parameters": {"w1": (0.3, 0.7), "w2": (0.3, 0.7), "μ1": (0.1, 0.4), "σ1": (0.05, 0.15), "μ2": (0.6, 0.9), "σ2": (0.05, 0.15)},
            "implementation_hint": "Use Gaussian PDF formula with soft normalization"
        },
        {
            "class_name": "multi_peak_3",
            "description": "Three asymmetric peaks at different positions with varying heights",
            "structure": "Sum of three narrow Gaussian-like peaks",
            "parameters": {"peak1": {"pos": (0.15, 0.25), "height": (1.0, 2.0), "width": (0.08, 0.15)}, "peak2": {"pos": (0.4, 0.5), "height": (1.2, 2.5), "width": (0.06, 0.12)}, "peak3": {"pos": (0.7, 0.85), "height": (0.8, 1.8), "width": (0.08, 0.15)}},
            "implementation_hint": "Use piecewise linear approximation or narrow Gaussians"
        },
        {
            "class_name": "sigmoid_transition",
            "description": "Smooth transition function using sigmoid-like activation",
            "structure": "f(x) = (1 + tanh(k*(x-x0)))/2 scaled appropriately",
            "parameters": {"x0": (0.3, 0.7), "k": (2.0, 5.0), "scale": (0.5, 1.5)},
            "implementation_hint": "Use sigmoid function with proper normalization"
        },
        {
            "class_name": "asymmetric_decay",
            "description": "Piecewise function with different decay rates on left and right of center",
            "structure": "Left: exponential decay, Right: slower decay or polynomial tail",
            "parameters": {"cutoff": (0.4, 0.6), "left_rate": (0.5, 2.0), "right_rate": (0.1, 0.5)},
            "implementation_hint": "Use different exponential decay functions on either side"
        },
        {
            "class_name": "piecewise_cubic",
            "description": "Three cubic polynomial segments with continuous first and second derivatives",
            "structure": "Cubic spline with optimized knot positions and coefficients",
            "parameters": {"knot1": (0.25, 0.35), "knot2": (0.6, 0.7), "coef_left": (0.5, 2.0), "coef_mid": (0.8, 2.5), "coef_right": (0.6, 2.0)},
            "implementation_hint": "Define cubic polynomials with continuity constraints"
        }
    ]
    
    proposals = []
    for cls in classes:
        proposals.append({
            "class_name": cls["class_name"],
            "description": cls["description"],
            "structure": cls["structure"],
            "parameters": cls["parameters"],
            "implementation_hint": cls["implementation_hint"]
        })
    
    return {
        "proposals": proposals,
        "total_classes": 5,
        "note": "These are distinct function architectures, not mutations of step patterns"
    }
