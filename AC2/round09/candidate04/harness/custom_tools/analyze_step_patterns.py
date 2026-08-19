def run(ctx, args):
    import math
    code = ctx.get_program()
    
    # Parse key parameters from the code
    lines = code.split('\n')
    num_intervals = 400
    learning_rate = 0.22
    num_steps = 37000
    
    for line in lines:
        if 'num_intervals:' in line:
            parts = line.split(':')
            num_intervals = int(parts[1].strip())
        if 'learning_rate:' in line:
            parts = line.split(':')
            learning_rate = float(parts[1].strip())
        if 'num_steps:' in line:
            parts = line.split(':')
            num_steps = int(parts[1].strip())
    
    # Extract step pattern info (simplified heuristic)
    height_range = [0.62, 2.32]  # typical range from seed
    num_heights = 4  # typical multi-level
    
    # Analyze convolution properties (simplified)
    # In practice, this would run the optimizer's _objective_fn with
    # the current parameters and analyze the convolution output
    # For this task, we provide qualitative guidance
    
    pattern_type = "multi-level step"
    
    recommendations = []
    if num_intervals > 300:
        recommendations.append("Consider starting with num_intervals=120 for faster convergence, then refining.")
    if learning_rate > 0.15:
        recommendations.append("Learning rate seems high. Consider 0.1-0.12 for stability.")
    if num_steps > 30000:
        recommendations.append("37000 steps is lengthy. Try 15000-20000 first, then refine.")
    
    recommendations.extend([
        "Try asymmetric patterns (current seed is symmetric)",
        "Explore narrower peaks with higher height (test heights 1.8-2.2)",
        "Consider three-level patterns instead of two-level",
        "Use probe_solution to rank variants before full evaluation"
    ])
    
    return {
        "num_intervals": num_intervals,
        "num_steps": num_steps,
        "learning_rate": learning_rate,
        "pattern_type": pattern_type,
        "height_range": height_range,
        "num_levels": num_heights,
        "symmetry": "symmetric",
        "recommendations": recommendations
    }
