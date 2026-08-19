def run(ctx, args):
    import math
    import numpy as np

    sigma = args.get("sigma", 1.0)
    step_width = args.get("step_width", 2.0)
    step_height = args.get("step_height", 0.5)
    
    def hybrid_func(x):
        gaussian = np.exp(-x**2 / (2 * sigma**2))
        step_mask = np.abs(x) > step_width
        hybrid = np.maximum(gaussian, step_mask * (step_height - gaussian))
        return hybrid
    
    result = {
        "type": "hybrid_gaussian_step",
        "sigma": sigma,
        "step_width": step_width,
        "step_height": step_height,
        "note": "Hybrid approach - smooth center, step wings. Good for exploring near-record solutions."
    }
    return result