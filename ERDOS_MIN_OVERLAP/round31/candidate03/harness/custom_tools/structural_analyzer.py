def run(ctx, args):
    import re
    import numpy as np
    h_str = ctx.get_best_program()
    if h_str is None or h_str == "":
        return {"error": "No best program available"}
    
    # Extract h array - look for different patterns
    patterns = [
        r"'\s*=.*array\s*\(([^)]+)",
        r'h\s*=.*array\s*\(([^)]+)',
        r'h\s*=.*np\.array\s*\(([^)]+)'
    ]
    
    match = None
    for pattern in patterns:
        m = re.search(pattern, h_str, re.IGNORECASE)
        if m:
            match = m
            break
    
    if not match:
        return {"error": "Could not parse h array. Tried patterns: " + str(patterns)}
    
    try:
        h_vals = [float(x.strip()) for x in match.group(1).split(",")]
        h_vals = np.array(h_vals, dtype=np.float64)
    except Exception as e:
        return {"error": "Failed to parse h values: " + str(e)}
    
    N = len(h_vals)
    domain = 2.0
    dx = domain / N
    
    integral_h = float(np.trapz(h_vals, dx=dx))
    h_min = float(np.min(h_vals))
    h_max = float(np.max(h_vals))
    
    constraint_violated = integral_h != 1.0 or h_min < 0.0 or h_max > 1.0
    
    return {
        "h_array": h_vals.tolist(),
        "integral_h": integral_h,
        "h_min": h_min,
        "h_max": h_max,
        "constraint_violated": constraint_violated,
        "step_count": N,
        "dx": float(dx)
    }
