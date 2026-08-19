def run(ctx, args):
    import math
    import numpy as np
    template = args.get("template", "high-narrow-peak")
    height_scale = args.get("height_scale", 1.0)
    width_scale = args.get("width_scale", 1.0)
    position_offset = args.get("position_offset", 0.0)
    
    # Default to 600 intervals if not available
    if not hasattr(ctx, '_num_intervals'):
        ctx._num_intervals = 600
    n = ctx._num_intervals
    
    # Create numpy array
    f = np.zeros(n)
    
    # Parse template and generate step function
    if template == "high-narrow-peak":
        start_frac = 0.25 + position_offset * 0.5
        end_frac = 0.75 - position_offset * 0.5
        start = int(n * start_frac)
        end = int(n * end_frac)
        height = 2.0 * height_scale
        f[start:end] = height
    
    elif template == "dual-peaks-symmetric":
        left_start = int(n * 0.15)
        left_end = int(n * 0.40)
        right_start = int(n * 0.60)
        right_end = int(n * 0.85)
        height = 1.8 * height_scale
        f[left_start:left_end] = height
        f[right_start:right_end] = height
    
    elif template == "plateau-center":
        shoulder_start = int(n * 0.1)
        shoulder_end = int(n * 0.9)
        plateau_start = int(n * 0.25)
        plateau_end = int(n * 0.75)
        shoulder_height = 0.8 * height_scale
        plateau_height = 1.5 * height_scale
        f[shoulder_start:shoulder_end] = shoulder_height
        f[plateau_start:plateau_end] = plateau_height
    
    elif template == "asymmetric-triple":
        left_start = int(n * 0.05)
        left_end = int(n * 0.25)
        center_start = int(n * 0.25)
        center_end = int(n * 0.55)
        right_start = int(n * 0.55)
        right_end = int(n * 0.80)
        left_height = 1.3 * height_scale
        center_height = 2.2 * height_scale
        right_height = 1.6 * height_scale
        f[left_start:left_end] = left_height
        f[center_start:center_end] = center_height
        f[right_start:right_end] = right_height
    
    elif template == "step-symmetric":
        levels = [0.6, 1.0, 1.4, 1.8]
        start_fractions = [0.0 + position_offset, 0.2, 0.4 + position_offset, 0.6, 0.8]
        end_fractions = [0.2 + position_offset, 0.4, 0.6 + position_offset, 0.8, 1.0 - position_offset]
        for i, (start_frac, end_frac) in enumerate(zip(start_fractions, end_fractions)):
            start = int(n * start_frac)
            end = int(n * end_frac)
            f[start:end] = levels[i] * height_scale
    
    elif template == "gradient-perturbed":
        # Perturb intervals by ±0.05 and heights by ±0.15
        perturbation = 0.05 * (1 - abs(position_offset) / 0.3)
        start_p = int(n * (0.15 + perturbation))
        left_end_p = int(n * (0.40 - perturbation))
        right_start_p = int(n * (0.60 - perturbation))
        right_end_p = int(n * (0.85 + perturbation))
        height_p = 1.8 * height_scale * (1 + 0.15 * math.sin(position_offset * 10))
        f[start_p:left_end_p] = height_p
        f[right_start_p:right_end_p] = height_p
    
    else:
        # Default: high-narrow-peak
        start = int(n * 0.25)
        end = int(n * 0.75)
        height = 2.0 * height_scale
        f[start:end] = height
    
    return {"function": str(f), "template": template, "n_intervals": n}