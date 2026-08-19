def run(ctx, args):
    import random
    pattern_idx = args.get("pattern_idx", random.randint(0, 13))
    height_scale = args.get("height_scale", 1.0)
    width_scale = args.get("width_scale", 1.0)
    symmetry_var = args.get("symmetry_var", 0.0)
    
    # Define perturbations for this pattern
    perturbations = []
    
    for scale_mult in [0.85, 0.95, 1.0, 1.1, 1.2]:
        for width_adj in [-0.05, 0.05, 0.0]:
            perturbations.append({
                "height_scale": height_scale * scale_mult,
                "width_scale": width_scale * width_adj,
                "symmetry_var": symmetry_var
            })
    
    return {
        "pattern_idx": pattern_idx,
        "num_variants": len(perturbations),
        "perturbations": perturbations,
        "note": f"Parameterizing seed pattern {pattern_idx} with {len(perturbations)} variants"
    }
