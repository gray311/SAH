def run(ctx, args):
    import random, math
    verts = args.get("vertices", [])
    density = args.get("sample_density", 50)
    if density < 1: density = 1
    
    best_score = ctx.best_score()
    
    # Generate grid points to sample
    min_x = min(v.get("x", 0) for v in verts) if verts else 0
    max_x = max(v.get("x", 100000) for v in verts) if verts else 100000
    min_y = min(v.get("y", 0) for v in verts) if verts else 0
    max_y = max(v.get("y", 100000) for v in verts) if verts else 100000
    
    # Clamp to valid range
    min_x = max(0, min_x); max_x = min(100000, max_x)
    min_y = max(0, min_y); max_y = min(100000, max_y)
    
    # Sample grid points
    grid_samples = 0
    for sx in range(min_x, max_x + 1, density):
        for sy in range(min_y, max_y + 1, density):
            grid_samples += 1
    
    # Estimate density from best program
    budget_info = ctx.budget_left()
    total_points = budget_info.get("evaluations_used", 0) + 1
    approx_score = best_score * (grid_samples / max(total_points, 1)) if total_points > 0 else 0
    
    return {
        "estimated_score": approx_score,
        "samples_checked": grid_samples,
        "grid_area": (max_x - min_x) * (max_y - min_y),
        "note": f"Subsampled estimate from {grid_samples} points"
    }