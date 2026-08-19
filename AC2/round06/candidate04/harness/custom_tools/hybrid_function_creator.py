def run(ctx, args):
    import random
    config = args
    hybrid_type = config.get("hybrid_type", "smooth_steps")
    num_peaks = config.get("num_peaks", random.randint(2, 4))
    base_height = config.get("base_height", 1.0)
    
    n = ctx.get_program().count("num_intervals") or 350
    
    if hybrid_type == "smooth_steps":
        code = '''def _create_smooth_step(key):
    n = %d
    f = jnp.zeros(n)
    step_levels = [%f, %f, %f]
    positions = [%d, %d, %d]
    for i, (h, p) in enumerate(zip(step_levels, positions)):
        f = f.at[p-p*0.1:p+p*0.1].set(h)
    return f''' % (n, base_height, base_height*1.2, base_height*0.8, int(0.1*n), int(0.4*n), int(0.7*n))
        return {"type": hybrid_type, "code": code, "comment": "Smooth step transitions"}
    
    elif hybrid_type == "plateau_edges":
        code = '''def _create_plateau_edges(key):
    n = %d
    plateau_width = int(%d)
    left_slope = jnp.linspace(0, %f, int(%d))
    plateau = jnp.full(plateau_width, %f)
    right_slope = jnp.linspace(%f, 0, int(%d))
    f = jnp.concatenate([left_slope, plateau, right_slope])
    return f''' % (n, int(0.4*n), base_height, int(0.2*n), base_height, base_height, int(0.2*n))
        return {"type": hybrid_type, "code": code, "comment": "Plateau with sloped edges"}
    
    elif hybrid_type == "multi_hump":
        code = '''def _create_multi_hump(key):
    n = %d
    f = jnp.zeros(n)
    peak_widths = [int(%d)] * %d
    peak_centers = [%d, %d, %d]
    peak_heights = [%f, %f, %f]
    
    for c, w, h in zip(peak_centers, peak_widths, peak_heights):
        radius = int(w / 2)
        left = jnp.linspace(0, h, radius)
        right = jnp.linspace(h, 0, radius)
        combined = left + right
        f = f.at[c-radius:c+radius].set(combined)
    return f''' % (n, int(0.1*n), num_peaks, int(0.2*n), int(0.4*n), int(0.6*n), base_height, base_height*1.2, base_height*1.0)
        return {"type": hybrid_type, "code": code, "comment": "Multiple Gaussian-like peaks"}
    
    return {"type": "unknown", "error": "Invalid hybrid type"}
