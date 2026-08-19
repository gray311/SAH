def run(ctx, args):
    sample_frac = args.get("sample_frac", 0.05)
    if sample_frac <= 0:
        return {"score": 0, "error": "invalid sample_frac"}
    
    import random
    rng = random.Random(42)
    
    # Get fish list from program or spatial index
    program = ctx.get_program()
    
    # For this task, we need to access the actual fish data
    # Use ctx.read_input_sample to get fish coordinates if available
    # Otherwise, use the fish_structs from the program
    
    # Parse fish from program (extract coordinates and types)
    fish_data = []
    try:
        # Try to access fish from the spatial index or program
        if hasattr(ctx, 'fish_list'):
            fish_data = ctx.fish_list
        elif hasattr(ctx, 'get_fish'):
            fish_data = ctx.get_fish()
    except:
        fish_data = []
    
    if len(fish_data) == 0:
        return {"score": 1, "note": "no fish data available"}
    
    # Sample fish
    num_samples = max(1, int(len(fish_data) * sample_frac))
    sampled_indices = []
    available = list(range(len(fish_data)))
    
    while len(sampled_indices) < num_samples and available:
        idx = rng.choice(available)
        sampled_indices.append(idx)
        available.remove(idx)
    
    # Count mackerels and sardines
    mackerels = 0
    sardines = 0
    
    for idx in sampled_indices:
        fish = fish_data[idx]
        if fish["type"] == 1:  # mackerel
            mackerels += 1
        else:  # sardine
            sardines += 1
    
    estimated_score = mackerels - sardines + 1
    return {"score": estimated_score, "mackerels": mackerels, 
            "sardines": sardines, "sampled": len(sampled_indices),
            "total": len(fish_data)}
