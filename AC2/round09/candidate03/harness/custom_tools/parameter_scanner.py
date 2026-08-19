def run(ctx, args):
    import random
    random.seed(42)
    base_heights = args.get('base_heights', [])
    base_positions = args.get('base_positions', [])
    n_variants = args.get('n_variants', 5)
    
    if not base_heights:
        return {"note": "no base heights provided"}
    
    var_results = []
    for i in range(n_variants):
        perturbed = []
        for h in base_heights:
            perturbation = (random.random() - 0.5) * 0.1
            new_h = max(0.1, h * (1 + perturbation))
            perturbed.append(round(new_h, 3))
        
        result = {
            "variant": i,
            "perturbed_heights": perturbed,
            "perturbation_range": f"±{0.05:.2f} from base"
        }
        # Use ctx to actually test - probe the variant
        ctx.scratch_write("current_heights", str(perturbed))
        score = ctx.probe() if hasattr(ctx, 'probe') else 0.0
        result["probe_score"] = score
        var_results.append(result)
    
    return {
        "n_variants": n_variants,
        "variants": var_results,
        "best_probe_idx": max(range(len(var_results)), key=lambda i: var_results[i].get("probe_score", 0))
    }
