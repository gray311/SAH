def run(ctx, args):
    from dataclasses import dataclass
    
    N = args.get("num_intervals", 200)
    num_cands = args.get("num_candidates", 10)
    domain_width = 2.0
    dx = domain_width / N
    
    candidates = []
    
    # Pattern 1: Single step on [0, 1]
    h1 = [0.0] * N
    h1 = [1.0 if x <= 1.0 else 0.0 for x in h1]
    candidates.append(("single_step_0_1", h1))
    
    # Pattern 2: Single step on [0, 0.5] with height 2
    h2 = [0.0] * N
    h2 = [2.0 if x <= 0.5 else 0.0 for x in h2]
    candidates.append(("single_step_0_0.5_height2", h2))
    
    # Pattern 3: Uniform on [0, 1]
    h3 = [0.0] * N
    h3 = [1.0 if x <= 1.0 else 0.0 for x in h3]
    candidates.append(("uniform_0_1", h3))
    
    # Pattern 4: Double step - 0.5 on [0,0.5] and [1,1.5]
    h4 = [0.0] * N
    h4 = [0.5 if (x <= 0.5 or x >= 1.0) else 0.0 for x in h4]
    candidates.append(("double_step_split", h4))
    
    # Pattern 5: Step at 0.66 with height 1.5
    h5 = [0.0] * N
    h5 = [1.5 if x <= 2/3 else 0.0 for x in h5]
    candidates.append(("step_0.66_height1.5", h5))
    
    # Pattern 6: Symmetric plateau - 0.5 on [0.25, 1.75]
    h6 = [0.0] * N
    h6 = [0.5 if (x >= 0.25 and x <= 1.75) else 0.0 for x in h6]
    candidates.append(("plateau_0.25_1.75", h6))
    
    # Pattern 7: Triangle shape - ramps up then down
    h7 = [0.0] * N
    h7 = [min(x/1.0, 2-x)/1.0 for x in h7]
    h7 = [max(0.0, min(1.0, v)) for v in h7]
    candidates.append(("triangle", h7))
    
    # Pattern 8: Three equal steps on [0,2/3], [2/3,4/3], [4/3,2]
    h8 = [0.0] * N
    h8 = [1.5 if (x >= 0 and x < 2/3) else 0.0 for x in h8]
    h8 = [1.5 if (x >= 2/3 and x < 4/3) else h8[i] for i, x in enumerate(h8)]
    h8 = [1.5 if (x >= 4/3 and x <= 2) else h8[i] for i, x in enumerate(h8)]
    candidates.append(("three_steps", h8))
    
    # Pattern 9: Concentrated mass - spike at x=1
    h9 = [0.0] * N
    h9 = [2.0 if (x >= 0.5 and x <= 1.5) else 0.0 for x in h9]
    candidates.append(("spike_0.5_1.5", h9))
    
    # Pattern 10: Gentle ramp
    h10 = [0.0] * N
    h10 = [x / 2.0 for x in h10]
    h10 = [max(0.0, min(1.0, v)) for v in h10]
    candidates.append(("ramp_0_2", h10))
    
    # Select top num_candidates by simple heuristic (max height concentration)
    best_candidates = []
    for name, h in candidates[:num_cands]:
        integral = sum(h) * dx
        valid = 0.99 <= float(integral) <= 1.01
        if valid:
            best_candidates.append((name, h))
        elif len(best_candidates) < num_cands:
            # Allow small violations, try to fix
            best_candidates.append((name, h))
    
    result = []
    for name, h in best_candidates:
        result.append({
            "name": name,
            "h_values": h,
            "num_intervals": N,
            "description": f"Generated candidate: {name}"
        })
    
    return {"candidates": result, "num_generated": len(result)}