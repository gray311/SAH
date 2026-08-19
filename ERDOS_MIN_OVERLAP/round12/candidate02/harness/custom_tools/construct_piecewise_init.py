def run(ctx, args):
    import numpy as np
    num_steps = args.get("num_steps", 3)
    seed = args.get("seed", 42)
    target_integral = args.get("target_integral", 1.0)
    
    rng = np.random.default_rng(seed)
    domain = 2.0
    constructions = {}
    
    # Pattern 1: Asymmetric two-step (high plateau + tail)
    if num_steps == 2:
        step_locs = 0.3 + rng.uniform(0, 1)
        # h = alpha on [0, step_locs], beta on [step_locs, 2]
        # alpha*step_locs + beta*(2-step_locs) = 1
        # Try alpha=0.8, solve for beta
        alpha = rng.uniform(0.5, 0.95)
        beta = (target_integral - alpha*step_locs) / (domain - step_locs)
        if 0 <= beta <= 1:
            constructions["asymmetric_2step"] = {
                "steps": [(0, alpha), (step_locs, beta)],
                "valid": True
            }
    
    # Pattern 2: Bimodal three-step (low-high-low)
    if num_steps == 3:
        for _ in range(5):
            a = rng.uniform(0.2, 0.6)
            b = rng.uniform(a + 0.1, 1.5)
            # h = 0 on [0,a], alpha on [a,b], beta on [b,2]
            # alpha*(b-a) + beta*(2-b) = 1
            alpha = rng.uniform(0.7, 1.0)
            beta = (target_integral - alpha*(b-a)) / (domain - b)
            if 0 <= beta <= 1:
                constructions["bimodal_3step_" + str(round(a*100)) + str(round(b*100))] = {
                    "steps": [(0, 0), (a, alpha), (b, beta), (2, 0)],
                    "valid": True
                }
                break
    
    # Pattern 3: Symmetric bimodal (peaks at 0.5, 1.5)
    constructions["symmetric_bimodal"] = {
        "steps": [(0, 0), (0.25, 0.8), (0.75, 0.8), (1.25, 0.8), (1.75, 0.8), (2, 0)],
        "valid": True,
        "note": "Four peaks of height 0.8 at [0.25,0.5], [0.75,1.0], [1.25,1.5], [1.75,2]"
    }
    
    # Pattern 4: Golomb-like spacing (5 peaks)
    peaks = [0.2, 0.5, 0.8, 1.1, 1.4]
    widths = [0.15, 0.2, 0.15, 0.2, 0.15]
    heights = [0.7, 0.6, 0.7, 0.6, 0.7]
    integral = sum(h*w for h,w in zip(heights,widths))
    if 0.8 <= integral <= 1.2:
        constructions["golomb_5peaks"] = {
            "steps": [],
            "peaks": [(p, h, w) for p,h,w in zip(peaks, heights, widths)],
            "integral": integral,
            "valid": True
        }
    
    return {"constructions": constructions, "num_valid": len(constructions)}
