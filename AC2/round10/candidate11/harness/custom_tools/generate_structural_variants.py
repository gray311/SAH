def run(ctx, args):
    import re
    prog = ctx.get_program()
    if "# EVOLVE-BLOCK" not in prog:
        return {"note": "no evolve block"}
    
    n_match = re.search(r'num_intervals:\s*(\d+)', prog)
    n = int(n_match.group(1)) if n_match else 450
    
    patterns = []
    
    h7 = [0.5, 1.0, 1.7, 2.3, 1.6, 1.0, 0.5]
    s7 = [0.06, 0.15, 0.27, 0.39, 0.51, 0.63, 0.75, 0.86]
    p7 = {
        "name": "pyramid_7level",
        "heights": h7,
        "starts": [int(si*n) for si in s7[:-1]],
        "ends": [int(si*n) for si in s7[1:]]
    }
    patterns.append(p7)
    
    h2 = [0.6, 0.4, 2.4, 2.1, 2.0, 0.4, 0.6]
    s2 = [0.05, 0.12, 0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.80]
    p2 = {
        "name": "bimodal_dual",
        "heights": h2,
        "starts": [int(si*n) for si in s2[:-1]],
        "ends": [int(si*n) for si in s2[1:]]
    }
    patterns.append(p2)
    
    h3 = [0.5, 1.1, 2.0, 1.2, 1.5, 1.0, 0.6]
    s3 = [0.05, 0.13, 0.23, 0.33, 0.43, 0.55, 0.67, 0.79, 0.89]
    p3 = {
        "name": "tri_asymmetric",
        "heights": h3,
        "starts": [int(si*n) for si in s3[:-1]],
        "ends": [int(si*n) for si in s3[1:]]
    }
    patterns.append(p3)
    
    h4 = [0.5, 0.7, 1.4, 2.1, 2.1, 1.4, 0.7, 0.5]
    s4 = [0.04, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.82]
    p4 = {
        "name": "plateau",
        "heights": h4,
        "starts": [int(si*n) for si in s4[:-1]],
        "ends": [int(si*n) for si in s4[1:]]
    }
    patterns.append(p4)
    
    h5 = [0.6, 1.2, 1.8, 2.4, 1.8, 1.2, 0.6]
    s5 = [0.06, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.86]
    p5 = {
        "name": "hybrid_pyramid",
        "heights": h5,
        "starts": [int(si*n) for si in s5[:-1]],
        "ends": [int(si*n) for si in s5[1:]]
    }
    patterns.append(p5)
    
    h6 = [0.5, 0.6, 0.7, 2.2, 1.8, 1.9, 0.7, 0.6, 0.5]
    s6 = [0.04, 0.10, 0.18, 0.28, 0.38, 0.48, 0.58, 0.68, 0.78, 0.88]
    p6 = {
        "name": "extended_bimodal",
        "heights": h6,
        "starts": [int(si*n) for si in s6[:-1]],
        "ends": [int(si*n) for si in s6[1:]]
    }
    patterns.append(p6)
    
    result = {"n_intervals": n, "patterns": []}
    for p in patterns:
        result["patterns"].append({
            "name": p["name"],
            "heights": p["heights"],
            "starts": p["starts"],
            "ends": p["ends"]
        })
    
    return result
