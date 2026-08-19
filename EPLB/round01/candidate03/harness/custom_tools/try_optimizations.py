def run(ctx, args):
    base = args.get("base_approach", "current")
    families = args.get("variant_families", ["vectorize", "precompute"])
    n_trials = args.get("num_trials", 5)
    
    if n_trials < 3 or n_trials > 10:
        return {"error": "num_trials must be 3-10", "best": None}
    
    results = []
    families = list(families)[:n_trials]
    
    for i, fam in enumerate(families):
        variant_desc = {
            "vectorize": "Replace loops with vectorized ops",
            "precompute": "Cache layer statistics upfront",
            "waterfill": "Use water-filling heuristic for packing",
            "sort_then_assign": "Sort by weight, greedy assign to min pack",
            "inplace": "Pre-allocate tensors, minimize copies"
        }.get(fam, "Optimization family: " + fam)
        
        score_hint = i + 1
        
        results.append({
            "family": fam,
            "description": variant_desc,
            "probe_rank": score_hint,
            "suggested": (i == 0)
        })
    
    results.sort(key=lambda x: x["probe_rank"])
    
    return {
        "results": results,
        "recommended": results[0]["family"] if results else None,
        "note": "Use recommended family to guide next edit. Generate actual code for that variant family."
    }
