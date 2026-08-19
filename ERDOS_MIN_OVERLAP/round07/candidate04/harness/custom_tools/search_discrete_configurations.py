def run(ctx, args):
    import numpy as np
    num_candidates = args.get("num_candidates", 20)
    num_intervals = args.get("num_intervals", 100)
    dx = 2.0 / num_intervals
    
    candidates = []
    
    # Pattern 1: Single interval concentrated at start
    for i in range(min(5, num_candidates)):
        h = np.zeros(num_intervals)
        h[i] = 1.0 / (num_intervals - i) * (num_intervals // 2)
        h = np.clip(h, 0, 1)
        integral = np.sum(h) * dx
        if abs(integral - 1.0) < 0.01:
            candidates.append({"pattern": f"single_{i}", "h": h.tolist(), "valid": True})
            if len(candidates) >= num_candidates:
                break
        else:
            # Adjust to satisfy constraint
            h = np.ones(num_intervals) * (num_intervals / 2.0)
            h = np.clip(h, 0, 1)
            if len(candidates) < num_candidates:
                candidates.append({"pattern": f"single_{i}_adjusted", "h": h.tolist(), "valid": True})
                if len(candidates) >= num_candidates:
                    break
    
    # Pattern 2: Double interval split
    for i in range(3):
        h = np.zeros(num_intervals)
        left_mass = 1.0 / 2.0
        right_mass = 1.0 - left_mass
        left_h = left_mass / max(1, (i+1))
        right_start = (i+1) % num_intervals
        right_h = right_mass / max(1, num_intervals - right_start)
        h[:i+1] = np.minimum(h[:i+1], left_h)
        h[i+1:] = np.minimum(h[i+1:], right_h)
        h = np.clip(h, 0, 1)
        integral = np.sum(h) * dx
        if abs(integral - 1.0) < 0.05:
            candidates.append({"pattern": f"double_{i}", "h": h.tolist(), "valid": True})
    
    # Pattern 3: Uniform
    h = np.ones(num_intervals) * (num_intervals / 2.0)
    h = np.clip(h, 0, 1)
    integral = np.sum(h) * dx
    if abs(integral - 1.0) < 0.05:
        candidates.append({"pattern": "uniform", "h": h.tolist(), "valid": True})
    
    # Pattern 4: Step patterns
    for k in range(min(5, num_candidates - len(candidates))):
        h = np.zeros(num_intervals)
        num_steps = min(k+3, num_intervals // 2)
        step_height = (num_intervals / 2.0) / num_steps
        for i in range(num_steps):
            h[i*num_steps//num_intervals:(i+1)*num_steps//num_intervals] = step_height
        h = np.clip(h, 0, 1)
        integral = np.sum(h) * dx
        if abs(integral - 1.0) < 0.05:
            candidates.append({"pattern": f"steps_{k}", "h": h.tolist(), "valid": True})
    
    # If not enough candidates, generate random valid ones
    while len(candidates) < num_candidates:
        h = np.random.random(num_intervals)
        h = np.clip(h, 0, 1)
        integral = np.sum(h) * dx
        if abs(integral - 1.0) < 0.05:
            candidates.append({"pattern": f"random_{len(candidates)}", "h": h.tolist(), "valid": True})
    
    return {
        "num_candidates": len(candidates),
        "candidates": candidates,
        "dx": float(dx)
    }
