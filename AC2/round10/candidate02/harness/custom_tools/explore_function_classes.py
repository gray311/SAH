def run(ctx, args):
    import random
    import re
    import json
    diversity = args.get("diversity_mode", "balanced")
    n_candidates = args.get("num_candidates", 50)
    probe_budget = args.get("probe_budget", 10)
    
    # Read current program to understand structure
    prog = ctx.get_program()
    
    # Generate diverse candidates
    candidates = []
    
    # Category 1: Step function variations
    if "step" in diversity or diversity == "steps_only":
        n_intervals = ctx.hypers.get("num_intervals", 450)
        for base_h in [1.40, 1.50, 1.60, 1.70, 1.80]:
            for width_mod in [0.85, 0.90, 0.95, 1.0, 1.05]:
                for pos_mod in [0.90, 0.95, 1.0, 1.05]:
                    if len(candidates) >= n_candidates:
                        break
                    candidates.append({
                        "type": "step",
                        "base_height": base_h,
                        "width_mod": width_mod,
                        "pos_mod": pos_mod
                    })
        if len(candidates) < n_candidates:
            # Add multi-level variations
            for n_levels in [3, 4, 5]:
                if len(candidates) >= n_candidates:
                    break
                heights = sorted([random.uniform(1.0, 2.2) for _ in range(n_levels)], reverse=True)
                candidates.append({
                    "type": "multi_step",
                    "n_levels": n_levels,
                    "heights": heights
                })
    
    # Category 2: Smooth functions (sigmoid-like)
    if "smooth" in diversity:
        for center in [0.25, 0.30, 0.35, 0.5, 0.65, 0.70, 0.75]:
            for width in [0.15, 0.20, 0.25, 0.30]:
                for amp in [1.0, 1.2, 1.4, 1.6, 1.8]:
                    if len(candidates) >= n_candidates:
                        break
                    candidates.append({
                        "type": "sigmoid",
                        "center": center,
                        "width": width,
                        "amplitude": amp
                    })
    
    # Category 3: Mixture models
    if "mixture" in diversity:
        n_mixtures = min(10, n_candidates - len(candidates))
        base_funcs = ["step", "step", "sigmoid"]
        for _ in range(n_mixtures):
            if len(candidates) >= n_candidates:
                break
            components = random.sample(base_funcs, 2)
            weights = [random.uniform(0.3, 0.7) for _ in range(2)]
            weights = [w / sum(weights) for w in weights]
            candidates.append({
                "type": "mixture",
                "components": components,
                "weights": weights
            })
    
    # Category 4: Asymmetric patterns
    if "asymmetric" in diversity:
        n_asym = min(5, n_candidates - len(candidates))
        for shift in [0.1, 0.2, 0.3, 0.4]:
            if len(candidates) >= n_candidates:
                break
            candidates.append({
                "type": "asymmetric",
                "shift": shift,
                "left_height": random.uniform(0.6, 1.0),
                "right_height": random.uniform(1.4, 2.0)
            })
    
    # Category 5: High resolution
    if "high_res" in diversity:
        n_high = min(3, n_candidates - len(candidates))
        for n in [600, 800, 1000]:
            if len(candidates) >= n_candidates:
                break
            candidates.append({
                "type": "high_res",
                "num_intervals": n
            })
    
    # Fill remaining with random variations
    while len(candidates) < n_candidates:
        c = {"type": "random", "seed": random.randint(0, 10000)}
        if c not in candidates:
            candidates.append(c)
    
    # Write candidates to scratch space
    scratch_content = json.dumps({"candidates": candidates})
    ctx.scratch_write("function_candidates", scratch_content)
    
    # Probe the top candidates by chance (to give solver options)
    top_probe = random.sample(range(len(candidates)), min(probe_budget, len(candidates)))
    top_indices = sorted(top_probe)
    
    return {
        "total_candidates": len(candidates),
        "candidate_classes": ["step_variants", "multi_step", "sigmoid", "mixture", "asymmetric", "high_res"],
        "top_probe_indices": top_indices[:probe_budget],
        "instruction": f"Use probe_solution on indices {top_indices[:probe_budget]} to find promising candidates, then evaluate the best."
    }