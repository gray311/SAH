def run(ctx, args):
    breakpoints = args.get("breakpoints", [])
    values = args.get("values", [])
    target_int = args.get("target_integral", 1.0)
    
    if len(breakpoints) != len(values) or len(breakpoints) < 2:
        return {"error": "Invalid breakpoints/values"}
    
    # Sort breakpoints in [0, 2]
    sorted_bps = sorted([0.0] + breakpoints + [2.0])
    if len(sorted_bps) < 2:
        return {"error": "Need at least 2 breakpoints"}
    
    # Compute current integral
    intervals = [(sorted_bps[i], sorted_bps[i+1], values[i]) 
                for i in range(len(sorted_bps)-1)]
    current_int = sum((b2-b1)*v1 for (b1,b2,v1) in intervals)
    
    if current_int == 0:
        return {"error": "Integral is zero, cannot normalize"}
    
    scale = target_int / current_int
    scaled_values = [v * scale for v in values]
    
    # Return piecewise definition
    intervals_str = []
    for i in range(len(sorted_bps)-1):
        b1, b2, v = sorted_bps[i], sorted_bps[i+1], scaled_values[i]
        intervals_str.append(f"[{b1:.4f}, {b2:.4f}): value={v:.4f}")
    
    return {
        "function": "piecewise_constant",
        "intervals": intervals_str,
        "integral": float(current_int * scale),
        "scaled_values": scaled_values,
        "note": f"Scaled from integral {current_int:.4f} to {target_int:.4f}"
    }
